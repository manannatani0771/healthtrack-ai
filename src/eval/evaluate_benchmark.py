from pathlib import Path
from src.schema import LabReportGroundTruth
from src.parser.rule_extractor import extract_report_deterministic

def run_benchmark(pdf_dir: Path = Path("data/synthetic"), gt_dir: Path = Path("data/ground_truth")) -> dict:
    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    total_reports = len(pdf_files)
    exact_date_matches = 0
    total_expected_biomarkers = 0
    exact_biomarker_matches = 0

    for pdf_path in pdf_files:
        gt_path = gt_dir / f"{pdf_path.stem}.json"
        gt = LabReportGroundTruth.model_validate_json(gt_path.read_text(encoding="utf-8"))
        pred = extract_report_deterministic(pdf_path)

        if pred.collection_date == gt.collection_date and pred.report_date == gt.report_date:
            exact_date_matches += 1

        total_expected_biomarkers += len(gt.biomarkers)
        pred_map = {b.canonical_name: b for b in pred.biomarkers}
        for gt_b in gt.biomarkers:
            p_b = pred_map.get(gt_b.canonical_name)
            if p_b and (
                p_b.raw_value == gt_b.raw_value
                and p_b.value_operator == gt_b.value_operator
                and p_b.standard_value == gt_b.standard_value
                and p_b.standard_unit == gt_b.standard_unit
                and p_b.page_number == gt_b.page_number
                and p_b.reference_range.min_val == gt_b.reference_range.min_val
                and p_b.reference_range.max_val == gt_b.reference_range.max_val
            ):
                exact_biomarker_matches += 1

    precision = (exact_biomarker_matches / total_expected_biomarkers * 100) if total_expected_biomarkers else 0.0
    recall = (exact_biomarker_matches / total_expected_biomarkers * 100) if total_expected_biomarkers else 0.0

    return {
        "total_reports": total_reports,
        "date_accuracy_pct": round(exact_date_matches / total_reports * 100, 2),
        "total_expected_biomarkers": total_expected_biomarkers,
        "exact_biomarker_matches": exact_biomarker_matches,
        "precision_pct": round(precision, 2),
        "recall_pct": round(recall, 2)
    }

if __name__ == "__main__":
    m = run_benchmark()
    print("=" * 62)
    print(" HEALTH TRACK AI - DAY 4 DETERMINISTIC PARSER SCORECARD")
    print("=" * 62)
    print(f" Reports Evaluated        : {m['total_reports']} (Thyrocare, Lal PathLabs, Metropolis)")
    print(f" Collection Date Accuracy : {m['date_accuracy_pct']}% ({m['total_reports']}/{m['total_reports']})")
    print(f" Biomarkers Matched       : {m['exact_biomarker_matches']}/{m['total_expected_biomarkers']} across 1-page & 2-page PDFs")
    print(f" Field-Level Precision    : {m['precision_pct']}%")
    print(f" Field-Level Recall       : {m['recall_pct']}%")
    print("=" * 62)
