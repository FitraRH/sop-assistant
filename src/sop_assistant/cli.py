"""CLI: ingest | inspect | ask | chat"""
import argparse
import sys
import warnings

from .answer import Assistant
from .config import Settings
from .embeddings import DenseEmbedder
from .extract import extract_sections, read_pages
from .store import index, make_client

warnings.filterwarnings("ignore")


def ingest(args) -> None:
    s = Settings()
    sections = []
    for pdf in sorted(s.pdf_dir.glob("*.pdf")):
        found = extract_sections(pdf)
        print(f"  {pdf.name}: {len(found)} section | {found[0].method} | {found[0].columns} kolom")
        sections += found
    if not sections:
        sys.exit(f"Tidak ada PDF di {s.pdf_dir}")
    n = index(make_client(s), s, sections, DenseEmbedder(s))
    print(f"Terindeks {n} section (embedding: {s.embed_model if s.embed_backend == 'fastembed' else 'hash'})")


def inspect(args) -> None:
    for pdf in sorted(Settings().pdf_dir.glob("*.pdf")):
        for no, text, method, columns in read_pages(pdf):
            print(f"===== {pdf.name} hlm.{no} | {method} | {columns} kolom =====\n{text}\n")


def ask(args) -> None:
    print(Assistant().ask(args.question).render(args.debug))


def chat(args) -> None:
    bot = Assistant()
    print("Tanya seputar SOP (ketik 'exit' untuk keluar).")
    try:
        while (q := input("\n> ").strip()) and q.lower() not in ("exit", "quit"):
            print("\n" + bot.ask(q).render(args.debug))
    except (EOFError, KeyboardInterrupt):
        pass


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(prog="sop_assistant")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ingest", help="ekstrak PDF dan indeks ke Qdrant").set_defaults(run=ingest)
    sub.add_parser("inspect", help="lihat teks hasil ekstraksi").set_defaults(run=inspect)
    for name, fn in (("ask", ask), ("chat", chat)):
        p = sub.add_parser(name)
        if name == "ask":
            p.add_argument("question")
        p.add_argument("--debug", action="store_true", help="tampilkan mode, coverage, dan keluaran mentah LLM")
        p.set_defaults(run=fn)
    args = parser.parse_args()
    args.run(args)