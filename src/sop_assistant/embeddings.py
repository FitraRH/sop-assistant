"""Dense (multilingual model) and sparse (BM25) encoders for hybrid search."""
import zlib
from collections import Counter

import numpy as np
from qdrant_client.models import SparseVector

from .config import Settings
from .text import query_terms, tokenize


class DenseEmbedder:
    def __init__(self, s: Settings):
        if s.embed_backend not in ("fastembed", "hash"):
            raise ValueError("EMBED_BACKEND must be 'fastembed' or 'hash'")
        self.hashing = s.embed_backend == "hash"
        if self.hashing:
            self.dim = 512
        else:
            from fastembed import TextEmbedding

            self.model = TextEmbedding(model_name=s.embed_model)
            self.e5 = "e5" in s.embed_model.lower()
            self.dim = len(next(iter(self.model.embed(["x"]))))

    def embed(self, texts: list[str], query: bool = False) -> list[list[float]]:
        if self.hashing:
            return [_hash_vector(t, self.dim) for t in texts]
        prefix = ("query: " if query else "passage: ") if self.e5 else ""
        return [v.tolist() for v in self.model.embed([prefix + t for t in texts])]


def _hash_vector(text: str, dim: int) -> list[float]:
    """Offline stand-in embedding (hashed stems and char trigrams). Weak semantically; for testing."""
    v = np.zeros(dim, dtype=np.float32)
    for tok in tokenize(text):
        for gram in [tok] + [tok[i : i + 3] for i in range(len(tok) - 2)]:
            h = zlib.crc32(gram.encode())
            v[h % dim] += 1.0 if (h >> 16) & 1 else -1.0
    norm = np.linalg.norm(v)
    return (v / norm if norm else v).tolist()


def _index(token: str) -> int:
    return zlib.crc32(token.encode()) & 0x7FFFFFFF


class BM25:
    """Document side of BM25. Qdrant adds the IDF part (Modifier.IDF)."""

    k1, b = 1.2, 0.75

    def __init__(self, texts: list[str]):
        self.avgdl = sum(len(tokenize(t)) for t in texts) / max(1, len(texts)) or 1.0

    def doc(self, text: str) -> SparseVector:
        tokens = tokenize(text)
        tf = Counter(tokens)
        norm = self.k1 * (1 - self.b + self.b * len(tokens) / self.avgdl)
        return SparseVector(indices=[_index(t) for t in tf],
                            values=[f * (self.k1 + 1) / (f + norm) for f in tf.values()])

    @staticmethod
    def query(text: str) -> SparseVector | None:
        terms = sorted(set(query_terms(text)))
        return SparseVector(indices=[_index(t) for t in terms], values=[1.0] * len(terms)) if terms else None