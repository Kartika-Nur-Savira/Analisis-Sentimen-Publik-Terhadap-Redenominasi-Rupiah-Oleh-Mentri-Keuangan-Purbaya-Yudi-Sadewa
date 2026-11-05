"""
dictionaries.py
Kamus dan leksikon untuk preprocessing, normalisasi slang/gaul,
dan labeling sentimen bahasa Indonesia terkait isu redenominasi rupiah.
"""

normalisasi_dict = {
    # Angka → Huruf
    "se7": "setuju", "s7": "setuju", "4ku": "aku", "b4nget": "banget",

    # Kata gaul setuju
    "stju": "setuju", "stuju": "setuju", "tuju": "setuju", "suju": "setuju",
    "stj": "setuju", "setju": "setuju", "sujuuu": "setuju", "setujuuu": "setuju",
    "setu": "setuju", "stuju2": "setuju", "setujuu": "setuju", "s7uju": "setuju",
    "setujuuung": "setuju", "s7bgt": "setuju banget",

    # Kata gaul positif
    "bgt": "banget", "bngt": "banget", "bgtt": "banget", "bngtt": "banget",
    "mantul": "mantap", "mantep": "mantap", "mantab": "mantap", "mantappu": "mantap",
    "kren": "keren", "krenn": "keren", "kereen": "keren", "kereeen": "keren",
    "bgs": "bagus", "okeh": "oke", "cakep": "bagus", "kece": "bagus", "keceee": "bagus",
    "siip": "sip", "mantaap": "mantap", "topbgt": "top banget", "jos": "bagus",
    "joss": "bagus", "gokil": "keren", "mantull": "mantap",

    # Kata gaul negatif
    "jlek": "jelek", "jelekk": "jelek", "jelex": "jelek",
    "ancur": "rusak", "ancuurr": "rusak",
    "parah": "buruk", "prh": "buruk", "payah": "buruk",
    "bobrok": "rusak", "ambyar": "hancur", "ancur2an": "hancur",

    # Negasi (SANGAT PENTING)
    "gk": "tidak", "ga": "tidak", "gak": "tidak", "gx": "tidak",
    "nggak": "tidak", "enggak": "tidak", "kagak": "tidak", "kaga": "tidak",
    "g": "tidak", "ngga": "tidak", "ngg": "tidak",
    "gada": "tidak ada", "gaada": "tidak ada", "tak": "tidak",
    "tdk": "tidak", "ndak": "tidak", "ora": "tidak",

    # Kata ganti
    "gw": "saya", "gue": "saya", "ane": "saya", "w": "saya", "akuu": "aku",
    "lu": "kamu", "loe": "kamu", "elu": "kamu", "lo": "kamu", "ente": "kamu",
    "km": "kamu", "kalian": "kalian",

    # Kata sambung
    "tp": "tapi", "tpi": "tapi",
    "krn": "karena", "krna": "karena", "soalnya": "karena",
    "jd": "jadi", "jdi": "jadi", "jadinya": "jadi",
    "dgn": "dengan", "dg": "dengan", "ama": "dengan",
    "sm": "sama", "sma": "sama",

    # Kata keterangan & frekuensi
    "udh": "sudah", "udah": "sudah", "dah": "sudah", "sdh": "sudah",
    "blm": "belum", "blom": "belum", "blum": "belum", "belom": "belum",
    "emg": "memang", "emang": "memang", "mmg": "memang",
    "bnyk": "banyak", "byk": "banyak", "byak": "banyak",
    "dikit": "sedikit", "dkt": "sedikit", "hrs": "harus",
    "nolak": "tolak", "thn": "tahun",

    # Singkatan umum
    "yg": "yang", "yng": "yang",
    "utk": "untuk", "u": "untuk",
    "dr": "dari", "dri": "dari",
    "pd": "pada", "pda": "pada",
    "sgt": "sangat",

    # Kata tambahan
    "klo": "kalau", "kalo": "kalau", "klau": "kalau", "klu": "kalau",
    "gitu": "begitu", "gt": "begitu", "gtu": "begitu",
    "gini": "begini", "gni": "begini",
    "aja": "saja", "aj": "saja", "doang": "saja",
    "skrg": "sekarang", "skrang": "sekarang", "skr": "sekarang", "now": "sekarang",
    "kmrn": "kemarin", "kmren": "kemarin",
    "gmn": "bagaimana", "gimana": "bagaimana",
    "knp": "kenapa", "knpa": "kenapa",

    # Khusus kebijakan publik, politik & moneter
    "menkeu": "menteri keuangan", "menkue": "menteri keuangan",
    "pemerin7ah": "pemerintah", "pmrntah": "pemerintah",
    "mentri": "menteri", "mentr1": "menteri",
    "pjk": "pajak", "rkyt": "rakyat", "rakyaat": "rakyat",
    "korup": "koruptor", "korupsii": "korupsi",
    "redenom": "redenominasi", "redominasi": "redenominasi", "redom": "redenominasi",
    "duwit": "duit", "pissik": "fisik", "sosialisasikan": "sosialisasi",
    "duwid": "duit", "rp": "rupiah",

    # Respons chat
    "wkwk": "tertawa", "wkwkwk": "tertawa", "haha": "tertawa", "hehe": "tertawa"
}

positive_phrases = {
    "sangat setuju", "setuju sekali", "setuju banget", "saya setuju", "setuju pak",
    "sangat bagus", "bagus sekali", "bagus banget",
    "sangat mantap", "mantap sekali", "mantap banget", "mantap pak",
    "sangat baik", "baik sekali", "sangat keren", "keren sekali",
    "terima kasih", "terima kasih pak", "terima kasih banyak",
    "mendukung penuh", "sangat mendukung", "dukung penuh",
    "sangat positif", "hebat sekali", "luar biasa", "mantap lanjut pak",
    "setuju bget", "setuju bagi yang mau maju"
}

negative_phrases = {
    "tidak setuju", "ga setuju", "gak setuju", "enggak setuju",
    "tidak percaya", "ga percaya", "gak percaya",
    "tidak benar", "ga benar", "gak benar",
    "tidak masuk akal", "tidak sesuai", "tidak tepat",
    "tidak bagus", "ga bagus", "gak bagus",
    "tidak baik", "ga baik", "gak baik",
    "sangat buruk", "buruk sekali", "parah sekali", "parah banget",
    "sangat parah", "sangat jelek", "jelek sekali",
    "bohong semua", "bohong besar", "pembohong",
    "koruptor semua", "korupsi semua", "tidak ngaruh",
    "jangan redenominasi", "tidak ada gunanya", "bikin ribet"
}

positive_words = {
    # Persetujuan
    "setuju", "dukung", "mendukung", "approve", "yakin", "percaya", "tuju",
    "percepat", "gass", "gasss", "cocok", "secepat", "secepatnya",

    # Kualitas
    "bagus", "baik", "mantap", "hebat", "keren", "top", "terbaik",
    "super", "luar", "biasa", "istimewa", "berkualitas", "unggul",
    "cemerlang", "jempolan", "cakep", "oke", "ok", "menarik", "cepat",
    "hemat", "genius",

    # Perasaan positif
    "suka", "senang", "gembira", "bangga", "puas", "bahagia", "syukur",
    "terima", "kasih", "thanks", "apresiasi", "salut", "respect", "hormat",
    "sip", "alhamdulillah", "berkah",

    # Hasil positif
    "sukses", "berhasil", "lancar", "mudah", "efektif", "efisien",
    "menguntungkan", "untung", "naik", "meningkat", "maju", "positif",
    "simpel", "sederhana", "stabil", "kuat",

    # Karakter
    "pintar", "cerdas", "bijak", "jujur", "amanah", "transparan",
    "profesional", "kompeten", "ahli", "terampil",

    # Solusi
    "solusi", "bantu", "manfaat", "berguna", "inspirasi",
    "reformasi", "inovasi", "terobosan", "gebrakan", "perubahan"
}

negative_words = {
    # Penolakan
    "tolak", "menolak", "penolakan", "salah", "keliru", "melarang",

    # Kualitas buruk
    "buruk", "jelek", "parah", "gagal", "hancur", "rusak", "kacau",
    "berantakan", "fatal", "bahaya", "berbahaya", "merugikan",
    "sia", "percuma", "zonk", "mengecewakan", "wacana", "ribet", "negatif",
    "pusing", "bingung", "kacau", "boros", "pemborosan",

    # Perasaan negatif
    "kecewa", "kesal", "marah", "jengkel", "benci", "muak",
    "sedih", "susah", "sulit", "berat", "payah", "capek",

    # Moral & Korupsi
    "bohong", "pembohong", "dusta", "tipu", "menipu", "tertipu", "penipuan",
    "korup", "koruptor", "korupsi", "curang", "kecurangan", "jahat",
    "bodoh", "dungu", "tolol", "goblok", "haram",

    # Ekonomi & Beban
    "rugi", "kerugian", "bangkrut", "miskin", "mahal",
    "krisis", "resesi", "turun", "menurun", "jatuh", "inflasi",
    "sengsara", "beban",

    # Kritik
    "kritik", "protes", "demo", "menentang", "sampah", "busuk", "brengsek"
}

stopwords_indonesia = {
    'yang', 'untuk', 'pada', 'ke', 'di', 'dari', 'ini', 'itu', 'dengan', 'dan', 'atau',
    'karena', 'oleh', 'dalam', 'akan', 'sudah', 'bisa', 'ada', 'juga', 'hanya', 'saja',
    'harus', 'jadi', 'lebih', 'agar', 'supaya', 'seperti', 'antara', 'namun', 'tetapi',
    'kalau', 'jika', 'bila', 'ketika', 'saat', 'sebelum', 'sesudah', 'setelah', 'hingga',
    'sampai', 'sebab', 'makanya', 'maka', 'sehingga', 'lalu', 'kemudian', 'padahal',
    'sedangkan', 'meskipun', 'walaupun', 'biarpun', 'kendati', 'seolah', 'ibarat',
    'bagaikan', 'bak', 'umpama', 'lagipula', 'bahkan', 'malah', 'yaitu', 'yakni',
    'adalah', 'merupakan', 'ialah', 'bahwa', 'tentang', 'terhadap', 'mengenai',
    'secara', 'bagi', 'guna', 'demi', 'buat', 'daripada', 'daripadanya', 'selain',
    'kecuali', 'selama', 'sepanjang', 'seputar', 'sekitar', 'sebagai', 'selaku',
    'atas', 'bawah', 'dalam', 'luar', 'depan', 'belakang', 'samping', 'tengah',
    'antara', 'sini', 'situ', 'sana', 'mana', 'siapa', 'apa', 'kapan', 'kenapa',
    'mengapa', 'bagaimana', 'berapa', 'begitu', 'begini', 'demikian', 'kemari',
    'kesana', 'dimana', 'kemana', 'darimana', 'sungguh', 'benar', 'amat', 'terlalu',
    'makin', 'kian', 'bertambah', 'paling', 'kurang', 'cukup', 'agak', 'hampir',
    'nyaris', 'kira', 'kiranya', 'mungkin', 'pasti', 'tentu', 'memang', 'boleh',
    'dapat', 'mesti', 'wajib', 'hendak', 'mau', 'ingin', 'bakal', 'pernah',
    'sempat', 'senantiasa', 'selalu', 'sering', 'kerap', 'kadang', 'jarang',
    'belum', 'masih', 'sedang', 'tengah', 'lagi', 'pun', 'lah', 'kah', 'tah',
    'jua', 'dong', 'sih', 'deh', 'kan', 'kok', 'toh', 'lho', 'ya', 'wah',
    'aduh', 'hai', 'halo', 'nah', 'oh', 'ah', 'ih', 'cih', 'id', 'com',
    'org', 'net', 'co', 'html', 'php', 'url', 'https', 'http', 'www', 'rt',
    'user', 'amp', 'gt', 'lt'
}

# 4 Aspek Analisis Kebijakan
aspect_keywords = {
    "Pemberantasan Korupsi": [
        "koruptor", "korupsi", "kamar", "kontrakan", "simpan", "uang", "duit",
        "ditukar", "kpk", "hukum", "sembunyi", "buntel", "koper", "timbun"
    ],
    "Sosialisasi & Uang Fisik": [
        "sosialisasi", "fisik", "cetak", "model", "edar", "masyarakat", "pelosok",
        "daerah", "tahap", "transisi", "pasar", "bingung", "edukasi", "paham"
    ],
    "Kondisi Ekonomi & Harga": [
        "ekonomi", "bbm", "sembako", "harga", "pasar", "turunkan", "daya", "beli",
        "rakyat", "kecil", "miskin", "inflasi", "kebutuhan", "pokok", "gaji"
    ],
    "Martabat & Nilai Tukar Rupiah": [
        "nilai", "tukar", "rupiah", "mata", "uang", "dolar", "angka", "nol",
        "sederhana", "hitung", "internasional", "1970", "kuat", "wosterling"
    ]
}
