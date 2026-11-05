"""
aspect_analyzer.py
Analisis sentimen berbasis aspek (Aspect-Based Sentiment Analysis / ABSA).
Mengelompokkan opini publik ke dalam 4 pilar utama kebijakan moneter redenominasi rupiah:
1. Pemberantasan Korupsi
2. Sosialisasi & Uang Fisik
3. Kondisi Ekonomi & Harga
4. Martabat & Nilai Tukar Rupiah
"""

from typing import Dict, List, Any
from collections import Counter
from src.dictionaries import aspect_keywords

def detect_aspects(text: str) -> List[str]:
    """Mendeteksi aspek kebijakan yang relevan dalam satu komentar."""
    text_lower = text.lower()
    words = set(text_lower.split())
    matched_aspects = []

    for aspect_name, keywords in aspect_keywords.items():
        if any(kw in words or kw in text_lower for kw in keywords):
            matched_aspects.append(aspect_name)

    if not matched_aspects:
        matched_aspects.append("Umum / Lainnya")
    return matched_aspects

def summarize_aspects(df_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Menghitung distribusi sentimen per aspek dari kumpulan data komentar.
    """
    summary = {
        name: {"total": 0, "positif": 0, "netral": 0, "negatif": 0, "sample_comments": []}
        for name in list(aspect_keywords.keys()) + ["Umum / Lainnya"]
    }

    for item in df_records:
        comment = item.get("comment", "")
        sentiment = item.get("sentimen", 0)
        aspects = detect_aspects(comment)

        for asp in aspects:
            summary[asp]["total"] += 1
            if sentiment == 1:
                summary[asp]["positif"] += 1
            elif sentiment == -1:
                summary[asp]["negatif"] += 1
            else:
                summary[asp]["netral"] += 1

            if len(summary[asp]["sample_comments"]) < 3 and len(comment) > 20:
                summary[asp]["sample_comments"].append({
                    "comment": comment,
                    "sentiment": sentiment,
                    "author": item.get("author", "User")
                })

    return summary

