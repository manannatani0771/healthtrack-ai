from pathlib import Path
import pdfplumber
from src.eval.generate_synthetic_reports import generate_dataset
from src.schema import LabReportGroundTruth

def test_synthetic_pdf_and_gt_generation():
    pdf_dir = Path("data/synthetic")
    gt_dir = Path("data/ground_truth")
    reports = generate_dataset(pdf_dir, gt_dir, count_per_lab=8)
    
    # Verify 24 reports across 3 Indian labs (8 each)
    assert len(reports) == 24
    
    sample_pdf = pdf_dir / "syn_thyrocare_01.pdf"
    sample_gt = gt_dir / "syn_thyrocare_01.json"
    assert sample_pdf.exists()
    assert sample_gt.exists()

    # Validate JSON matches our Pydantic Ground-Truth Schema
    gt_data = LabReportGroundTruth.model_validate_json(sample_gt.read_text(encoding="utf-8"))
    assert gt_data.lab_name == "Thyrocare"
    assert len(gt_data.biomarkers) == 3

    # Verify PDF is readable by pdfplumber
    with pdfplumber.open(sample_pdf) as pdf:
        text = pdf.pages[0].extract_text()
        assert "THYROCARE DIAGNOSTICS" in text
        assert "Sample Collection Date:" in text
