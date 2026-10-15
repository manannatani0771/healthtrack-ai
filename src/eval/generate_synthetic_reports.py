import json
import random
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from src.schema import LabReportGroundTruth, BiomarkerRecord, ReferenceRange

LABS = ["Thyrocare", "Dr Lal PathLabs", "Metropolis"]

def generate_dataset(output_pdf_dir: Path, output_gt_dir: Path, count_per_lab: int = 8):
    output_pdf_dir.mkdir(parents=True, exist_ok=True)
    output_gt_dir.mkdir(parents=True, exist_ok=True)
    random.seed(42)

    generated_reports = []

    for lab_idx, lab in enumerate(LABS):
        for i in range(1, count_per_lab + 1):
            lab_code = lab.lower().split()[0].replace("dr", "lal")
            report_id = f"syn_{lab_code}_{i:02d}"
            
            day = random.randint(1, 25)
            month = random.randint(1, 12)
            year = random.choice([2024, 2025, 2026])
            coll_date = f"{day:02d}/{month:02d}/{year}"
            rep_date = f"{day+1:02d}/{month:02d}/{year}"

            # Generate realistic values with edge cases (<, >)
            hba1c_num = round(random.uniform(4.8, 8.5), 1)
            hba1c_op = "<" if (i == 1 and lab == "Dr Lal PathLabs") else "="
            hba1c_raw = f"<{hba1c_num}" if hba1c_op == "<" else f"{hba1c_num}"
            hba1c_method = "HPLC" if i % 2 == 0 else "Immunoassay"

            ldl_num = round(random.uniform(75.0, 210.0), 1)
            ldl_op = ">" if (i == 2 and lab == "Thyrocare") else "="
            ldl_raw = f">{int(ldl_num)}" if ldl_op == ">" else f"{ldl_num}"
            ldl_method = "Calculated" if i % 2 == 0 else "Direct"

            tsh_num = round(random.uniform(0.4, 7.2), 2)
            tsh_op = "<" if (i == 3 and lab == "Metropolis") else "="
            tsh_raw = f"<{tsh_num}" if tsh_op == "<" else f"{tsh_num}"

            if lab == "Thyrocare":
                records = [
                    BiomarkerRecord(
                        raw_name="HbA1c - (HPLC)" if hba1c_method == "HPLC" else "HBA1C",
                        canonical_name="HbA1c",
                        raw_value=hba1c_raw,
                        value_operator=hba1c_op,
                        numeric_value=float(hba1c_raw.lstrip("<>")),
                        raw_unit="%",
                        standard_unit="%",
                        standard_value=float(hba1c_raw.lstrip("<>")),
                        reference_range=ReferenceRange(raw_text="< 5.7", min_val=0.0, max_val=5.7),
                        method=hba1c_method,
                        comparable_flag=(hba1c_method == "HPLC"),
                        page_number=1,
                        source_line_text=f"HbA1c - (HPLC) | {hba1c_method} | {hba1c_raw} | % | < 5.7"
                    ),
                    BiomarkerRecord(
                        raw_name="LDL Cholesterol - Direct" if ldl_method == "Direct" else "LDL Cholesterol",
                        canonical_name="LDL",
                        raw_value=ldl_raw,
                        value_operator=ldl_op,
                        numeric_value=float(ldl_raw.lstrip("<>")),
                        raw_unit="mg/dL",
                        standard_unit="mg/dL",
                        standard_value=float(ldl_raw.lstrip("<>")),
                        reference_range=ReferenceRange(raw_text="0 - 100", min_val=0.0, max_val=100.0),
                        method=ldl_method,
                        comparable_flag=True,
                        page_number=1,
                        source_line_text=f"LDL Cholesterol | {ldl_method} | {ldl_raw} | mg/dL | 0 - 100"
                    ),
                    BiomarkerRecord(
                        raw_name="TSH - Ultrasensitive",
                        canonical_name="TSH",
                        raw_value=tsh_raw,
                        value_operator=tsh_op,
                        numeric_value=float(tsh_raw.lstrip("<>")),
                        raw_unit="uIU/mL",
                        standard_unit="uIU/mL",
                        standard_value=float(tsh_raw.lstrip("<>")),
                        reference_range=ReferenceRange(raw_text="0.35 - 5.50", min_val=0.35, max_val=5.50),
                        method="CLIA",
                        comparable_flag=True,
                        page_number=1,
                        source_line_text=f"TSH - Ultrasensitive | CLIA | {tsh_raw} | uIU/mL | 0.35 - 5.50"
                    )
                ]
            elif lab == "Dr Lal PathLabs":
                records = [
                    BiomarkerRecord(
                        raw_name="Glycated Haemoglobin (HbA1c)",
                        canonical_name="HbA1c",
                        raw_value=hba1c_raw,
                        value_operator=hba1c_op,
                        numeric_value=float(hba1c_raw.lstrip("<>")),
                        raw_unit="%",
                        standard_unit="%",
                        standard_value=float(hba1c_raw.lstrip("<>")),
                        reference_range=ReferenceRange(raw_text="4.0 - 5.6", min_val=4.0, max_val=5.6),
                        method=hba1c_method,
                        comparable_flag=True,
                        page_number=1,
                        source_line_text=f"Glycated Haemoglobin (HbA1c)   {hba1c_raw}   %   4.0 - 5.6   {hba1c_method}"
                    ),
                    BiomarkerRecord(
                        raw_name="LDLCholesterol (Calculated)" if ldl_method == "Calculated" else "LDL Cholesterol",
                        canonical_name="LDL",
                        raw_value=ldl_raw,
                        value_operator=ldl_op,
                        numeric_value=float(ldl_raw.lstrip("<>")),
                        raw_unit="mg/dL",
                        standard_unit="mg/dL",
                        standard_value=float(ldl_raw.lstrip("<>")),
                        reference_range=ReferenceRange(raw_text="< 100", min_val=0.0, max_val=100.0),
                        method=ldl_method,
                        comparable_flag=(ldl_method == "Direct"),
                        page_number=1,
                        source_line_text=f"LDLCholesterol (Calculated)   {ldl_raw}   mg/dL   < 100   {ldl_method}"
                    ),
                    BiomarkerRecord(
                        raw_name="Thyroid Stimulating Hormone (TSH)",
                        canonical_name="TSH",
                        raw_value=tsh_raw,
                        value_operator=tsh_op,
                        numeric_value=float(tsh_raw.lstrip("<>")),
                        raw_unit="uIU/mL",
                        standard_unit="uIU/mL",
                        standard_value=float(tsh_raw.lstrip("<>")),
                        reference_range=ReferenceRange(raw_text="0.45 - 4.50", min_val=0.45, max_val=4.50),
                        method="ECLIA",
                        comparable_flag=True,
                        page_number=1,
                        source_line_text=f"Thyroid Stimulating Hormone (TSH)   {tsh_raw}   uIU/mL   0.45 - 4.50   ECLIA"
                    )
                ]
            else:  # Metropolis
                records = [
                    BiomarkerRecord(
                        raw_name="Glycosylated Hemoglobin",
                        canonical_name="HbA1c",
                        raw_value=hba1c_raw,
                        value_operator=hba1c_op,
                        numeric_value=float(hba1c_raw.lstrip("<>")),
                        raw_unit="%",
                        standard_unit="%",
                        standard_value=float(hba1c_raw.lstrip("<>")),
                        reference_range=ReferenceRange(raw_text="4.0 - 5.6", min_val=4.0, max_val=5.6),
                        method=hba1c_method,
                        comparable_flag=True,
                        page_number=1,
                        source_line_text=f"Glycosylated Hemoglobin   {hba1c_raw}   %   4.0 - 5.6"
                    ),
                    BiomarkerRecord(
                        raw_name="Low Density Lipoprotein",
                        canonical_name="LDL",
                        raw_value=ldl_raw,
                        value_operator=ldl_op,
                        numeric_value=float(ldl_raw.lstrip("<>")),
                        raw_unit="mg/dL",
                        standard_unit="mg/dL",
                        standard_value=float(ldl_raw.lstrip("<>")),
                        reference_range=ReferenceRange(raw_text="0 - 99", min_val=0.0, max_val=99.0),
                        method=ldl_method,
                        comparable_flag=True,
                        page_number=1,
                        source_line_text=f"Low Density Lipoprotein   {ldl_raw}   mg/dL   0 - 99"
                    ),
                    BiomarkerRecord(
                        raw_name="TSH",
                        canonical_name="TSH",
                        raw_value=tsh_raw,
                        value_operator=tsh_op,
                        numeric_value=float(tsh_raw.lstrip("<>")),
                        raw_unit="mIU/L",
                        standard_unit="uIU/mL",
                        standard_value=float(tsh_raw.lstrip("<>")),
                        reference_range=ReferenceRange(raw_text="0.27 - 4.20", min_val=0.27, max_val=4.20),
                        method="CMIA",
                        comparable_flag=True,
                        page_number=1,
                        source_line_text=f"TSH   {tsh_raw}   mIU/L   0.27 - 4.20"
                    )
                ]

            gt_report = LabReportGroundTruth(
                report_id=report_id,
                lab_name=lab,
                collection_date=coll_date,
                report_date=rep_date,
                patient_age=random.randint(45, 75),
                patient_sex=random.choice(["M", "F"]),
                biomarkers=records
            )

            # Save Ground-Truth JSON
            gt_path = output_gt_dir / f"{report_id}.json"
            with open(gt_path, "w", encoding="utf-8") as f:
                f.write(gt_report.model_dump_json(indent=2))

            # Render Synthetic PDF
            pdf_path = output_pdf_dir / f"{report_id}.pdf"
            render_pdf(gt_report, pdf_path)
            generated_reports.append(report_id)

    return generated_reports

def render_pdf(report: LabReportGroundTruth, pdf_path: Path):
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"{report.lab_name.upper()} DIAGNOSTICS - LABORATORY REPORT")
    y -= 25

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Report ID: {report.report_id}    Patient Age/Sex: {report.patient_age} Y / {report.patient_sex}")
    y -= 18
    c.drawString(50, y, f"Sample Collection Date: {report.collection_date}    Report Date: {report.report_date}")
    y -= 30

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "TEST NAME                    VALUE      UNIT       REFERENCE RANGE      METHOD")
    y -= 15
    c.line(50, y, width - 50, y)
    y -= 20

    c.setFont("Helvetica", 10)
    for b in report.biomarkers:
        line = f"{b.raw_name:<28} {b.raw_value:<10} {b.raw_unit:<10} {b.reference_range.raw_text:<20} {b.method or ''}"
        c.drawString(50, y, line)
        y -= 20

    c.save()

if __name__ == "__main__":
    pdfs = Path("data/synthetic")
    gts = Path("data/ground_truth")
    created = generate_dataset(pdfs, gts, count_per_lab=8)
    print(f"Successfully generated {len(created)} synthetic Indian lab PDFs and Ground-Truth JSONs!")
