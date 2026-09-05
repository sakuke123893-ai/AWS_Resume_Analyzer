# ⚡ AI Resume Intelligence Dashboard

An enterprise-grade **ATS Resume Analyzer** powered by **Groq LLaMA 3.3 70B** — rebuilt as a premium full-stack web application with a stunning custom UI.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?style=flat-square&logo=flask)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

- 📄 **Drag & Drop PDF Upload** — No plain file browser buttons
- 🎯 **ATS Match Scoring** — AI-powered 0–100% score against any job description
- 🔄 **Animated Score Ring** — SVG circular meter that fills up live
- 💡 **Typewriter AI Feedback** — Actionable resume improvement advice
- ✅ **Skill Gap Analysis** — Matched vs. missing skills with animated badges
- ⬇️ **Download PDF Report** — Full styled analysis report via ReportLab
- 🌙 **Dark Glassmorphism UI** — Premium design with Inter font & smooth animations

---

## 🗂️ Project Structure

```
AWS_Resume_Analyzer/
│
├── backend/
│   ├── app.py               ← Flask REST API
│   ├── report_generator.py  ← PDF report generation (ReportLab)
│   └── requirements.txt     ← Python dependencies
│
├── frontend/
│   ├── index.html           ← Single Page Application
│   ├── style.css            ← Dark glassmorphism design system
│   └── script.js            ← Drag-drop, animations, fetch API
│
├── .env.example             ← API key template
├── run.ps1                  ← One-click Windows launcher
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/sakuke123893-ai/AWS_Resume_Analyzer.git
cd AWS_Resume_Analyzer
```

### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Set Up Your API Key
Get a **free** Groq API key at [console.groq.com](https://console.groq.com)

```bash
# Windows
copy .env.example .env
# Then open .env and replace `your_groq_api_key_here` with your real key
```

### 4. Run the App
```bash
python backend/app.py
```

Open your browser at **[http://localhost:5000](http://localhost:5000)**

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12 + Flask |
| AI Model | Groq LLaMA 3.3 70B (free) |
| PDF Parsing | pypdf |
| PDF Reports | ReportLab |
| Frontend | Vanilla HTML + CSS + JavaScript |
| Design | Dark Glassmorphism + Inter Font |

---

## 📌 Notes

- Only **PDF** resumes are supported (text-based, not scanned)
- Your API key is stored locally in `.env` and **never pushed to GitHub**
- The Groq API is **completely free** with generous rate limits

---

> Built with ❤️ using Groq's blazing-fast inference API
