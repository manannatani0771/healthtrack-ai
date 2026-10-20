import re
from src.schema import ReferenceRange

def parse_reference_interval(raw_text: str) -> ReferenceRange:
    cleaned = raw_text.strip()
    range_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)", cleaned, re.IGNORECASE)
    if range_match:
        return ReferenceRange(raw_text=raw_text, min_val=float(range_match.group(1)), max_val=float(range_match.group(2)))
    lt_match = re.search(r"<\s*=?\s*(\d+(?:\.\d+)?)", cleaned)
    if lt_match:
        return ReferenceRange(raw_text=raw_text, min_val=0.0, max_val=float(lt_match.group(1)))
    gt_match = re.search(r">\s*=?\s*(\d+(?:\.\d+)?)", cleaned)
    if gt_match:
        return ReferenceRange(raw_text=raw_text, min_val=float(gt_match.group(1)), max_val=None)
    return ReferenceRange(raw_text=raw_text, min_val=None, max_val=None)

def normalize_unit(canonical_name: str, numeric_value: float, raw_unit: str) -> tuple[float, str]:
    unit_clean = raw_unit.strip()
    if canonical_name == "LDL":
        if unit_clean.lower() == "mmol/l":
            return round(numeric_value * 38.67, 1), "mg/dL"
        return numeric_value, "mg/dL"
    elif canonical_name == "TSH":
        return numeric_value, "uIU/mL"
    elif canonical_name == "HbA1c":
        return numeric_value, "%"
    return numeric_value, unit_clean
