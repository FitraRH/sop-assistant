# Catatan Evaluasi

27 soal: `eval/questions.json` (19, dipakai saat menyetel) dan `eval/holdout.json` (8, ditulis setelahnya, tidak dipakai menyetel). `python eval/run_eval.py` menulis `eval/results.md` beserta konfigurasi yang dipakai. Isi soal: bisa dijawab, ambigu, lintas dokumen, jebakan "mirip tapi beda", dan di luar cakupan.

## Hasil

| Run | Status benar | Bagian benar dikutip (18 soal berjawaban) | Di luar cakupan ditolak (9) |
|---|---|---|---|
| 1. Qwen2.5 3B, bukti berupa kutipan teks | 20/27 | 10/18 | 9/9 |
| 2. Qwen2.5 3B, bukti berupa id kalimat | isi setelah menjalankan ulang | | |
| Tanpa LLM (offline, embedding hash) | 26/27 | 18/18 | 8/9 |

Bagian yang benar selalu masuk 6 hasil teratas pencarian (18/18) pada semua run.

## Berjalan baik

- Pencarian: PDF scan, dua kolom, dan kolom kanan terbaca benar dan ditemukan.
- Tidak ada jawaban karangan di luar cakupan pada run dengan LLM: gaji, cuti, kode P5, waktu resolusi, dan reset password semuanya ditolak.
- Pengecekan bukti menahan jawaban tak berdasar. Pertanyaan waktu resolusi P1 (Q18, dokumen hanya mengatur respons awal) dijawab keliru tanpa LLM, tetapi ditolak pada run dengan LLM.

## Gagal atau kurang baik

- **Penolakan keliru (run 1):** 7 dari 18 pertanyaan yang jawabannya ada ditolak (Q02, Q09, Q11, Q12, H02, H04, H05), semua dengan alasan "bukti tidak terverifikasi". Pencarian benar, yang gagal adalah verifikasi: model 3B sulit menyalin kutipan persis. Perbaikannya (id kalimat, run 2) belum terbukti sampai dijalankan ulang.
- **Sitasi tidak mendukung jawaban (H01):** jawaban benar ("koordinator layanan") tetapi mengutip KB_04 §4, bukan KB_02 §5. Pengecekan hanya memastikan kutipan ada di dokumen, bukan bahwa ia menjawab.
- **Jawaban terlalu singkat (Q08, Q09):** hanya "30 menit", tidak menyebut aturan SEV1 (20 menit) atau semua tingkat prioritas.
- **Tanpa LLM:** Q18 dijawab keliru dan Q08 hanya menampilkan satu dari dua aturan. Penyebab: gate berbasis kata tidak membedakan "respons" dari "resolusi".
- Set utama ikut dipakai menyetel sistem (sinonim, gate kode), jadi angkanya lebih optimis daripada holdout. Holdout hanya 8 soal.

## Prioritas perbaikan

1. Jalankan ulang dengan model lebih besar (API) agar jawaban lebih lengkap, dan ukur run 2.
2. Pemeriksa apakah kalimat bukti benar-benar menjawab (NLI atau LLM-judge) untuk menutup kasus seperti H01.
3. Perbanyak soal uji dan pisahkan set penyetelan dari set uji.
4. Dukungan tabel dan PDF multi-halaman, serta skor kepercayaan OCR.