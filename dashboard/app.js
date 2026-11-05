/**
 * app.js - Logika Interaktif & Visualisasi Analisis Sentimen Redenominasi Rupiah
 * Sesuai dengan Kode & Temuan Riset NLP UNESA
 */

let sentimentData = null;
let charts = {};

// Kamus Slang & Leksikon untuk Live Tester Sandbox
const SLANG_DICT = {
  "se7": "setuju", "s7": "setuju", "stju": "setuju", "stuju": "setuju", "suju": "setuju",
  "bgt": "banget", "bngt": "banget", "mantul": "mantap", "mantep": "mantap", "kren": "keren",
  "gk": "tidak", "ga": "tidak", "gak": "tidak", "gx": "tidak", "nggak": "tidak", "enggak": "tidak",
  "gw": "saya", "gue": "saya", "lu": "kamu", "udh": "sudah", "udah": "sudah", "blm": "belum",
  "menkeu": "menteri keuangan", "korup": "koruptor", "duwit": "duit", "rp": "rupiah",
  "tp": "tapi", "krn": "karena", "jd": "jadi", "dgn": "dengan", "hrs": "harus", "thn": "tahun"
};

const POS_PHRASES = [
  "sangat setuju", "setuju sekali", "setuju banget", "saya setuju", "setuju pak",
  "sangat bagus", "bagus sekali", "sangat mantap", "mantap sekali", "sangat baik",
  "terima kasih", "mendukung penuh", "sangat mendukung", "hebat sekali", "luar biasa"
];

const NEG_PHRASES = [
  "tidak setuju", "ga setuju", "gak setuju", "tidak percaya", "ga percaya",
  "tidak benar", "sangat buruk", "parah sekali", "bohong semua", "koruptor semua",
  "korupsi semua", "tidak masuk akal", "bikin ribet"
];

const POS_WORDS = new Set([
  "setuju", "dukung", "mendukung", "yakin", "percaya", "bagus", "baik", "mantap",
  "hebat", "keren", "top", "terbaik", "luar", "biasa", "oke", "cepat", "mudah",
  "efektif", "efisien", "untung", "maju", "positif", "solusi", "manfaat", "berguna"
]);

const NEG_WORDS = new Set([
  "tolak", "menolak", "buruk", "jelek", "parah", "gagal", "hancur", "rusak", "kacau",
  "bahaya", "merugikan", "kecewa", "kesal", "marah", "sulit", "berat", "bohong",
  "korup", "koruptor", "korupsi", "curang", "rugi", "miskin", "mahal", "krisis", "turun"
]);

document.addEventListener("DOMContentLoaded", async () => {
  await initData();
  setupSidebarNavigation();
  setupSearch();
  renderOverviewBarChart();
  renderOverviewDonutChart();
  populateOverviewTable();
  renderModelEvaluations();
  renderAspectChart();
  renderTopWordsChart("overall");
  populateFullDatasetTable();
  setupExportAndPrint();
  setupModalKeyboard();
});

// 1. Inisialisasi Data
async function initData() {
  if (window.SENTIMENT_DATA) {
    sentimentData = window.SENTIMENT_DATA;
    return;
  }
  try {
    const res = await fetch("data/sentiment_data.json");
    sentimentData = await res.json();
  } catch (e) {
    console.warn("Gagal memuat JSON eksternal, menggunakan fallback", e);
  }
}

// 2. Navigasi Sidebar Tab
function setupSidebarNavigation() {
  const navButtons = document.querySelectorAll(".sidebar-nav .nav-link");

  navButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetTab = btn.getAttribute("data-tab");
      if (!targetTab) return;

      document.querySelectorAll(".sidebar-nav .nav-link").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      document.querySelectorAll(".view-panel").forEach(panel => {
        panel.style.display = "none";
      });

      const activePanel = document.getElementById(`view-${targetTab}`);
      if (activePanel) {
        activePanel.style.display = "block";
      }

      window.dispatchEvent(new Event("resize"));
    });
  });
}

// 3. Overview Bar Chart: Perbandingan Akurasi Model ML
function renderOverviewBarChart() {
  const ctx = document.getElementById("chart-model-accuracy-bar")?.getContext("2d");
  if (!ctx) return;

  if (charts.overviewBar) charts.overviewBar.destroy();

  charts.overviewBar = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Linear SVM", "Logistic Reg", "Naive Bayes"],
      datasets: [{
        label: "Akurasi Model (%)",
        data: [81.11, 79.44, 70.56],
        backgroundColor: [
          "#4f80ff",
          "rgba(79, 128, 255, 0.75)",
          "rgba(79, 128, 255, 0.45)"
        ],
        hoverBackgroundColor: "#6894ff",
        borderRadius: 14,
        borderSkipped: false,
        barPercentage: 0.48,
        categoryPercentage: 0.7
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#161922",
          titleColor: "#ffffff",
          bodyColor: "#94a3b8",
          borderColor: "rgba(255, 255, 255, 0.1)",
          borderWidth: 1,
          padding: 10,
          cornerRadius: 10,
          callbacks: {
            label: (item) => ` Akurasi: ${item.formattedValue}%`
          }
        }
      },
      scales: {
        y: {
          min: 50,
          max: 100,
          ticks: {
            stepSize: 10,
            color: "#5c6475",
            callback: (v) => v + "%",
            font: { size: 11, family: "'Plus Jakarta Sans', sans-serif" }
          },
          grid: {
            color: "rgba(255, 255, 255, 0.04)",
            drawBorder: false
          },
          border: { display: false }
        },
        x: {
          ticks: {
            color: "#8e95a5",
            font: { size: 12, weight: "700", family: "'Plus Jakarta Sans', sans-serif" }
          },
          grid: { display: false },
          border: { display: false }
        }
      }
    }
  });
}

// 4. Overview Donut Chart: Proporsi Sentimen Publik (38.1% Positif, 42.7% Netral, 19.2% Negatif)
function renderOverviewDonutChart() {
  const ctx = document.getElementById("chart-sentiment-donut")?.getContext("2d");
  if (!ctx) return;

  if (charts.sentimentDonut) charts.sentimentDonut.destroy();

  charts.sentimentDonut = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Positif", "Netral", "Negatif"],
      datasets: [{
        data: [341, 383, 172],
        backgroundColor: [
          "#22c55e", // Positif (Emerald Green)
          "#94a3b8", // Netral (Slate Gray)
          "#f43f5e"  // Negatif (Coral Rose)
        ],
        borderWidth: 0,
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "72%",
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#161922",
          titleColor: "#ffffff",
          bodyColor: "#94a3b8",
          borderColor: "rgba(255, 255, 255, 0.1)",
          borderWidth: 1,
          padding: 10,
          cornerRadius: 10,
          callbacks: {
            label: (item) => ` ${item.label}: ${item.raw} komentar (${(item.raw/896*100).toFixed(1)}%)`
          }
        }
      }
    }
  });
}

// 5. Populate Overview Table (Komentar Nyata YouTube)
function populateOverviewTable() {
  const tbody = document.getElementById("overview-table-body");
  if (!tbody) return;

  const comments = (sentimentData && sentimentData.sample_comments) ? sentimentData.sample_comments : [];
  if (comments.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding: 1.5rem; color: #5c6475;">Memuat data...</td></tr>`;
    return;
  }

  tbody.innerHTML = comments.slice(0, 6).map(r => {
    let badgeClass = "net";
    let badgeLabel = "Netral (0)";
    if (r.sentimen === 1) {
      badgeClass = "pos";
      badgeLabel = "Positif (+1)";
    } else if (r.sentimen === -1) {
      badgeClass = "neg";
      badgeLabel = "Negatif (-1)";
    }

    const aspectName = (r.aspects && r.aspects.length > 0) ? r.aspects[0] : (r.aspek || "Umum");

    return `
      <tr>
        <td class="table-author-name">${escapeHtml(r.author || "@user")}</td>
        <td style="max-width: 480px; line-height: 1.45; color: #d1d5db;">
          ${escapeHtml(r.raw_comment || r.comment)}
        </td>
        <td><span class="badge-pill ${badgeClass}">${badgeLabel}</span></td>
        <td style="font-size: 0.75rem; color: #8e95a5;">${escapeHtml(aspectName)}</td>
        <td style="color: #5c6475; font-size: 0.75rem;">${r.tanggal || "2025-12-10"}</td>
      </tr>
    `;
  }).join("");
}

// 6. Evaluasi Model: Detail Precision, Recall, F1 & Confusion Matrix
function renderModelEvaluations() {
  const ctxDetail = document.getElementById("chart-models-detail-bar")?.getContext("2d");
  if (ctxDetail) {
    if (charts.detailBar) charts.detailBar.destroy();
    charts.detailBar = new Chart(ctxDetail, {
      type: "bar",
      data: {
        labels: ["Linear SVM", "Logistic Reg", "Naive Bayes"],
        datasets: [
          { label: "Precision (%)", data: [82.0, 80.0, 72.0], backgroundColor: "#38bdf8", borderRadius: 6 },
          { label: "Recall (%)", data: [81.0, 79.0, 71.0], backgroundColor: "#4f80ff", borderRadius: 6 },
          { label: "F1-Score (%)", data: [81.0, 79.0, 68.0], backgroundColor: "#818cf8", borderRadius: 6 }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: { color: "#8e95a5", boxWidth: 12, font: { size: 11, family: "'Plus Jakarta Sans'" } }
          }
        },
        scales: {
          y: { min: 50, max: 100, ticks: { color: "#5c6475" }, grid: { color: "rgba(255,255,255,0.04)" } },
          x: { ticks: { color: "#8e95a5", font: { weight: "600" } }, grid: { display: false } }
        }
      }
    });
  }

  // Confusion Matrix Viewer
  renderConfusionMatrix("Linear SVM");
  const switcher = document.getElementById("cm-model-switcher");
  if (switcher) {
    switcher.addEventListener("change", (e) => renderConfusionMatrix(e.target.value));
  }
}

function renderConfusionMatrix(modelName) {
  const container = document.getElementById("cm-grid-container");
  if (!container || !sentimentData || !sentimentData.models_benchmark) return;

  const modelInfo = sentimentData.models_benchmark[modelName];
  if (!modelInfo) return;

  const cm = modelInfo.confusion_matrix;
  const classes = ["Negatif", "Netral", "Positif"];

  let html = `
    <table class="table-custom" style="text-align: center; margin-top: 0.5rem;">
      <thead>
        <tr>
          <th style="font-size: 0.7rem; color: #5c6475;">Aktual \\ Pred</th>
          <th style="font-size: 0.75rem; color: #f43f5e;">Pred: Neg</th>
          <th style="font-size: 0.75rem; color: #94a3b8;">Pred: Net</th>
          <th style="font-size: 0.75rem; color: #22c55e;">Pred: Pos</th>
        </tr>
      </thead>
      <tbody>
  `;

  for (let r = 0; r < 3; r++) {
    html += `<tr><td style="font-weight: 700; color: #8e95a5; font-size: 0.75rem;">${classes[r]}</td>`;
    for (let c = 0; c < 3; c++) {
      const val = cm[r][c];
      const isDiag = (r === c);
      const bg = isDiag ? "rgba(79, 128, 255, 0.18)" : (val > 10 ? "rgba(244, 63, 94, 0.1)" : "#13161f");
      const textColor = isDiag ? "#4f80ff" : (val > 10 ? "#fb7185" : "#5c6475");
      html += `<td style="background: ${bg}; font-weight: 800; font-size: 1rem; color: ${textColor}; border-radius: 8px;">${val}</td>`;
    }
    html += `</tr>`;
  }

  html += `</tbody></table>
    <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #5c6475; margin-top: 10px;">
      <span>Diagonal Biru = Prediksi Benar</span>
      <span style="color: #4ade80; font-weight: 700;">Akurasi: ${modelInfo.accuracy}%</span>
    </div>
  `;

  container.innerHTML = html;
}

// 7. Aspek Kebijakan Moneter Chart
function renderAspectChart() {
  const ctx = document.getElementById("chart-aspect-breakdown")?.getContext("2d");
  if (!ctx) return;

  if (charts.aspect) charts.aspect.destroy();

  charts.aspect = new Chart(ctx, {
    type: "bar",
    data: {
      labels: [
        "1. Pemberantasan Korupsi",
        "2. Sosialisasi & Fisik Uang",
        "3. Kondisi Ekonomi & Sembako",
        "4. Martabat Nilai Tukar"
      ],
      datasets: [
        { label: "Positif", data: [15, 86, 28, 82], backgroundColor: "#22c55e", borderRadius: 6 },
        { label: "Netral", data: [32, 45, 62, 35], backgroundColor: "#94a3b8", borderRadius: 6 },
        { label: "Negatif", data: [86, 12, 51, 8], backgroundColor: "#f43f5e", borderRadius: 6 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: { color: "#8e95a5", boxWidth: 12, font: { size: 11, family: "'Plus Jakarta Sans'" } }
        }
      },
      scales: {
        x: { stacked: true, grid: { display: false }, ticks: { color: "#8e95a5", font: { weight: "600" } } },
        y: { stacked: true, grid: { color: "rgba(255,255,255,0.04)" }, ticks: { color: "#5c6475" } }
      }
    }
  });
}

// 8. Top Words Chart & Filter
function renderTopWordsChart(sentimentFilter = "overall") {
  const ctx = document.getElementById("chart-top-words-bar")?.getContext("2d");
  if (!ctx || !sentimentData || !sentimentData.top_words) return;

  let list = [];
  let barColor = "#4f80ff";

  if (sentimentFilter === "overall") {
    list = sentimentData.top_words.overall.slice(0, 10);
    barColor = "#4f80ff";
  } else {
    list = (sentimentData.top_words.per_sentiment[sentimentFilter] || []).slice(0, 10);
    if (sentimentFilter === "Positif") barColor = "#22c55e";
    else if (sentimentFilter === "Negatif") barColor = "#f43f5e";
    else if (sentimentFilter === "Netral") barColor = "#94a3b8";
  }

  const labels = list.map(item => item.word);
  const values = list.map(item => item.count);

  if (charts.topWords) charts.topWords.destroy();

  charts.topWords = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Frekuensi Kemunculan",
        data: values,
        backgroundColor: barColor,
        borderRadius: 8,
        barPercentage: 0.6
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { beginAtZero: true, grid: { color: "rgba(255,255,255,0.04)" }, ticks: { color: "#5c6475" } },
        y: { grid: { display: false }, ticks: { color: "#8e95a5", font: { weight: "600" } } }
      }
    }
  });

  const select = document.getElementById("select-word-filter");
  if (select && !select.onchange) {
    select.onchange = (e) => renderTopWordsChart(e.target.value);
  }
}

// 9. Full Dataset Explorer Table
function populateFullDatasetTable() {
  const tbody = document.getElementById("full-comments-table-body");
  const filter = document.getElementById("explorer-filter-sentiment");
  if (!tbody || !sentimentData) return;

  const allComments = sentimentData.sample_comments || [];

  function renderRows(selectedSent = "ALL") {
    const filtered = allComments.filter(r => {
      return selectedSent === "ALL" || String(r.sentimen) === selectedSent;
    });

    if (filtered.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 2rem; color: #5c6475;">Tidak ada komentar yang cocok.</td></tr>`;
      return;
    }

    tbody.innerHTML = filtered.map((r, i) => {
      let badgeClass = "net";
      let badgeLabel = "Netral (0)";
      if (r.sentimen === 1) {
        badgeClass = "pos";
        badgeLabel = "Positif (+1)";
      } else if (r.sentimen === -1) {
        badgeClass = "neg";
        badgeLabel = "Negatif (-1)";
      }

      const aspectName = (r.aspects && r.aspects.length > 0) ? r.aspects[0] : (r.aspek || "Umum");

      return `
        <tr>
          <td style="color: #5c6475; font-size: 0.75rem;">${i + 1}</td>
          <td class="table-author-name">${escapeHtml(r.author || "@user")}</td>
          <td style="max-width: 480px; line-height: 1.45; color: #d1d5db;">
            <p>${escapeHtml(r.raw_comment || r.comment)}</p>
            <p style="font-size: 0.7rem; color: #5c6475; font-style: italic; margin-top: 2px;">
              Preprocessed: ${escapeHtml(r.clean_comment || r.comment)}
            </p>
          </td>
          <td><span class="badge-pill ${badgeClass}">${badgeLabel}</span></td>
          <td style="font-size: 0.75rem; color: #8e95a5;">${escapeHtml(aspectName)}</td>
          <td style="color: #5c6475; font-size: 0.75rem;">${r.tanggal || "2025-12-10"}</td>
        </tr>
      `;
    }).join("");
  }

  renderRows("ALL");
  if (filter) {
    filter.addEventListener("change", (e) => renderRows(e.target.value));
  }
}

// 10. Global Search Filter
function setupSearch() {
  const input = document.getElementById("global-search");
  if (!input) return;

  input.addEventListener("input", (e) => {
    const q = e.target.value.toLowerCase().trim();
    const rows = document.querySelectorAll("#overview-table-body tr, #full-comments-table-body tr");

    rows.forEach(row => {
      const text = row.innerText.toLowerCase();
      row.style.display = text.includes(q) ? "" : "none";
    });
  });
}

// 11. Modal Zoom Lightbox
window.openZoomModal = function(imgSrc, title) {
  const modal = document.getElementById("zoom-modal");
  const modalImg = document.getElementById("zoom-modal-img");
  const modalTitle = document.getElementById("zoom-modal-title");

  if (modal && modalImg) {
    modalImg.src = imgSrc;
    if (modalTitle) modalTitle.innerText = title || "Word Cloud";
    modal.classList.add("active");
  }
};

window.closeZoomModal = function(event) {
  if (event && event.target && event.target.id !== "zoom-modal" && event.target.tagName !== "BUTTON") {
    return;
  }
  const modal = document.getElementById("zoom-modal");
  if (modal) {
    modal.classList.remove("active");
  }
};

function setupModalKeyboard() {
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      const modal = document.getElementById("zoom-modal");
      if (modal) modal.classList.remove("active");
    }
  });
}

// 12. Live Tester Sandbox
window.setSandboxSample = function(text) {
  const area = document.getElementById("sandbox-textarea");
  if (area) {
    area.value = text;
    runSandboxAnalysis();
  }
};

const runSandboxBtn = document.getElementById("btn-run-sandbox");
if (runSandboxBtn) {
  runSandboxBtn.addEventListener("click", runSandboxAnalysis);
}

function runSandboxAnalysis() {
  const area = document.getElementById("sandbox-textarea");
  const rawText = (area?.value || "").trim();
  const resBox = document.getElementById("sandbox-result-box");
  const badge = document.getElementById("sandbox-badge");
  const exp = document.getElementById("sandbox-explanation");
  const tokensBox = document.getElementById("sandbox-tokens-box");

  if (!rawText || !resBox || !badge || !exp) return;

  resBox.style.display = "block";

  const lower = rawText.toLowerCase();
  let score = 0;
  const slangReplaces = [];
  const words = lower.replace(/[.,!?;:"'()]/g, " ").split(/\s+/).filter(Boolean);

  // Deteksi frasa multi-kata
  let phraseMatched = false;
  POS_PHRASES.forEach(p => {
    if (lower.includes(p)) {
      score += 2;
      phraseMatched = true;
    }
  });
  NEG_PHRASES.forEach(p => {
    if (lower.includes(p)) {
      score -= 2;
      phraseMatched = true;
    }
  });

  // Token processing & slang
  words.forEach(w => {
    const norm = SLANG_DICT[w] || w;
    if (norm !== w) {
      slangReplaces.push(`<strong>${w}</strong> ➔ <em>${norm}</em>`);
    }
    if (POS_WORDS.has(norm)) score += 1;
    if (NEG_WORDS.has(norm)) score -= 1;
  });

  // Decision
  if (score >= 1) {
    badge.className = "badge-pill pos";
    badge.innerText = `Positif (+1) • Skor: +${score}`;
    exp.innerHTML = `Teks mengandung dukungan atau apresiasi terhadap penyederhanaan digit rupiah, efisiensi transaksi, atau kemajuan ekonomi.`;
  } else if (score <= -1) {
    badge.className = "badge-pill neg";
    badge.innerText = `Negatif (-1) • Skor: ${score}`;
    exp.innerHTML = `Teks mengandung penolakan, kritik harga sembako/inflasi, atau kekhawatiran terhadap pencucian uang hasil korupsi.`;
  } else {
    badge.className = "badge-pill net";
    badge.innerText = `Netral (0) • Skor: 0`;
    exp.innerHTML = `Teks bernada faktual, historis, atau menanyakan teknis sosialisasi penukaran fisik uang baru di perbankan.`;
  }

  if (tokensBox) {
    tokensBox.innerHTML = `
      <div style="color: #8e95a5;">
        <span>Normalisasi Slang/Gaul: </span>
        <span>${slangReplaces.length > 0 ? slangReplaces.join(", ") : "Tidak ada singkatan yang diubah"}</span>
      </div>
    `;
  }
}

// 13. Export & Print Handlers
function setupExportAndPrint() {
  const exportBtn = document.getElementById("btn-export-csv");
  const printBtn = document.getElementById("btn-print-laporan");

  if (exportBtn) {
    exportBtn.addEventListener("click", () => {
      const rows = [
        ["Author", "Komentar", "Sentimen", "Tanggal"],
        ...((sentimentData?.sample_comments) || []).map(c => [
          `"${(c.author || '').replace(/"/g, '""')}"`,
          `"${(c.raw_comment || c.comment || '').replace(/"/g, '""')}"`,
          c.sentimen,
          c.tanggal || ""
        ])
      ];
      const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\n");
      const link = document.createElement("a");
      link.setAttribute("href", encodeURI(csvContent));
      link.setAttribute("download", "hasil_sentimen_redenominasi_rupiah.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });
  }

  if (printBtn) {
    printBtn.addEventListener("click", () => window.print());
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
