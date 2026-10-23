# Hasil Demonstrasi

27 pertanyaan dijalankan dengan `python eval/run_eval.py` (LLM Qwen2.5 3B lewat Ollama, embedding hash). Hasil otomatis lengkap ada di `eval/results.md`. Setiap jawaban di chatbot juga menampilkan sumbernya (dokumen, halaman, bagian), di sini hanya teks jawabannya.

Penolakan memakai pesan standar: "Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP yang tersedia. Saya tidak ingin menebak. Silakan hubungi koordinator layanan atau pemilik dokumen."

Ringkasan penilaian saya: dari 18 pertanyaan yang jawabannya ada di dokumen, 12 benar, 3 kurang lengkap, 3 salah. Dari 9 pertanyaan yang tidak didukung dokumen, 8 ditolak dengan benar dan 1 dijawab karangan.

## 1. Bisa dijawab langsung

| ID | Pertanyaan | Jawaban chatbot | Penilaian |
|---|---|---|---|
| Q01 | Berapa target respons awal untuk tiket P1? | Target respons awal untuk tiket P1 adalah 15 menit. | Benar |
| Q02 | Apa saja status tiket yang digunakan? | Status yang digunakan adalah Baru, Diproses, Menunggu Pelanggan, Menunggu Pihak Ketiga, Selesai, dan Ditutup. | Benar |
| Q03 | Paling lambat kapan sebuah keluhan harus diakui setelah diterima? | Paling lambat satu hari kerja sejak diterima. | Benar |
| Q04 | Kapan jam layanan reguler beroperasi? | Jam layanan reguler beroperasi Senin sampai Jumat pukul 09.00-17.00 WIB. | Benar |
| Q05 | Apa yang harus dilakukan jika sistem tiket tidak tersedia? | Jika sistem tiket tidak tersedia, catat laporan dalam formulir sementara dengan waktu asli penerimaan. | Kurang lengkap: tidak menyebut memasukkan data kembali setelah sistem pulih |
| Q06 | Kapan tiket bisa ditutup, dan apa pengecualian untuk P1? | Tiket bisa ditutup setelah penyelesaian dikonfirmasi pelanggan atau setelah dua hari kerja tanpa tanggapan sejak notifikasi selesai. Pengecualian untuk tiket P1 adalah mereka memerlukan konfirmasi eksplisit. | Benar |
| Q07 | Berapa batas waktu penyusunan tinjauan pascainsiden? | Tinjauan pascainsiden harus disusun paling lambat lima hari kerja setelah pemulihan. | Benar |
| H01 | Siapa yang menetapkan PIC utama jika penyelesaian keluhan butuh keputusan lintas tim? | PIC utama ditetapkan oleh koordinator layanan. | Benar |
| H02 | Apa tugas koordinator insiden? | Koordinator insiden memimpin keputusan dan komunikasi lintas tim. | Benar |
| H03 | Bolehkah berkas pelanggan dibagikan lewat tautan publik? | Berkas pelanggan tidak boleh dibagikan melalui tautan publik. | Benar |
| H04 | Dalam berapa menit SEV2 harus dieskalasikan? | SEV2 harus dieskalasikan kepada penanggung jawab teknis paling lambat 30 menit sejak klasifikasi. | Benar |

## 2. Jebakan "mirip tapi beda", lintas dokumen, dan sinonim

| ID | Pertanyaan | Jawaban chatbot | Penilaian |
|---|---|---|---|
| Q10 | Apakah keluhan berulang otomatis menjadi insiden P1? | Keluhan berulang tidak otomatis menjadi insiden P1; penentuan prioritas mengikuti dampak aktual. | Benar |
| Q11 | Jika ada dugaan kebocoran data, apa yang harus dilakukan? | Jika ada dugaan kebocoran data, akses harus segera dibatasi dan dicatat melalui kanal keamanan. | Kurang lengkap: dokumen juga melarang mengunggah contoh data pribadi ke tiket umum |
| Q12 | Kalau insiden sudah pulih, apakah semua tiket pelanggan otomatis ditutup? | Ditolak (pesan standar). | Salah: dokumen menyatakan tidak otomatis (KB_04 bagian 7) |
| Q13 | Apakah petugas boleh menjanjikan refund ke pelanggan? | Petugas tidak boleh menjanjikan pengembalian dana atau kompensasi sebelum ada persetujuan pejabat berwenang. | Benar |
| H05 | Apa bedanya tingkat P2 dengan SEV2? | Ditolak (pesan standar). | Salah: dijelaskan di KB_01 bagian 3 dan KB_04 bagian 2 |

## 3. Ambigu

| ID | Pertanyaan | Jawaban chatbot | Penilaian |
|---|---|---|---|
| Q08 | Berapa menit sekali update harus diberikan saat ada gangguan? | Pembaruan tiket P1 harus diberikan setiap 30 menit selama gangguan aktif. | Kurang lengkap: tidak menyebut aturan SEV1 (pembaruan internal tiap 20 menit) |
| Q09 | Berapa lama waktu respons? | Respons awal berarti petugas telah mengakui laporan dan menyampaikan langkah berikutnya, bukan bahwa masalah sudah selesai. | Salah: tidak menyebut waktunya (P1 15 menit, P2 1 jam, P3 4 jam kerja, P4 1 hari kerja) |

## 4. Tidak didukung dokumen

| ID | Pertanyaan | Jawaban chatbot | Penilaian |
|---|---|---|---|
| Q14 | Berapa gaji petugas layanan? | Ditolak (pesan standar). | Benar |
| Q15 | Bagaimana prosedur pengajuan cuti karyawan? | Ditolak (pesan standar). | Benar |
| Q16 | Siapa presiden Indonesia saat ini? | Ditolak (pesan standar). | Benar |
| Q17 | Berapa target respons awal untuk tiket P5? | Kode P5 tidak ditemukan dalam dokumen SOP. Kode yang tersedia: P1, P2, P3, P4. | Benar |
| Q18 | Berapa lama batas waktu penyelesaian (resolusi) tiket P1? | Batas waktu penyelesaian tiket P1 adalah 2 hari kerja. | Salah: dokumen hanya mengatur target respons awal. "Dua hari kerja" tampaknya diambil dari aturan penutupan tiket |
| Q19 | Bagaimana cara mereset password akun pelanggan? | Ditolak (pesan standar). | Benar |
| H06 | Bagaimana cara memesan tiket pesawat untuk perjalanan dinas? | Ditolak (pesan standar). | Benar |
| H07 | Berapa biaya lisensi sistem tiket yang dipakai petugas? | Ditolak (pesan standar). | Benar |
| H08 | Siapa nama koordinator insiden saat ini? | Ditolak (pesan standar). | Benar |
