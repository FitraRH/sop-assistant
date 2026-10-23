# Catatan Evaluasi

27 soal di `eval/questions.json` (Q01-Q19 dan H01-H08). Semuanya sudah terlihat saat saya mengembangkan sistem, jadi hasil ini bukan uji independen. Konfigurasi: LLM Qwen2.5 3B (Ollama, lokal), embedding hash (model multilingual-e5 belum diuji). Daftar lengkap pertanyaan dan jawaban ada di `DEMO.md`, hasil otomatis di `eval/results.md`.

## Hasil

| Run | Status benar | Bagian benar dikutip (18 soal berjawaban) | Di luar cakupan ditolak (9) |
|---|---|---|---|
| 1. Qwen2.5 3B, bukti berupa kutipan teks | 20/27 | 10/18 | 9/9 |
| 2. Qwen2.5 3B, bukti berupa id kalimat (final) | 24/27 | 16/18 | 8/9 |
| Tanpa LLM (offline, embedding hash) | 26/27 | 18/18 | 8/9 |

Mode tanpa LLM skornya lebih tinggi karena hanya menampilkan potongan dokumen, tidak menyusun jawaban, jadi tidak setara. Bagian yang benar selalu masuk 6 hasil teratas pencarian (18/18).

Penilaian manual pada run 2 (lihat DEMO.md): dari 18 pertanyaan berjawaban, 12 benar penuh, 3 benar tapi kurang lengkap, 3 salah. Dari 9 pertanyaan di luar cakupan, 8 ditolak dengan benar.

## Berjalan baik

- Pencarian: PDF scan, dua kolom, dan kolom kanan terbaca benar dan ditemukan (18/18).
- Pertanyaan di luar topik (cuti, tiket pesawat) dan kode yang tidak ada (P5) ditolak sebelum masuk LLM.
- Mengganti bukti dari kutipan teks menjadi id kalimat menurunkan penolakan keliru dari 7 menjadi 2.
- Salah ketik dan istilah tidak baku ("refund", "update") tetap dijawab benar.

## Gagal atau kurang baik

- **Jawaban karangan (Q18):** "2 hari kerja" untuk waktu penyelesaian P1, padahal dokumen hanya mengatur respons awal. Angka itu tampaknya dari aturan penutupan tiket. Pada run 1 kasus ini tertahan, pada run 2 lolos karena pengecekan bukti hanya memeriksa angka 2 digit ke atas dan tidak memastikan kalimat bukti benar-benar menjawab. Perbaikan yang menurunkan penolakan keliru ikut membuka celah ini.
- **Tidak menjawab (Q09):** "Berapa lama waktu respons?" dijawab dengan arti respons awal, bukan waktunya per prioritas.
- **Kurang lengkap (Q05, Q08, Q11):** model 3B cenderung ringkas, misalnya hanya menyebut aturan P1 (30 menit) dan tidak SEV1 (20 menit).
- **Penolakan keliru (Q12, H05):** model menilai dokumen tidak memuat jawaban yang sebenarnya ada.
- Embedding hash lemah secara makna, model multilingual-e5 belum diuji, dan tidak ada uji independen.

## Prioritas perbaikan

1. Pemeriksa apakah kalimat bukti benar-benar menjawab pertanyaan (NLI atau LLM-judge), dan cek angka satu digit. Ini menutup kasus Q18.
2. Model lebih besar lewat API dan embedding e5-large, lalu ukur ulang.
3. Soal uji baru yang benar-benar terpisah dari proses pengembangan.
4. Dukungan tabel dan PDF multi-halaman, serta skor kepercayaan OCR.