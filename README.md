# Health Track AI 🩺📊
**Understand Your Lab Reports. See Your Health Trends.**

A local-first, privacy-focused health tracking pipeline built to help individuals and family caregivers build a clear, longitudinal understanding of medical blood-test reports—specifically engineered and benchmarked for **Indian diagnostic lab formats** (Thyrocare, Dr Lal PathLabs, Metropolis).

> ⚠️ **Strictly Educational & Non-Diagnostic:** Organizes and explains recorded lab results only. No medical diagnoses, risk scores, or LLM-generated medical advice.

---

## 🎯 MVP Scope (3-Week Build in Public)
- **Evaluation Before UI:** Synthetic benchmark of 20–30 multi-layout Indian lab PDFs with paired Ground-Truth JSONs to measure exact field-level precision & recall.
- **Hybrid Extraction Pipeline:** Deterministic `pdfplumber` + regex rules first, structured-output LLM fallback second, and strict regex cross-checks so the LLM **never invents a number**.
- **Mandatory Source Verification:** Side-by-side Streamlit UI highlighting the exact extracted value on the original PDF before saving to SQLite.
- **Longitudinal Trends:** Chronological tracking for core MVP biomarkers (**HbA1c, LDL, TSH**) using neutral reference-band wording.

---

## 🏗️ Build Progress
- [x] **Day 1:** Repository setup, Ground-Truth Pydantic schema (`src/schema.py`), Indian lab biomarker alias & unit conversion table (`config/biomarker_aliases.json`), and unit tests (`pytest`).
- [x] **Day 2:** Synthetic Indian lab PDF generator (Thyrocare, Dr Lal PathLabs, Metropolis layouts).
- [x] **Day 3:** Ground-Truth JSON dataset generation & edge-case injection (`<0.5`, `>200`, `DD/MM/YYYY`).


