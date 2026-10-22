"""Qdrant: one collection with a dense and a sparse (BM25) vector per section."""
import uuid
from dataclasses import dataclass

from qdrant_client import QdrantClient, models

from .config import Settings
from .embeddings import BM25, DenseEmbedder
from .extract import Section

DENSE, SPARSE = "dense", "sparse"


@dataclass
class Hit:
    id: str
    doc: str
    doc_title: str
    page: int
    section_no: str
    section_title: str
    text: str


def make_client(s: Settings) -> QdrantClient:
    return QdrantClient(url=s.qdrant_url) if s.qdrant_url else QdrantClient(path=s.qdrant_path)


def index(client: QdrantClient, s: Settings, sections: list[Section], dense: DenseEmbedder) -> int:
    """(Re)build the collection. The embedded text carries document and section context."""
    texts = [f"{x.doc_title} - {x.number}. {x.title}: {x.text}" for x in sections]
    bm25 = BM25(texts)
    if client.collection_exists(s.collection):
        client.delete_collection(s.collection)
    client.create_collection(
        s.collection,
        vectors_config={DENSE: models.VectorParams(size=dense.dim, distance=models.Distance.COSINE)},
        sparse_vectors_config={SPARSE: models.SparseVectorParams(modifier=models.Modifier.IDF)},
    )
    points = [
        models.PointStruct(
            id=str(uuid.uuid5(uuid.NAMESPACE_URL, f"{x.doc}|{x.page}|{x.number}")),
            vector={DENSE: vec, SPARSE: bm25.doc(text)},
            payload={"doc": x.doc, "doc_title": x.doc_title, "page": x.page, "section_no": x.number,
                     "section_title": x.title, "text": x.text},
        )
        for x, text, vec in zip(sections, texts, dense.embed(texts))
    ]
    client.upsert(s.collection, points=points, wait=True)
    return len(points)


def search(client: QdrantClient, s: Settings, dense: DenseEmbedder, query: str) -> list[Hit]:
    """Dense and BM25 candidates fused with Reciprocal Rank Fusion inside Qdrant."""
    n = s.top_k * 3
    prefetch = [models.Prefetch(query=dense.embed([query], query=True)[0], using=DENSE, limit=n)]
    if (sparse := BM25.query(query)) is not None:
        prefetch.append(models.Prefetch(query=sparse, using=SPARSE, limit=n))
    res = client.query_points(s.collection, prefetch=prefetch, query=models.FusionQuery(fusion=models.Fusion.RRF),
                              limit=s.top_k, with_payload=True)
    return [Hit(str(p.id), **p.payload) for p in res.points]


def load_all(client: QdrantClient, s: Settings) -> list[Hit]:
    points, _ = client.scroll(s.collection, limit=10_000, with_payload=True)
    return [Hit(str(p.id), **p.payload) for p in points]