"""
preprocessor.py
Modul pembersihan, normalisasi kata gaul/slang, penghapusan stopword,
dan penyiapan teks untuk analisis sentimen & visualisasi wordcloud.
"""

import re
import string
import unicodedata
from src.dictionaries import normalisasi_dict, stopwords_indonesia, positive_phrases, negative_phrases

# Pola regex untuk emoji (standar unicode)
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U0001FA70-\U0001FAFF"
    "]+",
    flags=re.UNICODE
)

def remove_emoji(text: str) -> str:
    """Menghapus emoji menggunakan regex Unicode bawaan (tanpa dependensi eksternal)."""
    return EMOJI_PATTERN.sub(r'', text)

def remove_repeated_chars(text: str) -> str:
    """Mengurangi pengulangan huruf berlebih: 'bagussss' -> 'bagus', 'kerennnn' -> 'keren'."""
    return re.sub(r'(.)\1{2,}', r'\1', text)

def normalize_font(text: str) -> str:
    """
    Mengubah karakter Unicode fancy / bold / italic ke bentuk normal standar.
    Misal: 𝐛𝐚𝐠𝐮𝐬 -> bagus
    """
    try:
        return ''.join(unicodedata.normalize('NFKD', c) for c in text)
    except Exception:
        return text

def normalize_slang(text: str) -> str:
    """Mengubah kata-kata gaul/singkatan menjadi kata baku bahasa Indonesia."""
    words = text.split()
    normalized_words = [normalisasi_dict.get(w, w) for w in words]
    return " ".join(normalized_words)

def preprocess_text(text: str, remove_stop: bool = True) -> str:
    """
    Pipeline lengkap preprocessing teks komentar:
    1. Hapus HTML tag
    2. Hapus URL / Link
    3. Hapus Email
    4. Hapus imbuhan klitika (-nya, -lah, -kah, -pun)
    5. Hapus Emoji
    6. Normalisasi Font Fancy
    7. Lowercase
    8. Kurangi pengulangan karakter
    9. Normalisasi slang/singkatan
    10. Hapus tanda baca & angka tertentu
    11. Hapus stopwords (kecuali kata kunci sentimen)
    12. Hapus spasi berlebih
    """
    if text is None:
        return ""
    text = str(text)
    if not text.strip():
        return ""

    # 1. Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # 2. Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # 3. Remove Email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # 4. Hapus akhiran -nya, -lah, -kah, -pun
    text = re.sub(r'\b(\w+)(nya|lah|kah|pun)\b', r'\1', text)

    # 5. Remove Emojis
    text = remove_emoji(text)

    # 6. Normalize fancy fonts
    text = normalize_font(text)

    # 7. Convert to lowercase
    text = text.lower()

    # 8. Remove repeated characters
    text = remove_repeated_chars(text)

    # 9. Normalisasi kata gaul
    text = normalize_slang(text)

    # 10. Hapus tanda baca selain spasi
    text = re.sub(r'[' + re.escape(string.punctuation) + ']', ' ', text)

    # 11. Stopword filtering dengan proteksi sentimen
    if remove_stop:
        words = text.split()
        protected_words = {"tidak", "bukan", "jangan", "kurang", "belum"}
        for phrase in positive_phrases:
            protected_words.update(phrase.split())
        for phrase in negative_phrases:
            protected_words.update(phrase.split())

        filtered = [
            w for w in words
            if (w not in stopwords_indonesia) or (w in protected_words)
        ]
        text = " ".join(filtered)

    # 12. Hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_for_wordcloud(text: str) -> str:
    """Pembersihan khusus untuk tampilan WordCloud yang bersih dan relevan."""
    words_to_remove = {
        'uang', 'rupiah', 'indonesia', 'nya', 'yg', 'ini', 'itu',
        'di', 'ke', 'dari', 'dan', 'atau', 'pada', 'untuk', 'dengan',
        'tahun', 'thn', 'pak', 'menteri', 'keuangan', 'rp', 'ada',
        'bisa', 'akan', 'sudah', 'jadi', 'lebih', 'harus', 'kalau'
    }
    words = text.split()
    words = [w for w in words if w not in words_to_remove and len(w) > 2]
    return " ".join(words)

