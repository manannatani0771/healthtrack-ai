from pathlib import Path
import pdfplumber
from src.eval.intervals import parse_reference_interval, normalize_unit
from src.schema import LabReportGroundTruth

def test_reference_interval_parsing_edge_cases():
    r1 = parse_reference_interval("Desirable: < 100")
    assert r1.min_val == 0.0 and r1.max_val == 100.0
    r2 = parse_reference_interval("Adult: 0.45 - 4.50")
    assert r2.min_val == 0.45 and r2.max_val == 4.50
    r3 = parse_reference_interval("> 60")
    assert r3.min_val == 60.0 and r3.max_val is None

def test_unit_normalization_edge_cases():
    val, unit = normalize_unit("LDL", 3.0, "mmol/L")
    assert unit == "mg/dL" and val == 116.0
    val_tsh, unit_tsh = normalize_unit("TSH", 2.45, "mIU/L")
    assert unit_tsh == "uIU/mL" and val_tsh == 2.45

def test_multipage_pdf_and_ground_truth_alignment():
    pdf_path = Path("data/synthetic/syn_thyrocare_07.pdf")
    gt_path = Path("data/ground_truth/syn_thyrocare_07.json")
    gt = LabReportGroundTruth.model_validate_json(gt_path.read_text(encoding="utf-8"))
    tsh_record = [b for b in gt.biomarkers if b.canonical_name == "TSH"][0]
    assert tsh_record.page_number == 2
    with pdfplumber.open(pdf_path) as pdf:
        assert len(pdf.pages) == 2
        assert "TSH - Ultrasensitive" in pdf.pages[1].extract_text()
