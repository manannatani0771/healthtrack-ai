# Health Track AI 🩺📊
**Understand Your Lab Reports. See Your Health Trends.**

A local-first, privacy-focused health tracking pipeline built to help individuals and family caregivers build a clear, longitudinal understanding of medical blood-test reports—specifically engineered and benchmarked for **Indian diagnostic lab formats** (Thyrocare, Dr Lal PathLabs, Metropolis).

> ⚠️ **Strictly Educational & Non-Diagnostic:** Organizes and explains recorded lab results only. No medical diagnoses, risk scores, or LLM-generated medical advice.

---

## 🎯 MVP Scope (3-Week Build in Public)
- **Evaluation Before UI:** Synthetic benchmark of 24 multi-layout Indian lab PDFs with paired Ground-Truth JSONs to measure exact field-level precision & recall.
- **Hybrid Extraction Pipeline:** Deterministic `pdfplumber` + regex rules first, structured-output LLM fallback second, and strict regex cross-checks so the LLM **never invents a number**.
- **Mandatory Source Verification:** Side-by-side verification studio highlighting the exact extracted value on the original PDF before committing to SQLite.
- **Longitudinal Trends:** Chronological tracking for core MVP biomarkers (**HbA1c, LDL, TSH**) using neutral reference-band wording.
- **Doctor-Ready Export:** 1-page printable consultation summary scannable in 30 seconds.

---

## 🏗️ Build Progress
- [x] **Day 1:** Repository setup, Ground-Truth Pydantic schema (`src/schema.py`), Indian lab biomarker alias & unit conversion table (`config/biomarker_aliases.json`), and unit tests (`pytest`).
- [x] **Day 2:** Synthetic Indian lab PDF generator (`src/eval/generate_synthetic_reports.py`) covering Thyrocare, Dr Lal PathLabs, and Metropolis layouts.
- [x] **Day 3:** Ground-Truth JSON dataset generation & edge-case injection (`<0.5`, `>200`, `DD/MM/YYYY`, calculated vs direct LDL).
- [x] **Day 4:** Deterministic `pdfplumber` regex extractor (`src/parser/rule_extractor.py`) and benchmark scorecard (100% date accuracy, 98.4%+ field precision).
- [x] **Day 5:** Interactive caregiver web dashboard: side-by-side source verification studio, longitudinal trend charts (HbA1c, LDL, TSH), and printable 1-page doctor consultation summary.
- [x] **Day 6:** Full-stack dynamic FastAPI backend (`src/server.py`), SQLite persistence (`data/healthtrack.db`), drag-and-drop PDF parser, and safe `.env` secret management.

---

## ⚡ Quickstart (Run Locally)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Application
Run the one-command launcher:
```bash
python run.py
```
This automatically initializes the local SQLite database (`data/healthtrack.db`), starts the FastAPI server at `http://127.0.0.1:8000`, and opens the dashboard in your default web browser.

---

## 🔒 Security & Privacy Architecture
- **DPDP Act Principles:** Medical reports remain entirely on your local machine. No health records are sent to external cloud servers or used for model training.
- **Zero API Costs:** The primary extraction engine runs locally on CPU using `pdfplumber` (₹0.00 / $0.00 per report).
- **Safe Secret Management:** API credentials (if using optional cloud LLM fallback) are stored in `.env`, strictly excluded from git via `.gitignore`. A safe [`.env.example`](.env.example) is provided as a template.

---

## 📊 Published Benchmark Scorecard

| Metric | Score | Notes |
| :--- | :---: | :--- |
| **Reports Evaluated** | **24** | Multi-page reports across Thyrocare, Lal PathLabs, Metropolis |
| **Collection Date Accuracy** | **100.0%** | Standardized Indian `DD/MM/YYYY` formats |
| **Field-Level Precision** | **98.4%** | Test name, observed value, unit, and reference interval |
| **Field-Level Recall** | **98.4%** | Zero missed biomarkers across MVP panels |
| **Number Hallucinations** | **0** | Strict regex cross-validation against raw document stream |

Run the benchmark scorecard anytime:
```bash
python -m src.eval.evaluate_benchmark
```

---

## 📁 Repository Structure
```text
healthtrack-ai/
├── config/
│   └── biomarker_aliases.json      # Indian lab aliases, units & curated text
├── data/
│   ├── ground_truth/               # 24 benchmark ground-truth JSONs
│   ├── synthetic/                  # 24 synthetic multi-layout Indian lab PDFs
│   └── healthtrack.db              # Local SQLite database (ignored by git)
├── src/
│   ├── db/
│   │   └── database.py             # SQLite schema and query interface
│   ├── eval/
│   │   ├── evaluate_benchmark.py   # Benchmark evaluation script
│   │   └── generate_synthetic.py   # Synthetic Indian report generator
│   ├── parser/
│   │   └── rule_extractor.py       # Deterministic pdfplumber regex extractor
│   ├── schema.py                   # Pydantic data models
│   └── server.py                   # FastAPI REST API & static file server
├── app.js                          # Client-side dynamic interactivity
├── index.html                      # Verification studio & longitudinal dashboard
├── run.py                          # 1-command server launcher
├── styles.css                      # Clinical design system & print stylesheet
├── requirements.txt                # Python dependencies
└── .env.example                    # Environment secrets template
```

---

## 📄 License & Disclaimer
This project is licensed under the MIT License. **Strictly educational and non-diagnostic.** Always consult a qualified clinician regarding personal medical decisions.
