from sop_assistant.extract import Word, find_gutter, fix_ocr_codes, reading_order, split_sections


def column(x0, names, step=20):
    return [Word(x0, 100 + i * step, x0 + 60, 110 + i * step, n) for i, n in enumerate(names)]


def test_two_columns_read_left_then_right():
    left, right = [f"L{i}" for i in range(20)], [f"R{i}" for i in range(20)]
    text, cols = reading_order(column(50, left) + column(350, right), 600)
    assert cols == 2 and text.split() == left + right


def test_single_column_has_no_gutter():
    words = [Word(40 + (i % 8) * 65, 100 + (i // 8) * 20, 100 + (i % 8) * 65, 110 + (i // 8) * 20, f"w{i}") for i in range(48)]
    assert find_gutter(words, 600) is None


def test_full_width_title_stays_on_top():
    title = [Word(50, 40, 300, 70, "JUDUL"), Word(310, 40, 560, 70, "BESAR")]  # crosses the gutter
    text, _ = reading_order(title + column(50, [f"L{i}" for i in range(15)]) + column(350, [f"R{i}" for i in range(15)]), 600)
    assert text.split()[:2] == ["JUDUL", "BESAR"]


def test_ocr_code_repair_leaves_real_words():
    assert fix_ocr_codes("tiket Pl dan SEVl, SEV2") == "tiket P1 dan SEV1, SEV2"
    assert fix_ocr_codes("Plan baru") == "Plan baru"


def test_sections_and_ocr_heading_recovery():
    names = ["Satu", "Dua", "Tiga", "Empat", "Lima", "Enam", "Tujuh"]
    text = "Judul\n" + "\n".join(f"{i}. {n}\nisi {n}." for i, n in enumerate(names, 1)) + "\n&. Evaluasi Akhir\nisi akhir."
    secs = split_sections("x.pdf", 1, text, "ocr", 1)
    assert [s.number for s in secs][-1] == "8" and secs[-1].title == "Evaluasi Akhir"
    # '&' is not a plausible misread of 3, so it stays body text
    assert [s.number for s in split_sections("x.pdf", 1, "T\n1. Satu\na.\n2. Dua\nb.\n&. Tiga Palsu\nc.", "ocr", 1)] == ["1", "2"]