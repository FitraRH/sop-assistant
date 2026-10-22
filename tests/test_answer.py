"""Pipeline tests with fake LLMs (no network, no API key, no model download)."""
import re
from pathlib import Path

import pytest

from sop_assistant.answer import NOT_FOUND, Assistant
from sop_assistant.config import Settings
from sop_assistant.embeddings import DenseEmbedder
from sop_assistant.extract import extract_sections
from sop_assistant.store import index, make_client

PDFS = Path(__file__).resolve().parents[1] / "data" / "pdfs"


class FakeLLM:
    """Replies with a fixed JSON. `pick` is a regex: the evidence is the first sentence id whose text matches it."""

    def __init__(self, status="answered", answer="x", pick=None, missing=""):
        self.reply = dict(status=status, answer=answer, missing=missing)
        self.pick = pick

    def complete_json(self, system, user):
        assert "<kutipan>" in user and "HANYA" in system
        m = re.search(rf"(C\d+\.\d+): [^\n]*{self.pick}", user) if self.pick else None
        return {**self.reply, "evidence": [m.group(1)] if m else ["C99.9"]}


class Boom:
    def complete_json(self, *args):
        raise TimeoutError("down")


@pytest.fixture(scope="module")
def bot(tmp_path_factory):
    s = Settings(qdrant_path=str(tmp_path_factory.mktemp("qdrant")), embed_backend="hash", pdf_dir=PDFS)
    index(make_client(s), s, [x for p in sorted(PDFS.glob("*.pdf")) for x in extract_sections(p)], DenseEmbedder(s))
    return Assistant(s)


def test_all_sections_extracted():
    assert [len(extract_sections(p)) for p in sorted(PDFS.glob("*.pdf"))] == [8, 8, 8, 8]
    text = " ".join(x.text for x in extract_sections(sorted(PDFS.glob("*.pdf"))[0]))
    assert "tiket P1 yang memerlukan konfirmasi eksplisit" in text  # scan + 2 columns + OCR code repair


def test_valid_answer_keeps_verbatim_citation(bot):
    bot.llm = FakeLLM(answer="Setelah dikonfirmasi atau dua hari kerja tanpa tanggapan.", pick="dua hari kerja")
    a = bot.ask("Kapan tiket bisa ditutup?")
    assert a.status == "answered" and a.mode == "llm"
    assert a.citations[0].section == "7" and "dua hari kerja" in a.citations[0].quote


def test_unknown_evidence_id_is_refused(bot):
    bot.llm = FakeLLM()
    assert bot.ask("Kapan tiket bisa ditutup?").status == "not_found"


def test_fabricated_number_is_refused(bot):
    bot.llm = FakeLLM(answer="Tiket ditutup setelah 45 hari.", pick="dua hari kerja")
    a = bot.ask("Kapan tiket bisa ditutup?")
    assert a.status == "not_found" and "angka" in a.reason


def test_llm_not_found_is_honoured(bot):
    bot.llm = FakeLLM(status="not_found")
    assert bot.ask("Berapa batas waktu penyelesaian tiket P1?").answer == NOT_FOUND


def test_partial_adds_missing_note(bot):
    bot.llm = FakeLLM(status="partial", answer="Respons awal P1 adalah 15 menit.", pick="P1: 15 menit", missing="waktu penyelesaian")
    a = bot.ask("Berapa respons dan penyelesaian tiket P1?")
    assert a.status == "partial" and "waktu penyelesaian" in a.answer


def test_llm_error_falls_back_to_extractive(bot):
    bot.llm = Boom()
    a = bot.ask("Berapa target respons awal untuk tiket P1?")
    assert a.status == "answered" and a.mode == "extractive" and "LLM gagal" in a.reason


@pytest.mark.parametrize("question", ["Berapa target respons awal untuk tiket P5?", "Bagaimana prosedur pengajuan cuti karyawan?"])
def test_gates_refuse_before_the_llm(bot, question):
    bot.llm = Boom()  # would show "LLM gagal" if it were called
    a = bot.ask(question)
    assert a.status == "not_found" and a.mode == "gate"
    assert "P1" in a.answer or a.answer == NOT_FOUND