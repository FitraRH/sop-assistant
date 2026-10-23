# SOP Assistant

Tanya jawab atas dokumen SOP (PDF) dengan sitasi (dokumen, halaman, bagian) dan penolakan jujur bila jawabannya tidak ada. Python + Qdrant.

## Menjalankan

```bash
# 1. Tesseract (OCR untuk PDF scan)
winget install UB-Mannheim.TesseractOCR            # Windows
sudo apt install tesseract-ocr tesseract-ocr-ind   # Linux

# 2. Proyek
python -m venv .venv
.venv\Scripts\Activate.ps1                         # Linux/macOS: source .venv/bin/activate
pip install -e .
cp .env.example .env                               # lalu isi, lihat di bawah

# 3. Pakai
python -m sop_assistant ingest                     # baca PDF di data/pdfs, indeks ke Qdrant
python -m sop_assistant chat                       # atau: ask "Berapa target respons awal P1?"
python eval/run_eval.py                            # 27 soal uji, hasil di eval/results.md
pytest
```

Isi `.env` sesuai kebutuhan. `--debug` pada `ask`/`chat` menampilkan mode, coverage, dan keluaran mentah LLM. `inspect` menampilkan teks hasil ekstraksi.

| Mode | `.env` | Catatan |
|---|---|---|
| Cepat, offline | `EMBED_BACKEND=hash`, `LLM_*` kosong | Tanpa unduhan. Pencarian makna lemah. |
| Tanpa LLM | `EMBED_BACKEND=fastembed`, `LLM_*` kosong | Menampilkan bagian dokumen apa adanya. |
| Penuh | `fastembed` + `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` | Ollama, Groq, Gemini, atau endpoint kompatibel OpenAI lain. |

## Arsitektur

```
PDF ─► ada text layer? ─ya─► kata + posisi (PyMuPDF)
                      └tidak► OCR Tesseract ► kata + posisi ► perbaikan kode (Pl → P1)
        ─► deteksi 2 kolom, susun urutan baca ─► pecah per section bernomor (1 section = 1 chunk)
        ─► Qdrant: vektor dense (multilingual-e5) + sparse (BM25), metadata dokumen/halaman/bagian

Pertanyaan ─► hybrid search (RRF) ─► rerank kata ─► gate ─► LLM ─► cek bukti ─► jawaban + sumber
                                                     └ tolak: kata kunci tak ada di dokumen, atau kode tak dikenal (P5)
```

## Keputusan teknis

| Keputusan | Alasan | Alternatif yang tidak dipakai |
|---|---|---|
| 1 section bernomor = 1 chunk | Sitasi tepat dan angka tetap bersama konteksnya ("P1: 15 menit; P2: 1 jam"). | Potongan token tetap memecah aturan. Chunking semantik tidak perlu, dokumen sudah terstruktur. |
| Ambil kata + posisi, susun urutan kolom sendiri | Satu logika untuk PDF digital dan hasil OCR; dua kolom tidak tercampur. | Model layout (mis. Docling) lebih kuat untuk tabel dan 3 kolom, tapi berat dan berlebihan untuk dokumen sederhana ini. |
| OCR Tesseract | Gratis dan lokal. | OCR berbasis model atau vision LLM lebih akurat, tapi berbayar atau berat. |
| Hybrid dense + BM25 (RRF) | Istilah eksak (P1, "30 menit") unggul di BM25, parafrase di dense. | Dense saja kurang tajam untuk kode dan angka. |
| multilingual-e5-large | Mendukung Indonesia dan tersedia di fastembed tanpa API key. | bge-m3 tidak ada di daftar model fastembed yang saya periksa. MiniLM lebih ringan, tapi konteks 128 token bisa memotong section panjang. |
| LLM lewat API kompatibel OpenAI | Bebas pilih Ollama atau API lain tanpa ubah kode. | Model besar lebih patuh dan lengkap tapi butuh API key. Saya uji dengan Qwen2.5 3B lokal karena gratis. |
| Bukti = id kalimat dari dokumen, bukan kutipan buatan model | Model kecil sering salah menyalin kutipan (percobaan pertama: banyak penolakan keliru). Id mudah dicek dan kalimatnya ditampilkan persis dari dokumen. | Kutipan verbatim lebih ketat tapi rapuh. Pemeriksa NLI lebih tepat tapi butuh model tambahan. |
| Gate sebelum LLM (cakupan kata + kode tak dikenal) | Pertanyaan di luar topik ditolak tanpa biaya LLM. | Classifier terlatih lebih akurat tapi butuh data berlabel. |
| Tanpa LangChain/LlamaIndex | Alur pendek, mudah dibaca dan diaudit. | Framework berguna untuk sistem yang lebih besar. |

## Keterbatasan

- PDF contoh satu halaman, jadi sitasi selalu "hlm. 1". Pembeda sumbernya nomor bagian.
- Pengecekan bukti hanya memastikan id ada dan angka (2 digit ke atas) muncul di bukti. Ia tidak membuktikan kalimat bukti benar-benar menjawab pertanyaan. Contoh nyata: Q18 dijawab "2 hari kerja" padahal dokumen tidak mengatur waktu penyelesaian.
- Hasil uji memakai embedding hash dan Qwen2.5 3B. Model multilingual-e5-large belum diuji.
- Gate berbasis kata: salah ketik atau sinonim yang belum dipetakan bisa ditolak di mode tanpa LLM.
- OCR bisa salah baca kode pendek ("P1" jadi "Pl"). Sudah ditambal, pola lain mungkin ada.
- Belum ada tabel, memori percakapan, dan ingest inkremental.
- Kualitas jawaban bergantung model. Model 3B cenderung singkat dan sering menolak (lihat EVALUATION.md).