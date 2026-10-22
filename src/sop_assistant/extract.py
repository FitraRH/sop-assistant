"""PDF to sections: text layer or OCR, two-column reading order, numbered-section chunking."""
import io
import re
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

import pymupdf
import numpy as np

MIN_WORDS = 15  # fewer words than this on a page = scan, use OCR
OCR_DPI = 300


class Word(NamedTuple):
    x0: float
    y0: float
    x1: float
    y1: float
    text: str

    @property
    def xc(self) -> float:
        return (self.x0 + self.x1) / 2

    @property
    def yc(self) -> float:
        return (self.y0 + self.y1) / 2

    @property
    def h(self) -> float:
        return self.y1 - self.y0


@dataclass
class Section:
    doc: str
    doc_title: str
    page: int
    number: str
    title: str
    text: str
    method: str  # "text" or "ocr"
    columns: int


# ---- words -----------------------------------------------------------------
def _ocr_lang() -> str:
    import pytesseract

    installed = set(pytesseract.get_languages(config=""))
    return "+".join(lang for lang in ("ind", "eng") if lang in installed) or "eng"


def _page_words(page: pymupdf.Page) -> tuple[list[Word], float, str]:
    """Words with boxes, page width and method. Falls back to OCR for scans."""
    words = [Word(*w[:5]) for w in page.get_text("words") if w[4].strip()]
    if len(words) >= MIN_WORDS:
        return words, page.rect.width, "text"
    import pytesseract
    from PIL import Image

    pix = page.get_pixmap(dpi=OCR_DPI)
    data = pytesseract.image_to_data(Image.open(io.BytesIO(pix.tobytes("png"))), lang=_ocr_lang(),
                                     config="--psm 11", output_type=pytesseract.Output.DICT)
    rows = zip(data["text"], data["conf"], data["left"], data["top"], data["width"], data["height"])
    words = [Word(x, y, x + w, y + h, t.strip()) for t, c, x, y, w, h in rows if t.strip() and float(c) >= 20]
    return words, pix.width, "ocr"


# ---- reading order ---------------------------------------------------------
def find_gutter(words: list[Word], width: float) -> float | None:
    """x of the gap between two columns, or None for a single-column page."""
    if len(words) < 30:
        return None
    cover = np.zeros(int(width) + 2, dtype=int)  # cover[x] = words crossing x
    for w in words:
        cover[max(0, int(w.x0)) : int(w.x1) + 1] += 1
    lo, hi = int(width * 0.30), int(width * 0.70)
    best, start = (0, 0), None
    for x in range(lo, hi + 2):
        if x <= hi and cover[x] <= 1:  # tolerate one stray word, e.g. a wide title
            start = x if start is None else start
        elif start is not None:
            best = max(best, (start, x), key=lambda r: r[1] - r[0])
            start = None
    if best[1] - best[0] < max(6, int(width * 0.015)):
        return None
    gutter = (best[0] + best[1]) / 2
    left = sum(w.xc < gutter for w in words)
    return gutter if min(left, len(words) - left) >= 0.15 * len(words) else None


def _lines(words: list[Word]) -> list[tuple[float, str]]:
    """Group words into (y, text) lines, top to bottom."""
    if not words:
        return []
    tol = 0.6 * statistics.median(w.h for w in words)
    rows: list[list[Word]] = []
    for w in sorted(words, key=lambda w: (w.yc, w.x0)):
        if rows and abs(w.yc - statistics.mean(r.yc for r in rows[-1])) <= tol:
            rows[-1].append(w)
        else:
            rows.append([w])
    return [(min(w.y0 for w in r), " ".join(w.text for w in sorted(r, key=lambda w: w.x0))) for r in rows]


def reading_order(words: list[Word], width: float) -> tuple[str, int]:
    """Text in human reading order and the column count (1 or 2)."""
    gutter = find_gutter(words, width)
    if gutter is None:
        return "\n".join(t for _, t in _lines(words)), 1
    crossing = [w for w in words if w.x0 < gutter - 2 and w.x1 > gutter + 2]
    # full width = crosses the gutter, or shares a row with a word that does (e.g. a big title)
    full = {w for w in words if any(c.y0 - 0.3 * c.h <= w.yc <= c.y1 + 0.3 * c.h for c in crossing)}
    left = _lines([w for w in words if w not in full and w.xc < gutter])
    right = _lines([w for w in words if w not in full and w.xc >= gutter])
    full_lines = _lines(list(full))
    bounds = [float("-inf")] + [y for y, _ in full_lines] + [float("inf")]
    out = []
    for i in range(len(bounds) - 1):  # left column, right column, then the full-width line below them
        for column in (left, right):
            out += [t for y, t in column if bounds[i] <= y < bounds[i + 1]]
        if i < len(full_lines):
            out.append(full_lines[i][1])
    return "\n".join(out), 2


def fix_ocr_codes(text: str) -> str:
    """Tesseract often misreads the 1 in codes like P1 / SEV1."""
    text = re.sub(r"\b(P|SEV)[lI|](?=[\s:;,.)]|$)", r"\g<1>1", text)
    return re.sub(r"\b(P|SEV)[Zz](?=[\s:;,.)]|$)", r"\g<1>2", text)


# ---- sections --------------------------------------------------------------
_HEADING = re.compile(r"^\s*(\d{1,2})\s*[.)]\s+([A-Za-z][^\n]{1,70}?)\s*$")
# OCR may misread the number glyph (e.g. "8." as "&."): accept only if plausible for the expected number
_LOOSE_HEADING = re.compile(r"^\s*(\S)\s*[.)]\s+([A-Z][^\n]{1,70}?)\s*$")
_CONFUSED = {"1": "lI|!", "2": "Zz", "3": "B", "4": "A", "5": "Ss", "6": "bG", "7": "T?", "8": "&BS%g", "9": "gq"}


def _heading(line: str, expected: int) -> tuple[str, str] | None:
    for pattern in (_HEADING, _LOOSE_HEADING):
        m = pattern.match(line)
        if not m or len(m.group(2).split()) > 7 or m.group(2).rstrip().endswith((".", ",", ";")):
            continue
        if pattern is _HEADING:
            return m.group(1), m.group(2).strip()
        if m.group(1) in _CONFUSED.get(str(expected), ""):
            return str(expected), m.group(2).strip()
    return None


def split_sections(doc: str, page: int, text: str, method: str, columns: int) -> list[Section]:
    lines = [l.strip() for l in text.splitlines() if l.strip() and not re.fullmatch(r"\d{1,3}", l.strip())]
    title: list[str] = []
    found: list[list] = []  # [number, title, body lines]
    for line in lines:
        h = _heading(line, len(found) + 1)
        if h:
            found.append([h[0], h[1], []])
        elif found:
            found[-1][2].append(line)
        else:
            title.append(line)
    doc_title = " ".join(title) or Path(doc).stem
    sections = [Section(doc, doc_title, page, n, t, " ".join(body), method, columns) for n, t, body in found if body]
    if not sections and lines:  # no headings: keep the page as one section
        sections = [Section(doc, doc_title, page, "-", doc_title, " ".join(lines), method, columns)]
    return sections


# ---- public ----------------------------------------------------------------
def read_pages(path: str | Path):
    """Yield (page_no, text, method, columns) for each page."""
    with pymupdf.open(path) as pdf:
        for no, page in enumerate(pdf, 1):
            words, width, method = _page_words(page)
            text, columns = reading_order(words, width)
            yield no, (fix_ocr_codes(text) if method == "ocr" else text), method, columns


def extract_sections(path: str | Path) -> list[Section]:
    name = Path(path).name
    return [s for no, text, method, cols in read_pages(path) for s in split_sections(name, no, text, method, cols)]