/* ══════════════════════════════════════════════════════════════
   AI Resume Intelligence — Frontend Logic
   Handles: drag-and-drop, API calls, score animation, typewriter,
            skill badges, PDF download
══════════════════════════════════════════════════════════════ */

const API_BASE = "http://127.0.0.1:5000";

// ── DOM References ─────────────────────────────────────────────
const dropZone      = document.getElementById("drop-zone");
const fileInput     = document.getElementById("file-input");
const fileNameTag   = document.getElementById("file-name");
const jobTextarea   = document.getElementById("job-description");
const analyzeBtn    = document.getElementById("analyze-btn");
const btnText       = document.getElementById("btn-text");
const btnSpinner    = document.getElementById("btn-spinner");

const errorToast    = document.getElementById("error-toast");
const loadingOverlay= document.getElementById("loading-overlay");
const loadingMsg    = document.getElementById("loading-msg");

const emptyState    = document.getElementById("empty-state");
const scoreSection  = document.getElementById("score-section");
const scoreNumber   = document.getElementById("score-number");
const scoreRingFg   = document.getElementById("score-ring-fg");
const scoreBadge    = document.getElementById("score-badge");
const feedbackCard  = document.getElementById("feedback-card");
const feedbackText  = document.getElementById("feedback-text");
const skillsSection = document.getElementById("skills-section");
const matchedWrap   = document.getElementById("matched-wrap");
const missingWrap   = document.getElementById("missing-wrap");
const downloadBtn   = document.getElementById("download-btn");

let selectedFile    = null;
let lastResult      = null;

// ── Drag and Drop ──────────────────────────────────────────────
dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", e => {
  e.preventDefault();
  dropZone.classList.add("drag-over");
});

dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));

dropZone.addEventListener("drop", e => {
  e.preventDefault();
  dropZone.classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file) handleFileSelect(file);
});

fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) handleFileSelect(fileInput.files[0]);
});

function handleFileSelect(file) {
  if (!file.name.toLowerCase().endsWith(".pdf")) {
    showError("⚠️ Only PDF files are supported. Please upload a .pdf file.");
    return;
  }
  selectedFile = file;
  dropZone.classList.add("has-file");
  fileNameTag.style.display = "block";
  fileNameTag.textContent   = `📄 ${file.name}  (${(file.size / 1024).toFixed(1)} KB)`;
  hideError();
}

// ── Analyze ────────────────────────────────────────────────────
analyzeBtn.addEventListener("click", runAnalysis);

async function runAnalysis() {
  hideError();

  if (!selectedFile) {
    showError("Please upload a resume PDF before analyzing.");
    return;
  }
  if (!jobTextarea.value.trim()) {
    showError("Please paste a job description before analyzing.");
    return;
  }

  setLoading(true);
  showLoadingState();

  const formData = new FormData();
  formData.append("resume", selectedFile);
  formData.append("job_description", jobTextarea.value.trim());

  try {
    const messages = [
      "Extracting resume text...",
      "Parsing candidate profile...",
      "Cross-referencing job requirements...",
      "Compiling AI intelligence matrices...",
      "Finalizing ATS score...",
    ];
    let msgIdx = 0;
    const msgTimer = setInterval(() => {
      msgIdx = (msgIdx + 1) % messages.length;
      if (loadingMsg) loadingMsg.textContent = messages[msgIdx];
    }, 1800);

    const response = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      body: formData,
    });

    clearInterval(msgTimer);

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Analysis failed. Please try again.");
    }

    lastResult = data;
    setLoading(false);
    renderResults(data);

  } catch (err) {
    setLoading(false);
    showError(`❌ ${err.message}`);
    showEmptyState();
  }
}

// ── Render Results ─────────────────────────────────────────────
function renderResults(data) {
  const { score, feedback, matched_skills = [], missing_skills = [] } = data;

  // Show containers
  emptyState.style.display    = "none";
  loadingOverlay.style.display= "none";

  scoreSection.style.display  = "block";
  feedbackCard.style.display  = "block";
  skillsSection.style.display = "grid";
  downloadBtn.style.display   = "flex";

  // ── Score Ring ──
  const circumference = 502; // 2π × 80
  const offset = circumference - (score / 100) * circumference;
  const ringColor = score >= 75 ? "#10b981" : score >= 50 ? "#f59e0b" : "#ef4444";

  scoreRingFg.style.stroke = ringColor;

  // Animate dashoffset after a short delay
  requestAnimationFrame(() => {
    setTimeout(() => {
      scoreRingFg.style.strokeDashoffset = offset;
    }, 80);
  });

  // Animate counter
  animateCounter(scoreNumber, 0, score, 1400);

  // Score badge
  const [badgeBg, badgeColor, badgeText] =
    score >= 75
      ? ["rgba(16,185,129,0.15)", "#10b981", "✅ Strong Match"]
      : score >= 50
        ? ["rgba(245,158,11,0.15)", "#f59e0b", "⚠️ Moderate Match"]
        : ["rgba(239,68,68,0.15)",  "#ef4444", "❌ Weak Match"];

  scoreBadge.textContent   = badgeText;
  scoreBadge.style.background  = badgeBg;
  scoreBadge.style.color       = badgeColor;
  scoreBadge.style.border      = `1px solid ${badgeColor}`;

  // ── Feedback Typewriter ──
  feedbackText.textContent = "";
  typeWriter(feedbackText, feedback || "No feedback available.", 14);
  feedbackCard.style.borderLeftColor = ringColor;

  // ── Skill Badges ──
  matchedWrap.innerHTML = "";
  missingWrap.innerHTML = "";

  if (matched_skills.length === 0) {
    matchedWrap.innerHTML = `<span style="color:var(--text-muted);font-size:.82rem;">No matched skills detected.</span>`;
  } else {
    matched_skills.forEach((skill, i) => {
      const b = makeBadge(skill, "badge-match", i * 60);
      matchedWrap.appendChild(b);
    });
  }

  if (missing_skills.length === 0) {
    missingWrap.innerHTML = `<span style="color:var(--text-muted);font-size:.82rem;">No skill gaps — perfect alignment!</span>`;
  } else {
    missing_skills.forEach((skill, i) => {
      const b = makeBadge(skill, "badge-miss", i * 60);
      missingWrap.appendChild(b);
    });
  }
}

// ── Helpers ────────────────────────────────────────────────────
function makeBadge(text, cls, delay) {
  const span = document.createElement("span");
  span.className = `badge ${cls}`;
  span.textContent = text;
  span.style.animationDelay = `${delay}ms`;
  return span;
}

function animateCounter(el, from, to, duration) {
  const start = performance.now();
  const update = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    el.textContent = Math.round(from + (to - from) * eased);
    if (progress < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}

function typeWriter(el, text, speed = 16) {
  let i = 0;
  const tick = () => {
    if (i < text.length) {
      el.textContent += text.charAt(i++);
      setTimeout(tick, speed);
    }
  };
  tick();
}

// ── UI State Helpers ───────────────────────────────────────────
function setLoading(isLoading) {
  analyzeBtn.disabled = isLoading;
  btnSpinner.style.display = isLoading ? "block" : "none";
  btnText.textContent = isLoading ? "Analyzing..." : "⚡ Execute Profile Analysis";
}

function showLoadingState() {
  emptyState.style.display    = "none";
  scoreSection.style.display  = "none";
  feedbackCard.style.display  = "none";
  skillsSection.style.display = "none";
  downloadBtn.style.display   = "none";
  loadingOverlay.style.display= "block";
}

function showEmptyState() {
  loadingOverlay.style.display= "none";
  emptyState.style.display    = "flex";
}

function showError(msg) {
  errorToast.textContent = msg;
  errorToast.style.display = "block";
}

function hideError() {
  errorToast.style.display = "none";
}

// ── PDF Download ───────────────────────────────────────────────
downloadBtn.addEventListener("click", async () => {
  if (!lastResult) return;

  downloadBtn.disabled = true;
  downloadBtn.textContent = "⏳ Generating Report...";

  try {
    const response = await fetch(`${API_BASE}/download-report`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lastResult),
    });

    if (!response.ok) throw new Error("Report generation failed.");

    const blob = await response.blob();
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement("a");
    a.href     = url;
    a.download = "ats_analysis_report.pdf";
    a.click();
    URL.revokeObjectURL(url);

  } catch (err) {
    showError(`❌ ${err.message}`);
  } finally {
    downloadBtn.disabled    = false;
    downloadBtn.innerHTML   = `<span>⬇️</span> Download PDF Report`;
  }
});
