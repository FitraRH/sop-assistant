# Hasil Evaluasi

Konfigurasi: embedding=hash, llm=qwen2.5:3b-instruct

## Set questions
- Status benar: 17/19
- Dalam cakupan: bagian benar ditemukan 13/13, dikutip 12/13, fakta kunci lengkap 10/13
- Di luar cakupan: ditolak dengan benar 5/6

| ID | Kategori | Harapan → Hasil | Ditemukan | Dikutip | Fakta |
|---|---|---|---|---|---|
| Q01 | answerable | answered → answered (benar) | ya | ya | ya |
| Q02 | answerable | answered → answered (benar) | ya | ya | ya |
| Q03 | answerable | answered → answered (benar) | ya | ya | ya |
| Q04 | answerable | answered → answered (benar) | ya | ya | ya |
| Q05 | answerable (2-kolom, kolom kanan) | answered → answered (benar) | ya | ya | ya |
| Q06 | answerable (scan + 2-kolom, kolom kanan) | answered → answered (benar) | ya | ya | ya |
| Q07 | answerable (scan) | answered → answered (benar) | ya | ya | ya |
| Q08 | ambigu / lintas dokumen | answered/partial → answered (benar) | ya | ya | tidak |
| Q09 | ambigu (kurang spesifik) | answered/partial → answered (benar) | ya | ya | tidak |
| Q10 | jebakan (mirip tapi beda) | answered → answered (benar) | ya | ya | ya |
| Q11 | lintas dokumen | answered → answered (benar) | ya | ya | ya |
| Q12 | jebakan (mirip tapi beda) | answered → not_found (salah) | ya | tidak | tidak |
| Q13 | sinonim / serapan | answered → answered (benar) | ya | ya | ya |
| Q14 | di luar cakupan | not_found → not_found (benar) | - | - | - |
| Q15 | di luar cakupan | not_found → not_found (benar) | - | - | - |
| Q16 | di luar cakupan (jauh) | not_found → not_found (benar) | - | - | - |
| Q17 | jebakan (entitas tidak ada) | not_found/partial → not_found (benar) | - | - | - |
| Q18 | jebakan (info tidak tercantum) | not_found/partial → answered (salah) | - | - | - |
| Q19 | jebakan (topik dekat) | not_found/partial → not_found (benar) | - | - | - |

## Set holdout
- Status benar: 7/8
- Dalam cakupan: bagian benar ditemukan 5/5, dikutip 4/5, fakta kunci lengkap 4/5
- Di luar cakupan: ditolak dengan benar 3/3

| ID | Kategori | Harapan → Hasil | Ditemukan | Dikutip | Fakta |
|---|---|---|---|---|---|
| H01 | holdout answerable | answered → answered (benar) | ya | ya | ya |
| H02 | holdout answerable (scan) | answered → answered (benar) | ya | ya | ya |
| H03 | holdout answerable (2-kolom) | answered → answered (benar) | ya | ya | ya |
| H04 | holdout answerable (scan) | answered → answered (benar) | ya | ya | ya |
| H05 | holdout lintas dokumen | answered/partial → not_found (salah) | ya | tidak | tidak |
| H06 | holdout luar cakupan | not_found → not_found (benar) | - | - | - |
| H07 | holdout luar cakupan (kosakata dekat) | not_found → not_found (benar) | - | - | - |
| H08 | holdout luar cakupan (kosakata dekat) | not_found/partial → not_found (benar) | - | - | - |

## Jawaban lengkap

**Q01. Berapa target respons awal untuk tiket P1?** (answered, llm)

Target respons awal untuk tiket P1 adalah 15 menit.

**Q02. Apa saja status tiket yang digunakan?** (answered, llm)

Status yang digunakan adalah Baru, Diproses, Menunggu Pelanggan, Menunggu Pihak Ketiga, Selesai, dan Ditutup.

**Q03. Paling lambat kapan sebuah keluhan harus diakui setelah diterima?** (answered, llm)

Paling lambat satu hari kerja sejak diterima.

**Q04. Kapan jam layanan reguler beroperasi?** (answered, llm)

Jam layanan reguler beroperasi Senin sampai Jumat pukul 09.00-17.00 WIB.

**Q05. Apa yang harus dilakukan jika sistem tiket tidak tersedia?** (answered, llm)

Jika sistem tiket tidak tersedia, catat laporan dalam formulir sementara dengan waktu asli penerimaan.

**Q06. Kapan tiket bisa ditutup, dan apa pengecualian untuk P1?** (answered, llm)

Tiket bisa ditutup setelah penyelesaian dikonfirmasi pelanggan atau setelah dua hari kerja tanpa tanggapan sejak notifikasi selesai. Pengecualian untuk tiket P1 adalah mereka memerlukan konfirmasi eksplisit.

**Q07. Berapa batas waktu penyusunan tinjauan pascainsiden?** (answered, llm)

Tinjauan pascainsiden harus disusun paling lambat lima hari kerja setelah pemulihan.

**Q08. Berapa menit sekali update harus diberikan saat ada gangguan?** (answered, llm)

Pembaruan tiket P1 harus diberikan setiap 30 menit selama gangguan aktif.

**Q09. Berapa lama waktu respons?** (answered, llm)

Respons awal berarti petugas telah mengakui laporan dan menyampaikan langkah berikutnya, bukan bahwa masalah sudah selesai.

**Q10. Apakah keluhan berulang otomatis menjadi insiden P1?** (answered, llm)

Keluhan berulang tidak otomatis menjadi insiden P1; penentuan prioritas mengikuti dampak aktual.

**Q11. Jika ada dugaan kebocoran data, apa yang harus dilakukan?** (answered, llm)

Jika ada dugaan kebocoran data, akses harus segera dibatasi dan dicatat melalui kanal keamanan.

**Q12. Kalau insiden sudah pulih, apakah semua tiket pelanggan otomatis ditutup?** (not_found, llm)

Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP yang tersedia. Saya tidak ingin menebak. Silakan hubungi koordinator layanan atau pemilik dokumen.

Catatan: model menilai dokumen tidak memuat jawabannya

**Q13. Apakah petugas boleh menjanjikan refund ke pelanggan?** (answered, llm)

Petugas tidak boleh menjanjikan pengembalian dana atau kompensasi sebelum ada persetujuan pejabat berwenang.

**Q14. Berapa gaji petugas layanan?** (not_found, llm)

Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP yang tersedia. Saya tidak ingin menebak. Silakan hubungi koordinator layanan atau pemilik dokumen.

Catatan: model menilai dokumen tidak memuat jawabannya

**Q15. Bagaimana prosedur pengajuan cuti karyawan?** (not_found, gate)

Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP yang tersedia. Saya tidak ingin menebak. Silakan hubungi koordinator layanan atau pemilik dokumen.

Catatan: kata kunci pertanyaan tidak ditemukan di dokumen

**Q16. Siapa presiden Indonesia saat ini?** (not_found, llm)

Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP yang tersedia. Saya tidak ingin menebak. Silakan hubungi koordinator layanan atau pemilik dokumen.

Catatan: model menilai dokumen tidak memuat jawabannya

**Q17. Berapa target respons awal untuk tiket P5?** (not_found, gate)

Kode P5 tidak ditemukan dalam dokumen SOP. Kode yang tersedia: P1, P2, P3, P4.

**Q18. Berapa lama batas waktu penyelesaian (resolusi) tiket P1?** (answered, llm)

Batas waktu penyelesaian tiket P1 adalah 2 hari kerja.

**Q19. Bagaimana cara mereset password akun pelanggan?** (not_found, llm)

Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP yang tersedia. Saya tidak ingin menebak. Silakan hubungi koordinator layanan atau pemilik dokumen.

Catatan: model menilai dokumen tidak memuat jawabannya

**H01. Siapa yang menetapkan PIC utama jika penyelesaian keluhan butuh keputusan lintas tim?** (answered, llm)

PIC utama ditetapkan oleh koordinator layanan.

**H02. Apa tugas koordinator insiden?** (answered, llm)

Koordinator insiden memimpin keputusan dan komunikasi lintas tim.

**H03. Bolehkah berkas pelanggan dibagikan lewat tautan publik?** (answered, llm)

Berkas pelanggan tidak boleh dibagikan melalui tautan publik.

**H04. Dalam berapa menit SEV2 harus dieskalasikan?** (answered, llm)

SEV2 harus dieskalasikan kepada penanggung jawab teknis paling lambat 30 menit sejak klasifikasi.

**H05. Apa bedanya tingkat P2 dengan SEV2?** (not_found, llm)

Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP yang tersedia. Saya tidak ingin menebak. Silakan hubungi koordinator layanan atau pemilik dokumen.

Catatan: model menilai dokumen tidak memuat jawabannya

**H06. Bagaimana cara memesan tiket pesawat untuk perjalanan dinas?** (not_found, gate)

Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP yang tersedia. Saya tidak ingin menebak. Silakan hubungi koordinator layanan atau pemilik dokumen.

Catatan: kata kunci pertanyaan tidak ditemukan di dokumen

**H07. Berapa biaya lisensi sistem tiket yang dipakai petugas?** (not_found, llm)

Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP yang tersedia. Saya tidak ingin menebak. Silakan hubungi koordinator layanan atau pemilik dokumen.

Catatan: model menilai dokumen tidak memuat jawabannya

**H08. Siapa nama koordinator insiden saat ini?** (not_found, llm)

Maaf, informasi tersebut tidak ditemukan dalam dokumen SOP yang tersedia. Saya tidak ingin menebak. Silakan hubungi koordinator layanan atau pemilik dokumen.

Catatan: model menilai dokumen tidak memuat jawabannya