import json
from pathlib import Path
from src.schema import LabReportGroundTruth, BiomarkerRecord, ReferenceRange

def test_ground_truth_schema_validation():
    sample_record = BiomarkerRecord(
        raw_name="Glycated Haemoglobin (HbA1c)",
        canonical_name="HbA1c",
        raw_value="<5.7",
        value_operator="<",
        numeric_value=5.7,
        raw_unit="%",
        standard_unit="%",
        standard_value=5.7,
        reference_range=ReferenceRange(raw_text="< 5.7", min_val=0.0, max_val=5.7),
        method="HPLC",
        comparable_flag=True,
        page_number=1,
        source_line_text="Glycated Haemoglobin (HbA1c)   <5.7   %   < 5.7   HPLC"
    )

    report = LabReportGroundTruth(
        report_id="syn_lal_001",
        lab_name="Dr Lal PathLabs",
        collection_date="14/10/2026",
        report_date="15/10/2026",
        patient_age=58,
        patient_sex="M",
        biomarkers=[sample_record]
    )

    assert report.lab_name == "Dr Lal PathLabs"
    assert report.biomarkers[0].canonical_name == "HbA1c"
    assert report.biomarkers[0].value_operator == "<"

def test_aliases_json_loads():
    alias_path = Path("config") / "biomarker_aliases.json"
    with open(alias_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "HbA1c" in data
    assert "LDL" in data
    assert "TSH" in data
