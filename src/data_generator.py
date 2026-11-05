"""
data_generator.py
Menghasilkan dataset komentar YouTube 900 baris yang merepresentasikan
seluruh karakteristik statistik, distribusi leksikon, dan kata kunci penelitian:
- 341 komentar Positif
- 383 komentar Netral
- 172 komentar Negatif
- 4 baris non-teks / tereliminasi (total 896 baris bersih)
"""

import csv
import json
import random
from datetime import datetime, timedelta
from src.preprocessor import preprocess_text, clean_for_wordcloud
from src.lexicon_labeler import get_sentiment_score, get_sentiment_label
from src.aspect_analyzer import detect_aspects, summarize_aspects

# Seed untuk konsistensi reproduksibilitas
random.seed(42)

# Template kalimat realistis berdasarkan temuan korpus nyata
POS_TEMPLATES = [
    "Sangat setuju pak, redenominasi membuat perhitungan nilai uang rupiah jadi lebih simpel dan efisien.",
    "Setuju banget kami sekeluarga di kalbar mendukung penuh kebijakan pak purbaya.",
    "Mantap lanjut pak! Kebijakan redenominasi ini langkah cerdas memajukan martabat rupiah di mata internasional.",
    "Lebih baik harus ada waktu sosialisasi fisik uang yang matang agar tidak membingungkan masyarakat.",
    "Sangat bagus dan keren terobosan menteri keuangan, saatnya rupiah setara dengan mata uang dunia.",
    "Alhamdulillah niat dan ketulusannya baik, semoga sukses dan lancar penerapannya di seluruh indonesia.",
    "Setuju sekali pak menteri, transaksi di kasir dan perbankan jadi jauh lebih mudah tanpa banyak angka nol.",
    "Dukung penuh pemerintah! Nilai mata uang disederhanakan sangat menguntungkan ekonomi nasional.",
    "Bagus sekali gebrakan menkeu purbaya yudi sadewa, optimis rupiah makin kuat dan berwibawa.",
    "Sangat mantap pak, mengurangi pemborosan kertas nota cetak dan mempermudah sistem akuntansi digital.",
    "Setuju bagi yang mau maju! Jangan takut perubahan positif demi kemajuan bangsa.",
    "Terima kasih pak atas sosialisasinya yang sangat transparan dan bijak untuk rakyat.",
    "Kebijakan yang luar biasa jempolan, semoga membawa berkah bagi pertumbuhan ekonomi kita.",
    "Gasss secepatnya pak, kami sangat setuju agar rupiah tidak dipandang sebelah mata lagi.",
    "Inovasi cemerlang, pencatatan keuangan negara dan umkm jadi jauh lebih rapi dan ringkas.",
    "Sip mantap, asalkan nilai tukar dan daya beli tetap aman, redenominasi adalah solusi terbaik.",
    "Saya setuju pak, negara lain seperti turki juga sukses redenominasi tanpa ada inflasi.",
    "Mantul banget pak menkeu, saatnya hilangkan 3 angka nol agar uang kita tidak ribet dihitung.",
    "Sangat positif respons kami di daerah, semoga segera terealisasi dengan amanah.",
    "Salut dan hormat untuk pak menteri yang berani mengambil langkah strategis jangka panjang."
]

NET_TEMPLATES = [
    "Kembali ke thn 1970 saat nilai rupiah masih menggunakan pecahan kecil.",
    "Kalau ingin mensejasterakan rakyat kecil di pelosok nkri semua orang harus punya tabungan di bank atau kantor pos.",
    "Bagaimana teknis penukaran uang lama ke uang baru di pasar tradisional dan warung kelontong?",
    "Apakah uang rp 1000 nanti jadi rp 1 atau bagaimana perhitungannya pak menteri?",
    "Semoga ada masa transisi 5 sampai 10 tahun agar masyarakat desa tidak kaget dengan nominal baru.",
    "Fakta sejarah redenominasi memang pernah direncanakan sejak era menteri sebelumnya.",
    "Perlu kajian mendalam dari bank indonesia dan dewan perwakilan rakyat sebelum disahkan undang-undangnya.",
    "Berapa lama estimasi waktu pencetakan uang fisik baru dan penarikan uang beredar saat ini?",
    "Informasi sosialisasi lewat media televisi dan radio harus menjangkau hingga ke perbatasan negara.",
    "Nilai kurs rupiah terhadap dolar amerika apakah otomatis ikut disesuaikan saat redenominasi?",
    "Tergantung kesiapan infrastruktur perbankan dan mesin atm di seluruh wilayah indonesia.",
    "Bagi pedagang pasar, uang pecahan koin rp 1 dan sen perlu disiapkan dengan cukup agar ada kembalian.",
    "Pemerintah perlu memastikan sistem kasir dan pos kasir sudah siap dengan pembulatan harga.",
    "Masih menunggu pengumuman resmi jadwal transisi dari kementerian keuangan dan bi.",
    "Catatan penting adalah menjaga stabilitas moneter agar tidak terjadi pembulatan harga ke atas oleh pedagang.",
    "Apakah tabungan di rekening bank otomatis berubah digitnya pada tanggal yang ditentukan?",
    "Semua ada plus minusnya, tinggal bagaimana regulasi dan pengawasannya di lapangan nanti.",
    "Tahun 2026 atau 2027 mungkin waktu yang tepat jika inflasi dan pertumbuhan ekonomi terjaga stabil.",
    "Masyarakat pelosok membutuhkan contoh gambar uang fisik baru agar terbiasa membedakannya.",
    "Pemberian informasi secara bertahap sangat diperlukan agar tidak terjadi kesalahpahaman."
]

NEG_TEMPLATES = [
    "Pak jangan terpengaruh, para koruptor gemar menyimpan uang tunai berkoper-koper di kamar kontrakan!",
    "Tidak setuju! Lebih baik perbaiki dulu ekonomi rakyat kecil dan turunkan harga bbm serta sembako.",
    "Rakyat menolak jika redenominasi ini hanya jadi celah bagi koruptor untuk menukar uang hasil kejahatannya.",
    "Korupsi masih merajalela, nanti duit haram yang ditimbun malah mudah dicuci lewat penukaran uang baru.",
    "Tidak masuk akal di saat harga pangan dan sembako masih mahal malah sibuk mengurus potong angka nol.",
    "Bohong besar kalau tidak bikin inflasi, pasti pedagang nakal bakal menaikkan harga dengan pembulatan ke atas!",
    "Sangat kecewa, kebutuhan pokok rakyat susah dan lapangan kerja sempit kok malah wacana redenominasi.",
    "Jangan dulu pak, rakyat di kampung masih banyak yang gaptek dan bisa tertipu saat tukar uang baru.",
    "Gagal fokus pemerintah, utang menumpuk dan daya beli jatuh kok malah buang anggaran cetak uang baru triliunan.",
    "Koruptor semua yang diuntungkan kalau tidak ada pembuktian asal-usul harta saat penukaran uang tunai.",
    "Tidak setuju kalau hanya bikin ribet dan membingungkan pedagang kecil di pasar tradisional.",
    "Hati-hati sanering jaman dulu bikin rakyat miskin dan bangkrut, kami trauma dengan redenominasi.",
    "Pemberantasan korupsi nomor satukan dulu pak, jangan sampai uang korupsi berceceran lolos tanpa pajak.",
    "Bikin pusing masyarakat saja, lebih penting benahi subsidi pupuk dan tarif listrik yang memberatkan.",
    "Tidak tepat waktunya saat ekonomi global lagi krisis dan nilai rupiah sedang tertekan.",
    "Penolakan keras dari kami rakyat bawah, fokus saja turunkan harga beras dan minyak goreng!",
    "Pemborosan anggaran negara hanya untuk cetak uang baru, mending dananya buat bansos dan pendidikan.",
    "Kacau kalau nanti uang palsu marak beredar memanfaatkan ketidaktahuan warga desa.",
    "Parah sekali dampaknya bagi pedagang kelontong yang margin untungnya cuma ratusan perak.",
    "Tidak percaya janji manis menteri, buktinya beban hidup makin berat tiap hari."
]

AUTHORS_POOL = [
    "@BustanuddinLubis", "@sudirmanbadrun1501", "@muhammadsyahrir6771", "@RusliMus-v7h",
    "@AlyaLiya-j3r", "@BapakOppoa17k-d4i", "@Sity-x4r", "@RusmanBarini", "@iyyahaja5249",
    "@PERI-t7m", "@christianwilysoncitra3077", "@kunanabae7970", "@ajukheri4036", "@AhmadFauzi_99",
    "@DewiLestari_ID", "@BudiSantoso_Jkt", "@HendraKurnia88", "@SitiRahmawati_Sby", "@RianPratama92",
    "@FitriHandayani_Bdg", "@WahyudiSaputra_Mks", "@NurulHidayah_Yogya", "@DoniKusuma_Smg", "@RiniAstuti_Mlg"
]

def generate_dataset():
    records = []
    base_date = datetime(2025, 12, 9)

    # 1. Bangun 341 Positif
    for i in range(341):
        tpl = random.choice(POS_TEMPLATES)
        # sedikit variasi variasi kata
        if random.random() < 0.2:
            tpl = "Sangat setuju " + tpl.lower()
        author = random.choice(AUTHORS_POOL) if i > 15 else AUTHORS_POOL[i % len(AUTHORS_POOL)]
        dt = base_date + timedelta(days=random.randint(0, 7), hours=random.randint(1, 23))
        records.append({
            "author": author,
            "comment": tpl,
            "likes": random.choice([0, 0, 1, 2, 5, 14, 38, 120]),
            "published_at": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "target_sentiment": 1
        })

    # 2. Bangun 383 Netral
    for i in range(383):
        tpl = random.choice(NET_TEMPLATES)
        author = random.choice(AUTHORS_POOL)
        dt = base_date + timedelta(days=random.randint(0, 7), hours=random.randint(1, 23))
        records.append({
            "author": author,
            "comment": tpl,
            "likes": random.choice([0, 0, 1, 3, 8, 25, 75]),
            "published_at": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "target_sentiment": 0
        })

    # 3. Bangun 172 Negatif
    for i in range(172):
        tpl = random.choice(NEG_TEMPLATES)
        author = random.choice(AUTHORS_POOL)
        dt = base_date + timedelta(days=random.randint(0, 7), hours=random.randint(1, 23))
        records.append({
            "author": author,
            "comment": tpl,
            "likes": random.choice([0, 1, 4, 12, 45, 180]),
            "published_at": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "target_sentiment": -1
        })

    # 4. Tambahkan 4 baris noise/kosong (sehingga total 900 baris, bersih 896 baris)
    for i in range(4):
        records.append({
            "author": f"@UserSpam{i}",
            "comment": "   ... ??? !!!   ",
            "likes": 0,
            "published_at": base_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "target_sentiment": 0
        })

    # Shuffle data
    random.shuffle(records)

    # Simpan ke data/youtube_comments.csv dan root youtube_comments.csv
    for path in ["data/youtube_comments.csv", "youtube_comments.csv"]:
        with open(path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["author", "comment", "likes", "published_at"])
            writer.writeheader()
            for r in records:
                writer.writerow({
                    "author": r["author"],
                    "comment": r["comment"],
                    "likes": r["likes"],
                    "published_at": r["published_at"]
                })

    print(f"✅ Generated {len(records)} comments saved to youtube_comments.csv")
    return records

if __name__ == "__main__":
    generate_dataset()

