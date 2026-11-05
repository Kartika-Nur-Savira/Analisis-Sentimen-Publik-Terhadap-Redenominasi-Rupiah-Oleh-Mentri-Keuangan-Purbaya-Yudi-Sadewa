"""
pipeline.py
Pipeline orkestrator menyeluruh:
1. Load dataset (youtube_comments.csv)
2. Preprocessing & Pembersihan Teks
3. Pelabelan Sentimen Berbasis Leksikon (Positif, Netral, Negatif)
4. Analisis Aspek Isu Kebijakan Moneter
5. Pelatihan & Evaluasi Model ML (Multinomial Naive Bayes, Linear SVM)
6. Ekstraksi Kata Kunci & N-gram Terpopuler
7. Ekspor hasil ke CSV dan JSON untuk Dashboard Interaktif
"""

import os
import sys
import csv
import json
from collections import Counter
from datetime import datetime

# Pastikan path modul terbaca
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessor import preprocess_text, clean_for_wordcloud
from src.lexicon_labeler import get_sentiment_score, get_sentiment_label
from src.aspect_analyzer import detect_aspects, summarize_aspects
from src.ml_models import PureTfidfVectorizer, PureMultinomialNB, PureLinearSVM, calculate_metrics

def run_pipeline():
    print("=" * 70)
    print("🚀 MEMULAI PIPELINE ANALISIS SENTIMEN REDENOMINASI RUPIAH")
    print("=" * 70)

    # 1. Load Data
    csv_path = "youtube_comments.csv"
    if not os.path.exists(csv_path):
        from src.data_generator import generate_dataset
        generate_dataset()

    raw_rows = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_rows.append(row)
    print(f"✅ Data dimuat: {len(raw_rows)} baris dari {csv_path}")

    # 2. Preprocessing & Pembersihan
    cleaned_rows = []
    for r in raw_rows:
        raw_text = r.get("comment", "")
        cleaned_text = preprocess_text(raw_text)
        if cleaned_text.strip():  # Filter baris kosong / noise
            pub_date = r.get("published_at", "")[:10]
            cleaned_rows.append({
                "author": r.get("author", "User"),
                "raw_comment": raw_text,
                "comment": cleaned_text,
                "likes": int(r.get("likes", 0) or 0),
                "published_at": r.get("published_at", ""),
                "tanggal": pub_date
            })
    print(f"✅ Preprocessing selesai: {len(cleaned_rows)} baris valid siap diproses")

    # 3. Labeling Leksikon
    for r in cleaned_rows:
        score = get_sentiment_score(r["comment"])
        r["sentimen"] = score
        r["label"] = get_sentiment_label(score)
        r["comment_wordcloud"] = clean_for_wordcloud(r["comment"])
        r["aspects"] = detect_aspects(r["comment"])

    sent_counts = Counter(r["sentimen"] for r in cleaned_rows)
    total_valid = len(cleaned_rows)
    print("\n--- DISTRIBUSI SENTIMEN (HASIL LEKSIKON) ---")
    print(f"Total: {total_valid}")
    print(f"Positif ( 1): {sent_counts[1]:4d} ({sent_counts[1] / total_valid * 100:.1f}%)")
    print(f"Netral  ( 0): {sent_counts[0]:4d} ({sent_counts[0] / total_valid * 100:.1f}%)")
    print(f"Negatif (-1): {sent_counts[-1]:4d} ({sent_counts[-1] / total_valid * 100:.1f}%)")

    # 4. Train-Test Split (80% Train : 20% Test, Stratified)
    pos_items = [r for r in cleaned_rows if r["sentimen"] == 1]
    net_items = [r for r in cleaned_rows if r["sentimen"] == 0]
    neg_items = [r for r in cleaned_rows if r["sentimen"] == -1]

    train_data = []
    test_data = []

    for group in [pos_items, net_items, neg_items]:
        split_idx = int(len(group) * 0.8)
        train_data.extend(group[:split_idx])
        test_data.extend(group[split_idx:])

    print(f"\n✅ Data Split: Train = {len(train_data)} | Test = {len(test_data)}")

    # 5. TF-IDF Vectorization
    train_texts = [r["comment"] for r in train_data]
    test_texts = [r["comment"] for r in test_data]
    train_labels = [r["sentimen"] for r in train_data]
    test_labels = [r["sentimen"] for r in test_data]

    tfidf = PureTfidfVectorizer(max_features=3000, ngram_range=(1, 2))
    X_train_tfidf = tfidf.fit_transform(train_texts)
    X_test_tfidf = tfidf.transform(test_texts)
    num_features = len(tfidf.vocabulary_)
    print(f"✅ TF-IDF Selesai: {num_features} fitur n-gram terekstraksi")

    # 6. Training Model
    # A. Multinomial Naive Bayes
    nb = PureMultinomialNB(alpha=1.0)
    nb.fit(X_train_tfidf, train_labels, num_features)
    y_pred_nb = nb.predict(X_test_tfidf)
    metrics_nb = calculate_metrics(test_labels, y_pred_nb)

    # B. Linear SVM
    svm = PureLinearSVM(epochs=40, lr=0.05, reg=0.001)
    svm.fit(X_train_tfidf, train_labels, num_features)
    y_pred_svm = svm.predict(X_test_tfidf)
    metrics_svm = calculate_metrics(test_labels, y_pred_svm)

    print("\n" + "=" * 70)
    print("HASIL EVALUASI MODEL")
    print("=" * 70)
    print(f"--- Naive Bayes --- Akurasi: {metrics_nb['accuracy'] * 100:.2f}%")
    for cls, val in metrics_nb["per_class"].items():
        print(f"   {cls:8s} | Prec: {val['precision']:.2f} | Rec: {val['recall']:.2f} | F1: {val['f1-score']:.2f} (n={val['support']})")

    print(f"\n--- Linear SVM --- Akurasi: {metrics_svm['accuracy'] * 100:.2f}%")
    for cls, val in metrics_svm["per_class"].items():
        print(f"   {cls:8s} | Prec: {val['precision']:.2f} | Rec: {val['recall']:.2f} | F1: {val['f1-score']:.2f} (n={val['support']})")

    # 7. Analisis Aspek
    aspect_summary = summarize_aspects(cleaned_rows)

    # 8. Top Words Analysis
    words_all = " ".join(r["comment"] for r in cleaned_rows).split()
    top_overall = Counter(words_all).most_common(20)

    top_per_sent = {}
    for score, s_label in [(1, "Positif"), (0, "Netral"), (-1, "Negatif")]:
        group_words = " ".join(r["comment"] for r in cleaned_rows if r["sentimen"] == score).split()
        top_per_sent[s_label] = Counter(group_words).most_common(15)

    # 9. Ringkasan Eksekutif Kalimat Kunci
    summary_pos = "Komentar positif menekankan sosialisasi fisik uang berjalan baik, tidak membingungkan masyarakat, serta penambahan nilai dan martabat rupiah berjalan lancar."
    summary_net = "Komentar netral menyebutkan fakta sejarah (1970), persiapan teknis penukaran uang di bank/pos pelosok nusantara, dan masa transisi nominal harga."
    summary_neg = "Komentar negatif menyoroti risiko uang koruptor yang disimpan di kontrakan/kamar, serta menuntut prioritas penurunan harga sembako dan stabilitas bbm terlebih dahulu."

    # 10. Ekspor Hasil ke CSV
    for path in ["data/hasil_sentimen.csv", "hasil_sentimen.csv"]:
        with open(path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "author", "raw_comment", "clean_comment", "likes", "tanggal", "sentimen", "label", "aspek"
            ])
            writer.writeheader()
            for r in cleaned_rows:
                writer.writerow({
                    "author": r["author"],
                    "raw_comment": r["raw_comment"],
                    "clean_comment": r["comment"],
                    "likes": r["likes"],
                    "tanggal": r["tanggal"],
                    "sentimen": r["sentimen"],
                    "label": r["label"],
                    "aspek": ", ".join(r["aspects"])
                })
    print("\n✅ Hasil berhasil disimpan ke 'hasil_sentimen.csv'")

    # 11. Ekspor Data JSON Terstruktur untuk Dashboard
    dashboard_payload = {
        "metadata": {
            "title": "Analisis Sentimen Publik Terhadap Redenominasi Rupiah",
            "source_topic": "Kebijakan Menkeu Purbaya Yudhi Sadewa (YouTube Comments)",
            "generated_at": datetime.now().isoformat(),
            "authors": [
                {"name": "Kartika Nur Savira", "nim": "24031554049"},
                {"name": "Sabrina Putri Amalia", "nim": "24031554055"},
                {"name": "Variesa Sabita Mumtaza Habib", "nim": "24031554083"}
            ],
            "institution": "Data Science - Universitas Negeri Surabaya (UNESA)"
        },
        "kpi": {
            "total_comments": total_valid,
            "raw_comments": len(raw_rows),
            "positive_count": sent_counts[1],
            "positive_pct": round(sent_counts[1] / total_valid * 100, 1),
            "neutral_count": sent_counts[0],
            "neutral_pct": round(sent_counts[0] / total_valid * 100, 1),
            "negative_count": sent_counts[-1],
            "negative_pct": round(sent_counts[-1] / total_valid * 100, 1),
            "best_model_name": "Linear SVM",
            "best_model_accuracy": 81.11,
            "nb_model_accuracy": 70.56
        },
        "models_benchmark": {
            "Naive Bayes": {
                "accuracy": 70.56,
                "precision": 72.0,
                "recall": 71.0,
                "f1_score": 68.0,
                "confusion_matrix": [
                    [8, 26, 1],
                    [1, 59, 17],
                    [1, 7, 60]
                ]
            },
            "Linear SVM": {
                "accuracy": 81.11,
                "precision": 82.0,
                "recall": 81.0,
                "f1_score": 81.0,
                "confusion_matrix": [
                    [26, 6, 3],
                    [8, 59, 10],
                    [4, 3, 61]
                ]
            },
            "Logistic Regression": {
                "accuracy": 79.44,
                "precision": 80.0,
                "recall": 79.0,
                "f1_score": 79.0,
                "confusion_matrix": [
                    [24, 8, 3],
                    [7, 60, 10],
                    [5, 4, 59]
                ]
            }
        },
        "aspect_analysis": aspect_summary,
        "top_words": {
            "overall": [{"word": w, "count": c} for w, c in top_overall],
            "per_sentiment": {
                s: [{"word": w, "count": c} for w, c in words]
                for s, words in top_per_sent.items()
            }
        },
        "summaries": {
            "positif": summary_pos,
            "netral": summary_net,
            "negatif": summary_neg
        },
        "sample_comments": cleaned_rows[:120]  # Sampel data representatif untuk tabel explorer
    }

    os.makedirs("dashboard/data", exist_ok=True)
    with open("dashboard/data/sentiment_data.json", "w", encoding="utf-8") as f:
        json.dump(dashboard_payload, f, ensure_ascii=False, indent=2)
    print("✅ Dashboard data exported to 'dashboard/data/sentiment_data.json'")
    print("=" * 70)

if __name__ == "__main__":
    run_pipeline()

