# Analisis Sentimen Publik Terhadap Redenominasi Rupiah
### Studi Kasus: Kebijakan Menteri Keuangan Purbaya Yudhi Sadewa (YouTube Comments Corpus)

[![Dataset](https://img.shields.io/badge/Dataset-896%20Komentar-blue.svg)](youtube_comments.csv)
[![Best Model](https://img.shields.io/badge/Model%20Terbaik-Linear%20SVM%20(81.11%25)-emerald.svg)](#evaluasi-model)
[![Dashboard](https://img.shields.io/badge/Dashboard-Interactive%20Web-purple.svg)](dashboard/index.html)
[![Institution](https://img.shields.io/badge/UNESA-Data%20Science-orange.svg)](#author)

https://analisis-sentimen-redenominasi-rupiah.vercel.app/dashboard

Proyek ini menganalisis opini dan sentimen publik masyarakat Indonesia terhadap wacana dan kebijakan redenominasi rupiah yang diangkat oleh Menteri Keuangan Purbaya Yudhi Sadewa berdasarkan data komentar platform YouTube.

---

## 👥 Tim Peneliti & Pengembang

- **Kartika Nur Savira** (24031554049)
- **Sabrina Putri Amalia** (24031554055)
- **Variesa Sabita Mumtaza Habib** (24031554083)

*Program Studi Sains Data — Fakultas Matematika dan Ilmu Pengetahuan Alam (FMIPA)  
Universitas Negeri Surabaya (UNESA)*

---

## 📊 Ringkasan Hasil & Temuan Kunci

Dari **896 komentar valid** yang telah melewati proses preprocessing teks dan pembersihan:

| Kategori Sentimen | Jumlah Komentar | Persentase | Karakteristik Utama Aspirasi Publik |
|---|:---:|:---:|---|
| **Netral (0)** | **383** | **42.7%** | Mempertanyakan kesiapan teknis bank/pos pelosok, fakta sejarah redenominasi (1970), dan menuntut masa transisi yang jelas. |
| **Positif (+1)** | **341** | **38.1%** | Mendukung penyederhanaan digit rupiah, efisiensi transaksi, kemudahan akuntansi digital, dan peningkatan martabat mata uang. |
| **Negatif (-1)** | **172** | **19.2%** | Khawatir uang tunai timbunan koruptor dicuci saat penukaran, risiko pembulatan harga sembako ke atas, dan trauma sanering. |

---

## 🤖 Perbandingan Performa Model Machine Learning

Data diekstraksi menggunakan **TF-IDF Vectorizer (Unigram + Bigram, 3000 Fitur)** dengan rasio pembagian *Stratified Split* 80% Data Latih (716 baris) dan 20% Data Uji (180 baris):

| Algoritma Model | Akurasi | Precision (Macro) | Recall (Macro) | F1-Score (Macro) | Keunggulan & Catatan |
|---|:---:|:---:|:---:|:---:|---|
| **Linear SVM** ⭐ | **81.11%** | **0.79** | **0.80** | **0.79** | **Performa Terbaik.** Mampu mengenali sentimen negatif dengan Recall 74% dan F1 0.71. |
| **Logistic Regression** | **79.44%** | **0.80** | **0.79** | **0.79** | Stabil dan seimbang dalam membedakan batas antar kelas sentimen. |
| **Multinomial Naive Bayes** | **70.56%** | **0.73** | **0.63** | **0.62** | Cukup baik pada teks positif, namun lemah pada teks negatif (Recall hanya 23%). |

---

## 🏛️ Analisis 4 Aspek Isu Kebijakan Moneter (ABSA)

1. **Pemberantasan Korupsi & Transparansi:** Sorotan tajam terhadap uang tunai di luar sistem perbankan. Publik menuntut penukaran uang baru wajib dilengkapi verifikasi asal-usul harta (KYC/PPATK).
2. **Sosialisasi & Uang Fisik:** Publik mendesak contoh visual bentuk uang kertas dan logam baru diedukasikan secara masif ke pasar tradisional dan pedesaan.
3. **Kondisi Ekonomi & Harga Pasar:** Desakan agar pemerintah memprioritaskan stabilisasi harga sembako dan BBM sebelum memulai penarikan uang lama.
4. **Martabat & Nilai Tukar Rupiah:** Kebanggaan publik jika angka nol rupiah berkurang sehingga nilainya tampak kuat di kancah internasional.

---

## 🚀 Cara Menjalankan Project & Dashboard

### 1. Menjalankan Dashboard Interaktif

Cukup jalankan satu perintah python berikut di terminal:

```bash
python3 run_dashboard.py
```
> Server lokal akan aktif di `http://localhost:8080/index.html` dan otomatis membuka browser Anda.  
> *Alternatif tanpa server:* Anda juga dapat langsung membuka file [`dashboard/index.html`](file:///Users/savv/sentimen/Analisis-Sentimen-Publik-Terhadap-Redenominasi-Rupiah-Oleh-Mentri-Keuangan-Purbaya-Yudi-Sadewa/dashboard/index.html) langsung di browser Anda!

### 2. Fitur Dashboard:
- 📊 **Overview KPI Cards:** Statistik total komentar, persentase sentimen, dan akurasi model.
- 🤖 **Interactive Confusion Matrix:** Heatmap interaktif untuk model SVM, Naive Bayes, dan Logistic Regression.
- 🏛️ **Analisis 4 Pilar Aspek:** Distribusi sentimen per topik kebijakan moneter.
- 🔤 **Word Frequency & Word Cloud:** Visualisasi bar chart kata terpopuler serta galeri WordCloud resolusi tinggi.
- 📋 **Data Explorer:** Tabel penelusuran komentar dengan filter sentimen, pencarian nama akun/@author, dan pagination.
- 🧪 **Live Sentiment Tester (Interactive Sandbox):** Ketik opini baru dalam bahasa gaul/formal dan lihat proses translasi slang, ekstraksi token, skor leksikon, serta prediksi model secara langsung!
- 📑 **Rekomendasi Kebijakan:** Butir-butir saran strategis bagi Kementerian Keuangan dan Bank Indonesia.
- 🌓 **Mode Gelap & Terang (Dark/Light Mode).**
- 📥 **Ekspor Data ke CSV & Cetak Laporan PDF.**

### 3. Menjalankan Pipeline Analisis Ulang (Python)

```bash
python3 -m src.pipeline
```

### 4. Menjalankan Jupyter Notebook
Tersedia dua notebook:
- `Analisis Sentimen Terhadap Redenominasi Rupiah - Enhanced.ipynb`: Versi pengembangan modern, mandiri (self-contained), dilengkapi evaluasi model lengkap dan interactive tester.
- `Analisis Sentimen Terhadap Redenominasi Rupiah.ipynb`: Notebook asli proyek.

---

## 📁 Struktur Berkas Repository

```text
├── dashboard/                              # Aplikasi Web Dashboard Interaktif
│   ├── index.html                          # Tampilan utama dashboard modern
│   ├── styles.css                          # Desain responsif, modern theme & glassmorphism
│   ├── app.js                              # Logika interaktif, Chart.js & Live Sentiment Tester
│   ├── data/
│   │   ├── sentiment_data.json             # Ekspor data terstruktur
│   │   └── sentiment_data.js               # Offline data fallback
│   └── images/                             # Galeri visualisasi & WordCloud asli
│       ├── evaluasi_model.png
│       ├── wordcloud_sentimen.png
│       ├── top20_kata_bersih.png
│       └── top20_kata_raw.png
├── data/                                   # Folder dataset terorganisir
│   ├── youtube_comments.csv                # 900 komentar YouTube
│   └── hasil_sentimen.csv                  # Hasil klasifikasi lengkap dengan label & aspek
├── src/                                    # Arsitektur modul Python bersih
│   ├── dictionaries.py                     # Kamus normalisasi gaul, stopwords, leksikon sentimen
│   ├── preprocessor.py                     # Pembersihan teks, emoji regex, font normalizer
│   ├── lexicon_labeler.py                  # Rule-based scoring, negasi, detail analisis
│   ├── aspect_analyzer.py                  # Aspect-based sentiment analysis (4 pilar)
│   ├── ml_models.py                        # TF-IDF, Naive Bayes, Linear SVM & metrik evaluasi
│   ├── data_generator.py                   # Generator data terkalibrasi
│   └── pipeline.py                         # Orkestrator eksekusi end-to-end
├── Analisis Sentimen PPT.pptx              # File presentasi presentasi proyek
├── LAPORAN PROJECT PEMTEKS.pdf             # Laporan lengkap proyek UNESA
├── Stopword - Sheet1.csv                   # Daftar stopword bahasa Indonesia
├── run_dashboard.py                        # Script satu-klik untuk menjalankan dashboard
└── README.md                               # Dokumentasi lengkap proyek
```
