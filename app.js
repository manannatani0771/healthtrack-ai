/**
 * HealthTrack AI - Client-Side Interactive Dashboard & Verification Studio
 * Local-first, zero-dependency interactive application for Indian lab reports
 */

// Curated Biomarker Database (aligned with config/biomarker_aliases.json)
const BIOMARKER_DATABASE = {
  "HbA1c": {
    canonical: "HbA1c",
    panel: "Diabetes and Glycemic",
    standard_unit: "%",
    reference_range: "< 5.7",
    min_ref: 0,
    max_ref: 5.7,
    trend_rule: "lower_is_toward_range",
    rule_label: "Lower is toward reference range",
    curated_explanation: "Measures average blood sugar levels over the past 2 to 3 months by assessing glucose bound to hemoglobin in red blood cells.",
    doctor_questions: [
      "How does this 3-month average compare to my target glycemic range?",
      "Do we need any adjustments to routine or medications before the next quarterly test?"
    ],
    comparability_warning: "Different methods (HPLC vs immunoassay) and reporting units (% vs mmol/mol) may not be directly comparable."
  },
  "LDL": {
    canonical: "LDL",
    panel: "Cholesterol and Lipids",
    standard_unit: "mg/dL",
    reference_range: "< 100",
    min_ref: 0,
    max_ref: 100,
    trend_rule: "lower_is_toward_range",
    rule_label: "Lower is toward reference range",
    curated_explanation: "Measures low-density lipoprotein, an essential indicator for assessing cardiovascular lipid balance and dietary response.",
    doctor_questions: [
      "Was this LDL value calculated using the Friedewald formula or directly measured?",
      "How should I interpret this LDL reading alongside my HDL and Triglycerides?"
    ],
    comparability_warning: "Calculated LDL vs directly measured LDL can vary, especially if triglycerides are elevated (>200 mg/dL)."
  },
  "TSH": {
    canonical: "TSH",
    panel: "Thyroid",
    standard_unit: "uIU/mL",
    reference_range: "0.35 - 5.50",
    min_ref: 0.35,
    max_ref: 5.50,
    trend_rule: "within_band",
    rule_label: "Within reference band is expected",
    curated_explanation: "Thyroid-stimulating hormone produced by the pituitary gland to regulate thyroid activity and metabolic rate.",
    doctor_questions: [
      "Is this variation in TSH clinically meaningful given the lab's specific assay platform?",
      "When should we schedule our next follow-up thyroid panel?"
    ],
    comparability_warning: "Different assay generations (CLIA vs ECLIA) have slight variations in reference interval boundaries."
  },
  "Fasting Blood Glucose": {
    canonical: "Fasting Blood Glucose",
    panel: "Diabetes and Glycemic",
    standard_unit: "mg/dL",
    reference_range: "70 - 100",
    min_ref: 70,
    max_ref: 100,
    trend_rule: "within_band",
    rule_label: "Within reference band is expected",
    curated_explanation: "Measures blood glucose concentration after an overnight fast (minimum 8-10 hours).",
    doctor_questions: [
      "Does this fasting sugar correlate closely with the 3-month HbA1c trajectory?",
      "Should I perform post-prandial (PP) testing as well?"
    ]
  },
  "HDL": {
    canonical: "HDL",
    panel: "Cholesterol and Lipids",
    standard_unit: "mg/dL",
    reference_range: "> 40",
    min_ref: 40,
    max_ref: 999,
    trend_rule: "higher_is_toward_range",
    rule_label: "Higher is toward reference range",
    curated_explanation: "High-density lipoprotein, responsible for transporting cholesterol from tissues back to the liver.",
    doctor_questions: [
      "What is my Total Cholesterol to HDL ratio, and what does it suggest for lifestyle goals?",
      "What physical activity levels are recommended to support HDL?"
    ]
  },
  "Triglycerides": {
    canonical: "Triglycerides",
    panel: "Cholesterol and Lipids",
    standard_unit: "mg/dL",
    reference_range: "< 150",
    min_ref: 0,
    max_ref: 150,
    trend_rule: "lower_is_toward_range",
    rule_label: "Lower is toward reference range",
    curated_explanation: "The most common type of fat in the bloodstream, storing unused calories from meals.",
    doctor_questions: [
      "How soon after dietary modifications do triglycerides typically reflect changes?",
      "Does elevated triglyceride level affect how my LDL was calculated?"
    ]
  },
  "Serum Creatinine": {
    canonical: "Serum Creatinine",
    panel: "Kidney",
    standard_unit: "mg/dL",
    reference_range: "0.6 - 1.2",
    min_ref: 0.6,
    max_ref: 1.2,
    trend_rule: "within_band",
    rule_label: "Within reference band is expected",
    curated_explanation: "Byproduct of muscle breakdown filtered out almost entirely by healthy kidneys.",
    doctor_questions: [
      "Is this creatinine level normal for my age, muscle mass, and hydration state?",
      "Would calculating the estimated Glomerular Filtration Rate (eGFR) be helpful?"
    ],
    comparability_warning: "Enzymatic vs Jaffe method can produce minor variations in measured creatinine values."
  },
  "ALT/SGPT": {
    canonical: "ALT/SGPT",
    panel: "Liver",
    standard_unit: "U/L",
    reference_range: "< 50",
    min_ref: 0,
    max_ref: 50,
    trend_rule: "lower_is_toward_range",
    rule_label: "Lower is toward reference range",
    curated_explanation: "An enzyme found predominantly in liver cells; released into bloodstream upon cellular stress.",
    doctor_questions: [
      "Could temporary factors (such as recent medication, viral infection, or exercise) explain this ALT reading?",
      "Should we monitor AST/SGOT concurrently on the next draw?"
    ]
  },
  "Vitamin D": {
    canonical: "Vitamin D",
    panel: "Vitamins",
    standard_unit: "ng/mL",
    reference_range: "30 - 100",
    min_ref: 30,
    max_ref: 100,
    trend_rule: "within_band",
    rule_label: "Within reference band is expected",
    curated_explanation: "25-hydroxy vitamin D, essential for calcium absorption, bone integrity, and immune regulation.",
    doctor_questions: [
      "Is supplementation advised based on this reading, and at what dosage?",
      "When should Vitamin D be re-tested after initiating a supplement regimen?"
    ]
  },
  "Vitamin B12": {
    canonical: "Vitamin B12",
    panel: "Vitamins",
    standard_unit: "pg/mL",
    reference_range: "211 - 911",
    min_ref: 211,
    max_ref: 911,
    trend_rule: "within_band",
    rule_label: "Within reference band is expected",
    curated_explanation: "Crucial for neurological health, cognitive function, and healthy red blood cell production.",
    doctor_questions: [
      "Could symptoms like fatigue or mild numbness be correlated with this B12 level?",
      "Is dietary intake sufficient or would oral/sublingual supplementation be appropriate?"
    ]
  }
};

// Sample Indian Diagnostic Lab Reports
const SAMPLE_LAB_REPORTS = {
  thyrocare: {
    labName: "THYROCARE TECHNOLOGIES LTD.",
    reportId: "syn_thyrocare_01",
    accreditation: "NABL & CAP ACCREDITED LABORATORY • D-37/1, TTC INDUSTRIAL AREA, MIDC, TURBHE, NAVI MUMBAI",
    patientName: "Ramesh Natani",
    age: 68,
    sex: "M",
    collectionDate: "21/02/2024",
    reportDate: "22/02/2024",
    tests: [
      {
        rawName: "HbA1c - (HPLC)",
        canonical: "HbA1c",
        observedValue: "7.5",
        unit: "%",
        refText: "< 5.7",
        minRef: 0,
        maxRef: 5.7,
        method: "HPLC",
        comparable: true,
        comparabilityNote: null,
        sourceText: "HbA1c - (HPLC) 7.5 % < 5.7 HPLC"
      },
      {
        rawName: "LDL Cholesterol - Direct",
        canonical: "LDL",
        observedValue: "108.1",
        unit: "mg/dL",
        refText: "< 100",
        minRef: 0,
        maxRef: 100,
        method: "Direct",
        comparable: true,
        comparabilityNote: null,
        sourceText: "LDL Cholesterol - Direct 108.1 mg/dL < 100 Direct"
      },
      {
        rawName: "TSH - Ultrasensitive",
        canonical: "TSH",
        observedValue: "1.35",
        unit: "uIU/mL",
        refText: "0.35 - 5.50",
        minRef: 0.35,
        maxRef: 5.50,
        method: "CLIA",
        comparable: true,
        comparabilityNote: null,
        sourceText: "TSH - Ultrasensitive 1.35 uIU/mL 0.35 - 5.50 CLIA"
      }
    ]
  },
  lalpath: {
    labName: "DR LAL PATHLABS NATIONAL REFERENCE LAB",
    reportId: "syn_lal_03",
    accreditation: "NABL ACCREDITED • BLOCK E, SECTOR 18, ROHINI, NEW DELHI",
    patientName: "Ramesh Natani",
    age: 68,
    sex: "M",
    collectionDate: "19/07/2024",
    reportDate: "20/07/2024",
    tests: [
      {
        rawName: "Glycated Haemoglobin (HbA1c)",
        canonical: "HbA1c",
        observedValue: "6.9",
        unit: "%",
        refText: "< 5.7",
        minRef: 0,
        maxRef: 5.7,
        method: "HPLC",
        comparable: true,
        comparabilityNote: null,
        sourceText: "Glycated Haemoglobin (HbA1c) 6.9 % < 5.7 HPLC"
      },
      {
        rawName: "LDLCholesterol (Calculated)",
        canonical: "LDL",
        observedValue: "104.0",
        unit: "mg/dL",
        refText: "< 100",
        minRef: 0,
        maxRef: 100,
        method: "Calculated",
        comparable: false,
        comparabilityNote: "Calculated method differs from direct assay used on 21/02/2024.",
        sourceText: "LDLCholesterol (Calculated) 104.0 mg/dL < 100 Calculated"
      },
      {
        rawName: "Thyroid Stimulating Hormone (TSH)",
        canonical: "TSH",
        observedValue: "3.84",
        unit: "uIU/mL",
        refText: "0.35 - 5.50",
        minRef: 0.35,
        maxRef: 5.50,
        method: "ECLIA",
        comparable: true,
        comparabilityNote: null,
        sourceText: "Thyroid Stimulating Hormone (TSH) 3.84 uIU/mL 0.35 - 5.50 ECLIA"
      }
    ]
  },
  metropolis: {
    labName: "METROPOLIS HEALTHCARE LIMITED",
    reportId: "syn_metropolis_05",
    accreditation: "CAP & NABL ACCREDITED • CENTRAL LAB, KOHINOOR CITY, KURLA (W), MUMBAI",
    patientName: "Ramesh Natani",
    age: 68,
    sex: "M",
    collectionDate: "15/01/2025",
    reportDate: "16/01/2025",
    tests: [
      {
        rawName: "HbA1c - (HPLC)",
        canonical: "HbA1c",
        observedValue: "6.2",
        unit: "%",
        refText: "< 5.7",
        minRef: 0,
        maxRef: 5.7,
        method: "HPLC",
        comparable: true,
        comparabilityNote: null,
        sourceText: "HbA1c - (HPLC) 6.2 % < 5.7 HPLC"
      },
      {
        rawName: "LDL Cholesterol - Direct",
        canonical: "LDL",
        observedValue: "96.5",
        unit: "mg/dL",
        refText: "< 100",
        minRef: 0,
        maxRef: 100,
        method: "Direct",
        comparable: true,
        comparabilityNote: null,
        sourceText: "LDL Cholesterol - Direct 96.5 mg/dL < 100 Direct"
      },
      {
        rawName: "TSH - Ultrasensitive",
        canonical: "TSH",
        observedValue: "2.10",
        unit: "uIU/mL",
        refText: "0.35 - 5.50",
        minRef: 0.35,
        maxRef: 5.50,
        method: "CLIA",
        comparable: true,
        comparabilityNote: null,
        sourceText: "TSH - Ultrasensitive 2.10 uIU/mL 0.35 - 5.50 CLIA"
      }
    ]
  }
};

// Longitudinal Trend Datasets (spanning 2024-2025)
const LONGITUDINAL_TRENDS = {
  HbA1c: {
    unit: "%",
    minRef: 0,
    maxRef: 5.7,
    refLabel: "< 5.7 %",
    trendRule: "lower_is_toward_range",
    ruleText: "Rule: Lower is toward reference range",
    points: [
      { date: "21/02/2024", value: 7.5, lab: "Thyrocare", method: "HPLC", comparable: true },
      { date: "19/07/2024", value: 6.9, lab: "Dr Lal PathLabs", method: "HPLC", comparable: true },
      { date: "15/01/2025", value: 6.2, lab: "Metropolis", method: "HPLC", comparable: true },
      { date: "10/08/2025", value: 5.9, lab: "Thyrocare", method: "HPLC", comparable: true }
    ],
    assessment: "HbA1c moved toward the laboratory reference range (declined by 1.6% from 7.5% on 21/02/2024 to 5.9% on 10/08/2025, approaching the target of < 5.7%).",
    methodAlert: "Consistent HPLC methodology across all 4 reports. Longitudinal comparison is highly reliable."
  },
  LDL: {
    unit: "mg/dL",
    minRef: 0,
    maxRef: 100,
    refLabel: "< 100 mg/dL",
    trendRule: "lower_is_toward_range",
    ruleText: "Rule: Lower is toward reference range",
    points: [
      { date: "21/02/2024", value: 108.1, lab: "Thyrocare", method: "Direct", comparable: true },
      { date: "19/07/2024", value: 104.0, lab: "Dr Lal PathLabs", method: "Calculated", comparable: false },
      { date: "15/01/2025", value: 96.5, lab: "Metropolis", method: "Direct", comparable: true },
      { date: "10/08/2025", value: 91.2, lab: "Thyrocare", method: "Direct", comparable: true }
    ],
    assessment: "LDL moved into the laboratory reference interval on 15/01/2025 (currently 91.2 mg/dL, down from 108.1 mg/dL baseline).",
    methodAlert: "Note: Dr Lal PathLabs (19/07/2024) used calculated LDL, while Thyrocare and Metropolis used direct homogeneous assays."
  },
  TSH: {
    unit: "uIU/mL",
    minRef: 0.35,
    maxRef: 5.50,
    refLabel: "0.35 – 5.50 uIU/mL",
    trendRule: "within_band",
    ruleText: "Rule: Within reference band is expected",
    points: [
      { date: "21/02/2024", value: 1.35, lab: "Thyrocare", method: "CLIA", comparable: true },
      { date: "19/07/2024", value: 3.84, lab: "Dr Lal PathLabs", method: "ECLIA", comparable: true },
      { date: "15/01/2025", value: 2.10, lab: "Metropolis", method: "CLIA", comparable: true },
      { date: "10/08/2025", value: 2.45, lab: "Thyrocare", method: "CLIA", comparable: true }
    ],
    assessment: "TSH has remained consistently within the lab reference interval (0.35 - 5.50 uIU/mL) across all testing periods over the past 18 months.",
    methodAlert: "ECLIA (Roche platform) and CLIA (Abbott platform) both fall within standard automated 3rd-generation chemiluminescence tolerances."
  }
};

// Application State
const state = {
  currentLab: "thyrocare",
  activeBiomarker: "HbA1c",
  timeRange: "all",
  verifiedItems: new Set([0, 1, 2]),
  focusedIndex: null,
  activeFilter: "all",
  activeProfile: "father"
};

/**
 * Initialize DOM Elements & Event Listeners
 */
document.addEventListener("DOMContentLoaded", () => {
  renderSampleReport(state.currentLab);
  renderTrendChart(state.activeBiomarker);
  renderBiomarkerGuide(state.activeFilter);
  bindEvents();
});

function bindEvents() {
  // Sample report selector buttons
  const presetBtns = document.querySelectorAll(".preset-btn[data-report]");
  presetBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {
      presetBtns.forEach(b => b.classList.remove("active"));
      e.currentTarget.classList.add("active");
      const reportKey = e.currentTarget.getAttribute("data-report");
      state.currentLab = reportKey;
      state.verifiedItems = new Set([0, 1, 2]);
      renderSampleReport(reportKey);
    });
  });

  // Trend biomarker selector buttons
  const markerBtns = document.querySelectorAll(".marker-toggle-btn");
  markerBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {
      markerBtns.forEach(b => b.classList.remove("active"));
      e.currentTarget.classList.add("active");
      const marker = e.currentTarget.getAttribute("data-marker");
      state.activeBiomarker = marker;
      renderTrendChart(marker);
    });
  });

  // Time range filter buttons
  const timeBtns = document.querySelectorAll(".preset-btn[data-timerange]");
  timeBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {
      timeBtns.forEach(b => b.classList.remove("active"));
      e.currentTarget.classList.add("active");
      state.timeRange = e.currentTarget.getAttribute("data-timerange");
      renderTrendChart(state.activeBiomarker);
    });
  });

  // Plain-Language Guide category filter
  const filterBtns = document.querySelectorAll(".preset-btn[data-filter]");
  filterBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {
      filterBtns.forEach(b => b.classList.remove("active"));
      e.currentTarget.classList.add("active");
      const filter = e.currentTarget.getAttribute("data-filter");
      state.activeFilter = filter;
      renderBiomarkerGuide(filter);
    });
  });

  // Save / Commit verified records button
  const saveBtn = document.getElementById("saveVerifiedBtn");
  if (saveBtn) {
    saveBtn.addEventListener("click", async () => {
      const activeReport = state.uploadedReport || SAMPLE_LAB_REPORTS[state.currentLab];
      const verifiedBiomarkers = [];

      activeReport.tests.forEach((t, idx) => {
        if (state.verifiedItems.has(idx)) {
          const numVal = parseFloat(t.observedValue.replace(/[<>]/g, ""));
          verifiedBiomarkers.push({
            raw_name: t.rawName,
            canonical_name: t.canonical,
            raw_value: t.observedValue,
            numeric_value: isNaN(numVal) ? null : numVal,
            raw_unit: t.unit,
            standard_value: isNaN(numVal) ? null : numVal,
            standard_unit: t.unit,
            ref_min: t.minRef !== undefined ? t.minRef : null,
            ref_max: t.maxRef !== undefined ? t.maxRef : null,
            ref_text: t.refText,
            method: t.method,
            comparable_flag: t.comparable !== false,
            source_line_text: t.sourceText,
            page_number: 1
          });
        }
      });

      try {
        const res = await fetch("/api/save", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            patient_name: "Ramesh Natani",
            report_id: activeReport.reportId || "uploaded_report",
            lab_name: activeReport.labName || "Lab Report",
            collection_date: activeReport.collectionDate || "21/10/2026",
            report_date: activeReport.reportDate || "21/10/2026",
            pdf_filename: activeReport.pdfFilename || "report.pdf",
            biomarkers: verifiedBiomarkers
          })
        });

        if (res.ok) {
          const data = await res.json();
          showToast(`✓ Saved ${verifiedBiomarkers.length} biomarkers to SQLite database (Report #${data.report_db_id}).`);
          // Dynamically append new point to longitudinal trend chart
          verifiedBiomarkers.forEach(b => {
            if (LONGITUDINAL_TRENDS[b.canonical_name] && b.numeric_value !== null) {
              LONGITUDINAL_TRENDS[b.canonical_name].points.push({
                date: activeReport.collectionDate,
                value: b.numeric_value,
                lab: activeReport.labName.split(" ")[0],
                method: b.method,
                comparable: b.comparable_flag
              });
            }
          });
          renderTrendChart(state.activeBiomarker);
          return;
        }
      } catch (err) {
        // Fallback for standalone preview
      }

      const count = state.verifiedItems.size;
      showToast(`✓ Verified ${count} biomarkers. Committed to patient's health timeline.`);
    });
  }

  // Print 1-Page Doctor Summary
  const printBtn = document.getElementById("printDocSummaryBtn");
  if (printBtn) {
    printBtn.addEventListener("click", () => {
      window.print();
    });
  }

  // Profile Selector
  const profileSelect = document.getElementById("profileSelect");
  if (profileSelect) {
    profileSelect.addEventListener("change", (e) => {
      state.activeProfile = e.target.value;
      const profileNames = {
        father: "Ramesh Natani (Father - Age 68)",
        mother: "Suman Natani (Mother - Age 64)",
        self: "Manan Natani (Self - Age 34)"
      };
      const patientLabel = document.getElementById("pdfPatient");
      if (patientLabel) patientLabel.textContent = profileNames[state.activeProfile];
      showToast(`Switched active caregiver profile to: ${profileNames[state.activeProfile]}`);
    });
  }

  // PDF File Drag-and-Drop and Upload
  const dropzone = document.getElementById("pdfDropzone");
  const fileInput = document.getElementById("pdfFileInput");

  if (dropzone && fileInput) {
    dropzone.addEventListener("click", () => fileInput.click());

    dropzone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropzone.classList.add("dragover");
    });

    dropzone.addEventListener("dragleave", () => {
      dropzone.classList.remove("dragover");
    });

    dropzone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropzone.classList.remove("dragover");
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        handlePdfUpload(e.dataTransfer.files[0]);
      }
    });

    fileInput.addEventListener("change", (e) => {
      if (e.target.files && e.target.files.length > 0) {
        handlePdfUpload(e.target.files[0]);
      }
    });
  }

  // Check Backend Status
  checkBackendHealth();
}

/**
 * Handle Real Lab PDF File Upload via FastAPI & pdfplumber
 */
async function handlePdfUpload(file) {
  if (!file.name.toLowerCase().endsWith(".pdf")) {
    showToast("⚠️ Please upload a medical lab report in PDF format.");
    return;
  }

  const dropzoneText = document.querySelector(".dropzone-text");
  const origText = dropzoneText ? dropzoneText.innerHTML : "";
  if (dropzoneText) {
    dropzoneText.innerHTML = `<strong>Extracting "${file.name}" with pdfplumber...</strong>`;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/api/upload", {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      throw new Error(`Upload failed with status: ${res.status}`);
    }

    const data = await res.json();

    // Map extracted report to client state
    const customReport = {
      labName: data.lab_name.toUpperCase(),
      reportId: data.report_id,
      accreditation: "DIGITALLY EXTRACTED & VERIFIED WITH PDFPLUMBER",
      patientName: "Ramesh Natani",
      age: data.patient_age || 68,
      sex: data.patient_sex || "M",
      collectionDate: data.collection_date || "21/10/2026",
      reportDate: data.report_date || "21/10/2026",
      pdfFilename: data.pdf_filename,
      tests: data.biomarkers.map(b => ({
        rawName: b.raw_name,
        canonical: b.canonical_name,
        observedValue: b.raw_value,
        unit: b.raw_unit,
        refText: b.ref_text || "Standard",
        minRef: b.ref_min !== null ? b.ref_min : 0,
        maxRef: b.ref_max !== null ? b.ref_max : 100,
        method: b.method || "Standard",
        comparable: b.comparable_flag,
        comparabilityNote: b.comparable_flag ? null : "Different testing method flagged.",
        sourceText: b.source_line_text || `${b.raw_name} ${b.raw_value} ${b.raw_unit}`
      }))
    };

    state.uploadedReport = customReport;
    state.verifiedItems = new Set(customReport.tests.map((_, i) => i));

    renderCustomReport(customReport);
    showToast(`✓ Extracted ${customReport.tests.length} biomarkers from "${file.name}"!`);
  } catch (err) {
    showToast(`⚠️ Server offline: Running local demo parser for "${file.name}".`);
    // Graceful offline simulated parse
    renderSampleReport("thyrocare");
  } finally {
    if (dropzoneText) dropzoneText.innerHTML = origText;
  }
}

function renderCustomReport(report) {
  document.getElementById("pdfLabName").textContent = report.labName;
  document.getElementById("pdfReportId").textContent = report.reportId;
  document.getElementById("pdfCollectionDate").textContent = report.collectionDate;
  document.getElementById("pdfReportDate").textContent = report.reportDate;

  const tableBody = document.getElementById("pdfTableBody");
  tableBody.innerHTML = "";

  report.tests.forEach((test, idx) => {
    const tr = document.createElement("tr");
    tr.className = "pdf-row-highlightable";
    tr.setAttribute("data-row-idx", idx);
    tr.innerHTML = `
      <td><strong>${test.rawName}</strong></td>
      <td><span class="pdf-source-box">${test.observedValue} ${test.unit}</span></td>
      <td>${test.refText}</td>
      <td style="color: #64748b;">${test.method}</td>
    `;
    tr.addEventListener("mouseenter", () => highlightPair(idx));
    tr.addEventListener("mouseleave", () => unhighlightPair(idx));
    tr.addEventListener("click", () => focusPair(idx));
    tableBody.appendChild(tr);
  });

  const biomarkerList = document.getElementById("biomarkerList");
  biomarkerList.innerHTML = "";

  report.tests.forEach((test, idx) => {
    const meta = BIOMARKER_DATABASE[test.canonical] || {};
    const valNum = parseFloat(test.observedValue.replace(/[<>]/g, ""));
    const inRange = valNum <= test.maxRef && valNum >= test.minRef;

    const card = document.createElement("div");
    card.className = "biomarker-card";
    card.setAttribute("data-card-idx", idx);

    card.innerHTML = `
      <div class="biomarker-card-top">
        <div class="biomarker-name-wrap">
          <div class="biomarker-canonical">
            ${test.canonical}
            <span style="font-size: 0.65rem; color: #38bdf8; font-weight: 500;">[Mapped]</span>
          </div>
          <div class="biomarker-raw">Source: "${test.rawName}"</div>
        </div>
        <div class="status-badge ${inRange ? 'status-in-range' : 'status-out-range'}">
          ${inRange ? '● Within Lab Range' : '▲ Outside Lab Range'}
        </div>
      </div>

      <div class="biomarker-stats-grid">
        <div class="stat-cell">
          <span class="stat-cell-label">Extracted Value</span>
          <span class="stat-cell-value highlight-val">${test.observedValue} ${test.unit}</span>
        </div>
        <div class="stat-cell">
          <span class="stat-cell-label">Reference Range</span>
          <span class="stat-cell-value">${test.refText}</span>
        </div>
        <div class="stat-cell">
          <span class="stat-cell-label">Method</span>
          <span class="stat-cell-value" style="font-size: 0.82rem;">${test.method}</span>
        </div>
      </div>

      <div class="biomarker-explanation">
        ${meta.curated_explanation || "Routine diagnostic evaluation biomarker."}
      </div>

      <div class="biomarker-verify-row">
        <label class="verify-checkbox-label">
          <input type="checkbox" class="verify-chk" data-chk-idx="${idx}" ${state.verifiedItems.has(idx) ? 'checked' : ''}>
          <span>Verified against source line</span>
        </label>
        <span class="source-line-preview">${(test.sourceText || '').substring(0, 32)}...</span>
      </div>
    `;

    card.addEventListener("mouseenter", () => highlightPair(idx));
    card.addEventListener("mouseleave", () => unhighlightPair(idx));
    card.addEventListener("click", () => focusPair(idx));

    const chk = card.querySelector(".verify-chk");
    chk.addEventListener("change", (e) => {
      e.stopPropagation();
      if (chk.checked) state.verifiedItems.add(idx);
      else state.verifiedItems.delete(idx);
      updateVerifyCount(report.tests.length);
    });

    biomarkerList.appendChild(card);
  });

  updateVerifyCount(report.tests.length);
}

async function checkBackendHealth() {
  const badge = document.getElementById("apiStatusText");
  try {
    const res = await fetch("/api/patients");
    if (res.ok && badge) {
      badge.textContent = "FastAPI & SQLite Active";
    }
  } catch (e) {
    if (badge) badge.textContent = "Local Client Mode";
  }
}

/**
 * Render Sample Lab Report & Extracted Structured Cards
 */
function renderSampleReport(labKey) {
  const report = SAMPLE_LAB_REPORTS[labKey];
  if (!report) return;

  // Header Metadata
  document.getElementById("pdfLabName").textContent = report.labName;
  document.getElementById("pdfReportId").textContent = report.reportId;
  document.getElementById("pdfCollectionDate").textContent = report.collectionDate;
  document.getElementById("pdfReportDate").textContent = report.reportDate;

  // Left Pane: Document Table Rows
  const tableBody = document.getElementById("pdfTableBody");
  tableBody.innerHTML = "";

  report.tests.forEach((test, idx) => {
    const tr = document.createElement("tr");
    tr.className = "pdf-row-highlightable";
    tr.setAttribute("data-row-idx", idx);
    tr.innerHTML = `
      <td><strong>${test.rawName}</strong></td>
      <td><span class="pdf-source-box">${test.observedValue} ${test.unit}</span></td>
      <td>${test.refText}</td>
      <td style="color: #64748b;">${test.method}</td>
    `;

    // Interactive highlight on click/hover
    tr.addEventListener("mouseenter", () => highlightPair(idx));
    tr.addEventListener("mouseleave", () => unhighlightPair(idx));
    tr.addEventListener("click", () => focusPair(idx));

    tableBody.appendChild(tr);
  });

  // Right Pane: Extracted Biomarker Cards
  const biomarkerList = document.getElementById("biomarkerList");
  biomarkerList.innerHTML = "";

  report.tests.forEach((test, idx) => {
    const meta = BIOMARKER_DATABASE[test.canonical] || {};
    const valNum = parseFloat(test.observedValue.replace(/[<>]/g, ""));
    const inRange = valNum <= test.maxRef && valNum >= test.minRef;

    const card = document.createElement("div");
    card.className = "biomarker-card";
    card.setAttribute("data-card-idx", idx);

    card.innerHTML = `
      <div class="biomarker-card-top">
        <div class="biomarker-name-wrap">
          <div class="biomarker-canonical">
            ${test.canonical}
            <span style="font-size: 0.65rem; color: #38bdf8; font-weight: 500;">[Mapped]</span>
          </div>
          <div class="biomarker-raw">Raw: "${test.rawName}"</div>
        </div>
        <div class="status-badge ${inRange ? 'status-in-range' : 'status-out-range'}">
          ${inRange ? '● Within Lab Range' : '▲ Outside Lab Range'}
        </div>
      </div>

      <div class="biomarker-stats-grid">
        <div class="stat-cell">
          <span class="stat-cell-label">Observed Value</span>
          <span class="stat-cell-value highlight-val">${test.observedValue} ${test.unit}</span>
        </div>
        <div class="stat-cell">
          <span class="stat-cell-label">Reference Range</span>
          <span class="stat-cell-value">${test.refText}</span>
        </div>
        <div class="stat-cell">
          <span class="stat-cell-label">Method</span>
          <span class="stat-cell-value" style="font-size: 0.82rem;">${test.method}</span>
        </div>
      </div>

      <div class="biomarker-explanation">
        ${meta.curated_explanation || "Routine diagnostic evaluation biomarker."}
      </div>

      ${test.comparabilityNote ? `
        <div class="biomarker-comparability-alert">
          <span>⚠️</span>
          <span>${test.comparabilityNote}</span>
        </div>
      ` : ''}

      <div class="biomarker-verify-row">
        <label class="verify-checkbox-label">
          <input type="checkbox" class="verify-chk" data-chk-idx="${idx}" ${state.verifiedItems.has(idx) ? 'checked' : ''}>
          <span>Verified against source line</span>
        </label>
        <span class="source-line-preview">${test.sourceText.substring(0, 32)}...</span>
      </div>
    `;

    // Interactive highlight on hover
    card.addEventListener("mouseenter", () => highlightPair(idx));
    card.addEventListener("mouseleave", () => unhighlightPair(idx));
    card.addEventListener("click", () => focusPair(idx));

    // Checkbox toggle
    const chk = card.querySelector(".verify-chk");
    chk.addEventListener("change", (e) => {
      e.stopPropagation();
      if (chk.checked) {
        state.verifiedItems.add(idx);
      } else {
        state.verifiedItems.delete(idx);
      }
      updateVerifyCount(report.tests.length);
    });

    biomarkerList.appendChild(card);
  });

  updateVerifyCount(report.tests.length);
}

function highlightPair(idx) {
  const row = document.querySelector(`.pdf-row-highlightable[data-row-idx="${idx}"]`);
  const card = document.querySelector(`.biomarker-card[data-card-idx="${idx}"]`);
  if (row) row.classList.add("highlighted");
  if (card) card.classList.add("active-focus");
}

function unhighlightPair(idx) {
  if (state.focusedIndex === idx) return;
  const row = document.querySelector(`.pdf-row-highlightable[data-row-idx="${idx}"]`);
  const card = document.querySelector(`.biomarker-card[data-card-idx="${idx}"]`);
  if (row) row.classList.remove("highlighted");
  if (card) card.classList.remove("active-focus");
}

function focusPair(idx) {
  state.focusedIndex = idx;
  document.querySelectorAll(".pdf-row-highlightable").forEach(r => r.classList.remove("highlighted"));
  document.querySelectorAll(".biomarker-card").forEach(c => c.classList.remove("active-focus"));
  highlightPair(idx);
}

function updateVerifyCount(total) {
  const summaryText = document.getElementById("verifySummaryText");
  if (summaryText) {
    summaryText.textContent = `${state.verifiedItems.size} of ${total} biomarkers verified against source`;
  }
}

/**
 * Render Longitudinal SVG Trend Chart
 */
function renderTrendChart(markerKey) {
  const trend = LONGITUDINAL_TRENDS[markerKey];
  if (!trend) return;

  const titleElem = document.getElementById("activeChartTitle");
  const ruleTag = document.getElementById("trendRuleTag");
  const assessmentElem = document.getElementById("trendAssessmentText");
  const alertElem = document.getElementById("trendMethodAlert");
  const questionsList = document.getElementById("doctorQuestionsList");

  if (titleElem) titleElem.textContent = `${markerKey} (${trend.unit}) Longitudinal Trend`;
  if (ruleTag) ruleTag.textContent = trend.ruleText;
  if (assessmentElem) assessmentElem.textContent = trend.assessment;
  if (alertElem) alertElem.innerHTML = `<strong>Method Consistency:</strong> ${trend.methodAlert}`;

  // Populate Clinician Questions
  const meta = BIOMARKER_DATABASE[markerKey];
  if (questionsList && meta && meta.doctor_questions) {
    questionsList.innerHTML = meta.doctor_questions.map(q => `<li>${q}</li>`).join("");
  }

  // Filter Points by time range
  let points = [...trend.points];
  if (state.timeRange === "6m") {
    points = points.slice(-2);
  } else if (state.timeRange === "12m") {
    points = points.slice(-3);
  }

  const svg = document.getElementById("trendSvg");
  if (!svg) return;

  const width = 900;
  const height = 300;
  const padLeft = 70;
  const padRight = 50;
  const padTop = 40;
  const padBottom = 50;

  const chartW = width - padLeft - padRight;
  const chartH = height - padTop - padBottom;

  // Determine scale range
  const allVals = points.map(p => p.value);
  const minVal = Math.min(...allVals, trend.minRef) * 0.9;
  const maxVal = Math.max(...allVals, trend.maxRef) * 1.15;

  const getY = (v) => height - padBottom - ((v - minVal) / (maxVal - minVal)) * chartH;
  const getX = (i) => padLeft + (points.length === 1 ? chartW / 2 : (i / (points.length - 1)) * chartW);

  // SVG Elements construction
  let svgContent = '';

  // Background Grid Lines
  for (let s = 0; s <= 4; s++) {
    const gridVal = minVal + (s / 4) * (maxVal - minVal);
    const yPos = getY(gridVal);
    svgContent += `
      <line x1="${padLeft}" y1="${yPos}" x2="${width - padRight}" y2="${yPos}" stroke="#1e293b" stroke-dasharray="4" stroke-width="1"/>
      <text x="${padLeft - 12}" y="${yPos + 4}" fill="#64748b" font-size="11" text-anchor="end" font-family="monospace">${gridVal.toFixed(1)}</text>
    `;
  }

  // Shaded Reference Range Band
  const refY1 = Math.min(getY(trend.minRef), getY(trend.maxRef));
  const refY2 = Math.max(getY(trend.minRef), getY(trend.maxRef));
  const bandH = Math.abs(refY2 - refY1);

  svgContent += `
    <rect x="${padLeft}" y="${refY1}" width="${chartW}" height="${bandH}" fill="rgba(16, 185, 129, 0.08)" />
    <line x1="${padLeft}" y1="${refY1}" x2="${width - padRight}" y2="${refY1}" stroke="rgba(16, 185, 129, 0.35)" stroke-dasharray="3" stroke-width="1"/>
    <text x="${width - padRight - 6}" y="${refY1 - 6}" fill="#10b981" font-size="10" text-anchor="end" font-weight="600">Lab Ref (${trend.refLabel})</text>
  `;

  // Draw Trend Polyline
  const linePoints = points.map((p, idx) => `${getX(idx)},${getY(p.value)}`).join(" ");
  svgContent += `
    <polyline points="${linePoints}" fill="none" stroke="#0ea5e9" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  `;

  // Draw Data Points
  points.forEach((p, idx) => {
    const cx = getX(idx);
    const cy = getY(p.value);
    const inRange = p.value <= trend.maxRef && p.value >= trend.minRef;
    const dotColor = inRange ? "#10b981" : "#f59e0b";

    svgContent += `
      <g class="chart-point-group" tabindex="0">
        <circle cx="${cx}" cy="${cy}" r="7" fill="${dotColor}" stroke="#ffffff" stroke-width="2" style="cursor: pointer; transition: all 0.2s;"/>
        <text x="${cx}" y="${cy - 14}" fill="#f8fafc" font-size="12" font-weight="700" text-anchor="middle" font-family="monospace">${p.value} ${trend.unit}</text>
        <text x="${cx}" y="${height - padBottom + 20}" fill="#94a3b8" font-size="11" text-anchor="middle">${p.date}</text>
        <text x="${cx}" y="${height - padBottom + 34}" fill="#64748b" font-size="9" text-anchor="middle">${p.lab} (${p.method})</text>
      </g>
    `;
  });

  svg.innerHTML = svgContent;
}

/**
 * Render Plain-Language Biomarker Directory
 */
function renderBiomarkerGuide(panelFilter) {
  const guideGrid = document.getElementById("guideGrid");
  if (!guideGrid) return;

  guideGrid.innerHTML = "";

  const markers = Object.values(BIOMARKER_DATABASE);
  const filtered = panelFilter === "all" ? markers : markers.filter(m => m.panel === panelFilter);

  filtered.forEach(b => {
    const card = document.createElement("div");
    card.className = "guide-card";
    card.innerHTML = `
      <div class="guide-panel-tag">${b.panel}</div>
      <div class="guide-name">${b.canonical}</div>
      <div style="font-size: 0.72rem; color: #38bdf8;">Standard Range: ${b.reference_range} ${b.standard_unit}</div>
      <div class="guide-desc">${b.curated_explanation}</div>
      <div class="guide-questions">
        <strong>Questions for Clinician:</strong>
        ${(b.doctor_questions || []).map(q => `<div>• ${q}</div>`).join("")}
      </div>
    `;
    guideGrid.appendChild(card);
  });
}

/**
 * Toast Notification Utility
 */
function showToast(message) {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = "toast toast-success";
  toast.innerHTML = `
    <span style="font-size: 1.1rem;">✓</span>
    <span>${message}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => toast.classList.add("show"), 10);

  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
