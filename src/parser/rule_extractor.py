import json
import re
from pathlib import Path
import pdfplumber
from src.schema import LabReportGroundTruth, BiomarkerRecord
from src.eval.intervals import parse_reference_interval, normalize_unit

ALIAS_PATH = Path("config/biomarker_aliases.json")

def load_aliases() -> dict:
    return json.loads(ALIAS_PATH.read_text(encoding="utf-8"))

def extract_report_deterministic(pdf_path: Path) -> LabReportGroundTruth:
    aliases_cfg = load_aliases()
    report_id = pdf_path.stem
    lab_name = "Unknown"
    coll_date = "01/01/1970"
    rep_date = "01/01/1970"
    age = 0
    sex = "U"
    biomarkers = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            for line in text.splitlines():
                line_str = line.strip()
                if not line_str:
                    continue

                if page_idx == 1:
                    if "THYROCARE" in line_str.upper():
                        lab_name = "Thyrocare"
                    elif "DR LAL PATHLABS" in line_str.upper():
                        lab_name = "Dr Lal PathLabs"
                    elif "METROPOLIS" in line_str.upper():
                        lab_name = "Metropolis"

                    age_sex = re.search(r"Patient Age/Sex:\s*(\d+)\s*Y\s*/\s*([MF])", line_str)
                    if age_sex:
                        age, sex = int(age_sex.group(1)), age_sex.group(2)

                    dates = re.search(r"Sample Collection Date:\s*(\d{2}/\d{2}/\d{4})\s+Report Date:\s*(\d{2}/\d{2}/\d{4})", line_str)
                    if dates:
                        coll_date, rep_date = dates.group(1), dates.group(2)

                if any(h in line_str for h in ["TEST NAME", "DIAGNOSTICS -", "Report ID:", "Sample Collection Date:", "Note: Please correlate"]):
                    continue

                row_match = re.match(
                    r"^(.+?)\s+([<>]?\d+(?:\.\d+)?)\s+(%|mg/dL|mmol/L|uIU/mL|mIU/L)\s+(.+?)(?:\s+(HPLC|Immunoassay|Calculated|Direct|CLIA|ECLIA|CMIA))?$",
                    line_str
                )
                if row_match:
                    raw_name = row_match.group(1).strip()
                    raw_val = row_match.group(2).strip()
                    raw_unit = row_match.group(3).strip()
                    ref_str = row_match.group(4).strip()
                    method = row_match.group(5).strip() if row_match.group(5) else None

                    canonical = None
                    for canon_key, meta in aliases_cfg.items():
                        for alias in sorted(meta["aliases"], key=len, reverse=True):
                            if raw_name.lower() == alias.lower() or alias.lower() in raw_name.lower():
                                canonical = canon_key
                                break
                        if canonical:
                            break

                    if not canonical:
                        continue

                    val_op = "<" if raw_val.startswith("<") else (">" if raw_val.startswith(">") else "=")
                    num_val = float(raw_val.lstrip("<>"))
                    std_val, std_unit = normalize_unit(canonical, num_val, raw_unit)
                    ref_range = parse_reference_interval(ref_str)

                    if canonical == "HbA1c":
                        comp = (method == "HPLC")
                    elif canonical == "LDL":
                        comp = (method == "Direct")
                    else:
                        comp = True

                    biomarkers.append(
                        BiomarkerRecord(
                            raw_name=raw_name,
                            canonical_name=canonical,
                            raw_value=raw_val,
                            value_operator=val_op,
                            numeric_value=num_val,
                            raw_unit=raw_unit,
                            standard_unit=std_unit,
                            standard_value=std_val,
                            reference_range=ref_range,
                            method=method,
                            comparable_flag=comp,
                            page_number=page_idx,
                            source_line_text=line_str
                        )
                    )

    return LabReportGroundTruth(
        report_id=report_id,
        lab_name=lab_name,
        collection_date=coll_date,
        report_date=rep_date,
        patient_age=age,
        patient_sex=sex,
        biomarkers=biomarkers
    )
