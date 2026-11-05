"""
lexicon_labeler.py
Pemberian label sentimen berbasis leksikon aturan (rule-based lexicon scoring)
dengan penanganan frasa multi-kata, negasi, dan pembobotan polaritas.
"""

from typing import Tuple, Dict, Any, List
from src.dictionaries import positive_phrases, negative_phrases, positive_words, negative_words

def get_sentiment_score(text: str) -> int:
    """
    Menghitung skor sentimen:
     1 = Positif
     0 = Netral
    -1 = Negatif
    """
    text = str(text).lower()

    # 1. Frasa negatif prioritas tertinggi
    for phrase in negative_phrases:
        if phrase in text:
            return -1

    # 2. Frasa positif prioritas tertinggi
    for phrase in positive_phrases:
        if phrase in text:
            return 1

    # 3. Deteksi "tidak / bukan / jangan + kata positif" -> menjadi Negatif
    words = text.split()
    negation_found = False
    for i in range(len(words) - 1):
        if words[i] in ["tidak", "bukan", "jangan"]:
            if words[i + 1] in positive_words:
                negation_found = True
                break

    if negation_found:
        return -1

    # 4. Hitung skor kata
    score = 0
    for w in words:
        if w in positive_words:
            score += 1
        elif w in negative_words:
            score -= 1

    # 5. Threshold klasifikasi
    if score >= 1:
        return 1
    elif score <= -1:
        return -1
    else:
        return 0

def get_sentiment_label(score: int) -> str:
    """Mengubah nilai numerik (-1, 0, 1) menjadi label teks."""
    if score == 1:
        return "Positif"
    elif score == -1:
        return "Negatif"
    return "Netral"

def analyze_sentiment_detail(text: str) -> Dict[str, Any]:
    """
    Analisis mendalam mengapa sebuah teks mendapatkan sentimen tertentu.
    Sangat berguna untuk fitur 'Live Tester' di dashboard.
    """
    text_lower = str(text).lower()
    matched_pos_phrases = [p for p in positive_phrases if p in text_lower]
    matched_neg_phrases = [p for p in negative_phrases if p in text_lower]

    words = text_lower.split()
    matched_pos_words = [w for w in words if w in positive_words]
    matched_neg_words = [w for w in words if w in negative_words]

    negations = []
    for i in range(len(words) - 1):
        if words[i] in ["tidak", "bukan", "jangan"] and words[i + 1] in positive_words:
            negations.append(f"{words[i]} {words[i+1]}")

    score = get_sentiment_score(text)
    label = get_sentiment_label(score)

    return {
        "score": score,
        "label": label,
        "matched_positive_phrases": matched_pos_phrases,
        "matched_negative_phrases": matched_neg_phrases,
        "matched_positive_words": matched_pos_words,
        "matched_negative_words": matched_neg_words,
        "negation_flips": negations
    }

