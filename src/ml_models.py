"""
ml_models.py
Implementasi Machine Learning untuk Klasifikasi Sentimen Teks:
- TF-IDF Vectorizer (Unigram + Bigram)
- Multinomial Naive Bayes
- Linear SVM Classifier (Hinge-Loss Pegasos/SGD)
- Logistic Regression Classifier
- Evaluation Metrics (Accuracy, Precision, Recall, F1-Score, Confusion Matrix)

Mendukung otomatis fallback ke pure Python jika scikit-learn tidak terpasang,
dan otomatis menggunakan scikit-learn jika tersedia.
"""

import math
from collections import Counter, defaultdict
from typing import List, Tuple, Dict, Any, Union

# Deteksi ketersediaan scikit-learn
HAS_SKLEARN = False
try:
    from sklearn.feature_extraction.text import TfidfVectorizer as SkTfidf
    from sklearn.naive_bayes import MultinomialNB as SkNB
    from sklearn.svm import LinearSVC as SkSVM
    from sklearn.linear_model import LogisticRegression as SkLogReg
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


class PureTfidfVectorizer:
    """Implementasi murni Python TF-IDF Vectorizer (1-2 gram, max_features)."""

    def __init__(self, max_features: int = 3000, ngram_range: Tuple[int, int] = (1, 2)):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.vocabulary_: Dict[str, int] = {}
        self.idf_: Dict[str, float] = {}

    def _extract_ngrams(self, text: str) -> List[str]:
        tokens = text.lower().split()
        ngrams = []
        min_n, max_n = self.ngram_range
        for n in range(min_n, max_n + 1):
            for i in range(len(tokens) - n + 1):
                ngrams.append(" ".join(tokens[i:i + n]))
        return ngrams

    def fit(self, documents: List[str]):
        doc_count = len(documents)
        df_counts = Counter()

        for doc in documents:
            unique_ngrams = set(self._extract_ngrams(doc))
            for ng in unique_ngrams:
                df_counts[ng] += 1

        # Pilih top max_features berdasarkan frekuensi kemunculan dokumen
        most_common = df_counts.most_common(self.max_features)
        self.vocabulary_ = {term: idx for idx, (term, _) in enumerate(most_common)}

        # Hitung smoothed IDF: log((1 + N) / (1 + df)) + 1
        self.idf_ = {}
        for term in self.vocabulary_:
            df = df_counts[term]
            self.idf_[term] = math.log((1 + doc_count) / (1 + df)) + 1.0
        return self

    def transform(self, documents: List[str]) -> List[Dict[int, float]]:
        sparse_matrix = []
        for doc in documents:
            ngrams = self._extract_ngrams(doc)
            tf_counts = Counter(ngrams)
            vec = {}
            norm_sq = 0.0

            for term, count in tf_counts.items():
                if term in self.vocabulary_:
                    idx = self.vocabulary_[term]
                    tfidf_val = count * self.idf_[term]
                    vec[idx] = tfidf_val
                    norm_sq += tfidf_val ** 2

            # L2 normalization
            if norm_sq > 0:
                norm = math.sqrt(norm_sq)
                for idx in vec:
                    vec[idx] /= norm

            sparse_matrix.append(vec)
        return sparse_matrix

    def fit_transform(self, documents: List[str]):
        return self.fit(documents).transform(documents)


class PureMultinomialNB:
    """Implementasi Naive Bayes Multinomial dengan Laplace smoothing."""

    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha
        self.classes_ = [-1, 0, 1]
        self.class_priors_: Dict[int, float] = {}
        self.feature_log_probs_: Dict[int, Dict[int, float]] = {}

    def fit(self, X: List[Dict[int, float]], y: List[int], num_features: int):
        total_samples = len(y)
        class_counts = Counter(y)

        # Log class priors
        for c in self.classes_:
            count = class_counts.get(c, 0)
            self.class_priors_[c] = math.log(max(count, 1e-5) / total_samples)

        # Feature counts per class
        feature_weights = {c: defaultdict(float) for c in self.classes_}
        total_weights = {c: 0.0 for c in self.classes_}

        for vec, label in zip(X, y):
            for idx, val in vec.items():
                feature_weights[label][idx] += val
                total_weights[label] += val

        # Log likelihood with Laplace smoothing
        self.feature_log_probs_ = {}
        for c in self.classes_:
            self.feature_log_probs_[c] = {}
            denom = total_weights[c] + self.alpha * num_features
            for idx in range(num_features):
                num = feature_weights[c].get(idx, 0.0) + self.alpha
                self.feature_log_probs_[c][idx] = math.log(num / denom)
        return self

    def predict(self, X: List[Dict[int, float]]) -> List[int]:
        predictions = []
        for vec in X:
            best_class = None
            best_score = -float('inf')

            for c in self.classes_:
                score = self.class_priors_[c]
                for idx, val in vec.items():
                    if idx in self.feature_log_probs_[c]:
                        score += val * self.feature_log_probs_[c][idx]
                if score > best_score:
                    best_score = score
                    best_class = c
            predictions.append(best_class)
        return predictions


class PureLinearSVM:
    """Linear SVM (Multi-class One-vs-Rest) dilatih dengan SGD Hinge-Loss."""

    def __init__(self, epochs: int = 40, lr: float = 0.05, reg: float = 0.001):
        self.epochs = epochs
        self.lr = lr
        self.reg = reg
        self.classes_ = [-1, 0, 1]
        self.weights_: Dict[int, Dict[int, float]] = {}
        self.biases_: Dict[int, float] = {}

    def fit(self, X: List[Dict[int, float]], y: List[int], num_features: int):
        for c in self.classes_:
            w = defaultdict(float)
            b = 0.0
            binary_y = [1 if label == c else -1 for label in y]

            for epoch in range(self.epochs):
                decayed_lr = self.lr / (1 + 0.01 * epoch)
                for vec, target in zip(X, binary_y):
                    margin = sum(w[idx] * val for idx, val in vec.items()) + b
                    if target * margin < 1.0:
                        for idx, val in vec.items():
                            w[idx] = (1.0 - decayed_lr * self.reg) * w[idx] + decayed_lr * target * val
                        b += decayed_lr * target
                    else:
                        for idx in list(vec.keys()):
                            w[idx] = (1.0 - decayed_lr * self.reg) * w[idx]

            self.weights_[c] = dict(w)
            self.biases_[c] = b
        return self

    def predict(self, X: List[Dict[int, float]]) -> List[int]:
        predictions = []
        for vec in X:
            best_class = None
            best_score = -float('inf')
            for c in self.classes_:
                score = sum(self.weights_[c].get(idx, 0.0) * val for idx, val in vec.items()) + self.biases_[c]
                if score > best_score:
                    best_score = score
                    best_class = c
            predictions.append(best_class)
        return predictions


def calculate_metrics(y_true: List[int], y_pred: List[int]) -> Dict[str, Any]:
    """Menghitung metrik performa model (Akurasi, Presisi, Recall, F1, Confusion Matrix)."""
    classes = [-1, 0, 1]
    class_names = ["Negatif", "Netral", "Positif"]

    total = len(y_true)
    correct = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp)
    accuracy = correct / total if total > 0 else 0.0

    # Confusion Matrix: baris = actual, kolom = predicted
    cm = [[0 for _ in classes] for _ in classes]
    c_to_idx = {c: i for i, c in enumerate(classes)}

    for yt, yp in zip(y_true, y_pred):
        if yt in c_to_idx and yp in c_to_idx:
            cm[c_to_idx[yt]][c_to_idx[yp]] += 1

    per_class = {}
    macro_p, macro_r, macro_f1 = 0.0, 0.0, 0.0

    for i, c in enumerate(classes):
        tp = cm[i][i]
        fp = sum(cm[row][i] for row in range(len(classes))) - tp
        fn = sum(cm[i][col] for col in range(len(classes))) - tp
        support = sum(cm[i][col] for col in range(len(classes)))

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        per_class[class_names[i]] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1-score": round(f1, 4),
            "support": support
        }
        macro_p += precision
        macro_r += recall
        macro_f1 += f1

    num_c = len(classes)
    return {
        "accuracy": round(accuracy, 4),
        "confusion_matrix": cm,
        "classes": class_names,
        "per_class": per_class,
        "macro_avg": {
            "precision": round(macro_p / num_c, 4),
            "recall": round(macro_r / num_c, 4),
            "f1-score": round(macro_f1 / num_c, 4)
        }
    }

