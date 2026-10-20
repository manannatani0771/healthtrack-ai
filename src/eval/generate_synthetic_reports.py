import random
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from src.schema import LabReportGroundTruth, BiomarkerRecord
from src.eval.intervals import parse_reference_interval, normalize_unit

LABS = ["Thyrocare", "Dr Lal PathLabs", "Metropolis"]

def generate_dataset(output_pdf_dir: Path, output_gt_dir: Path, count_per_lab: int = 8):
    output_pdf_dir.mkdir(parents=True, exist_ok=True)
    output_gt_dir.mkdir(parents=True, exist_ok=True)
    random.seed(42)
    generated = []

    for lab in LABS:
        for i in range(1, count_per_lab + 1):
            lab_code = lab.lower().split()[0].replace("dr", "lal")
            report_id = f"syn_{lab_code}_{i:02d}"
            day, month, year = random.randint(1, 25), random.randint(1, 12), random.choice([2024, 2025, 2026])
            coll_date, rep_date = f"{day:02d}/{month:02d}/{year}", f"{day+1:02d}/{month:02d}/{year}"
            is_multipage = (i in [7, 8])
            tsh_page = 2 if is_multipage else 1

            hba1c_num = round(random.uniform(4.8, 8.5), 1)
            hba1c_op = "<" if (i == 1 and lab == "Dr Lal PathLabs") else "="
            hba1c_raw = f"<{hba1c_num}" if hba1c_op == "<" else f"{hba1c_num}"
            hba1c_method = "HPLC" if i % 2 == 0 else "Immunoassay"

            use_mmol = (lab == "Metropolis" and i == 4)
            ldl_num = round(random.uniform(2.1, 4.8), 2) if use_mmol else round(random.uniform(75.0, 210.0), 1)
            ldl_unit = "mmol/L" if use_mmol else "mg/dL"
            ldl_ref = "Desirable: < 2.59" if use_mmol else ("Desirable: < 100" if lab == "Dr Lal PathLabs" else "0 - 100")
            ldl_op = ">" if (i == 2 and lab == "Thyrocare") else "="
            ldl_raw = f">{int(ldl_num)}" if ldl_op == ">" else f"{ldl_num}"
            ldl_method = "Calculated" if i % 2 == 0 else "Direct"
            ldl_std_val, ldl_std_unit = normalize_unit("LDL", float(ldl_raw.lstrip("<>")), ldl_unit)

            tsh_num = round(random.uniform(0.4, 7.2), 2)
            tsh_op = "<" if (i == 3 and lab == "Metropolis") else "="
            tsh_raw = f"<{tsh_num}" if tsh_op == "<" else f"{tsh_num}"
            tsh_unit = "mIU/L" if lab == "Metropolis" else "uIU/mL"
            tsh_ref = "Adult: 0.45 - 4.50" if lab == "Dr Lal PathLabs" else "0.35 - 5.50"

            hba1c_name = "HbA1c - (HPLC)" if lab == "Thyrocare" else ("Glycated Haemoglobin (HbA1c)" if lab == "Dr Lal PathLabs" else "Glycosylated Hemoglobin")
            ldl_name = "LDL Cholesterol - Direct" if lab == "Thyrocare" else ("LDLCholesterol (Calculated)" if lab == "Dr Lal PathLabs" else "Low Density Lipoprotein")
            tsh_name = "TSH - Ultrasensitive" if lab == "Thyrocare" else ("Thyroid Stimulating Hormone (TSH)" if lab == "Dr Lal PathLabs" else "TSH")

            records = [
                BiomarkerRecord(raw_name=hba1c_name, canonical_name="HbA1c", raw_value=hba1c_raw, value_operator=hba1c_op, numeric_value=float(hba1c_raw.lstrip("<>")), raw_unit="%", standard_unit="%", standard_value=float(hba1c_raw.lstrip("<>")), reference_range=parse_reference_interval("< 5.7"), method=hba1c_method, comparable_flag=(hba1c_method == "HPLC"), page_number=1, source_line_text=f"{hba1c_name} {hba1c_raw} % < 5.7"),
                BiomarkerRecord(raw_name=ldl_name, canonical_name="LDL", raw_value=ldl_raw, value_operator=ldl_op, numeric_value=float(ldl_raw.lstrip("<>")), raw_unit=ldl_unit, standard_unit=ldl_std_unit, standard_value=ldl_std_val, reference_range=parse_reference_interval(ldl_ref), method=ldl_method, comparable_flag=(ldl_method == "Direct"), page_number=1, source_line_text=f"{ldl_name} {ldl_raw} {ldl_unit} {ldl_ref}"),
                BiomarkerRecord(raw_name=tsh_name, canonical_name="TSH", raw_value=tsh_raw, value_operator=tsh_op, numeric_value=float(tsh_raw.lstrip("<>")), raw_unit=tsh_unit, standard_unit="uIU/mL", standard_value=float(tsh_raw.lstrip("<>")), reference_range=parse_reference_interval(tsh_ref), method="CLIA", comparable_flag=True, page_number=tsh_page, source_line_text=f"{tsh_name} {tsh_raw} {tsh_unit} {tsh_ref}")
            ]

            gt = LabReportGroundTruth(report_id=report_id, lab_name=lab, collection_date=coll_date, report_date=rep_date, patient_age=random.randint(45, 75), patient_sex=random.choice(["M", "F"]), biomarkers=records)
            (output_gt_dir / f"{report_id}.json").write_text(gt.model_dump_json(indent=2), encoding="utf-8")
            render_pdf(gt, output_pdf_dir / f"{report_id}.pdf", is_multipage)
            generated.append(report_id)
    return generated

def _draw_header(c, r, p, tot):
    w, h = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, h - 50, f"{r.lab_name.upper()} DIAGNOSTICS - LABORATORY REPORT")
    c.setFont("Helvetica", 10)
    c.drawString(50, h - 75, f"Report ID: {r.report_id}    Patient Age/Sex: {r.patient_age} Y / {r.patient_sex}")
    c.drawString(50, h - 93, f"Sample Collection Date: {r.collection_date}    Report Date: {r.report_date}")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, h - 123, "TEST NAME                    VALUE      UNIT       REFERENCE RANGE      METHOD")
    c.line(50, h - 138, w - 50, h - 138)
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, 40, f"Note: Please correlate clinically. Page {p} of {tot}")
    return h - 158

def render_pdf(r: LabReportGroundTruth, pdf_path: Path, is_multipage: bool = False):
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    tot = 2 if is_multipage else 1
    for p in range(1, tot + 1):
        if p > 1:
            c.showPage()
        y = _draw_header(c, r, p, tot)
        c.setFont("Helvetica", 10)
        for b in [rec for rec in r.biomarkers if rec.page_number == p]:
            c.drawString(50, y, f"{b.raw_name:<28} {b.raw_value:<10} {b.raw_unit:<10} {b.reference_range.raw_text:<20} {b.method or ''}")
            y -= 20
    c.save()

if __name__ == "__main__":
    created = generate_dataset(Path("data/synthetic"), Path("data/ground_truth"), 8)
    print(f"Day 3 Complete: Regenerated {len(created)} reports (with multi-page & unit edge cases)!")
