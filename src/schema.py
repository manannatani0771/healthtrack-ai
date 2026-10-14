from typing import Optional, List, Literal
from pydantic import BaseModel, Field

class ReferenceRange(BaseModel):
    raw_text: str = Field(..., description="Exact reference interval text printed on the report")
    min_val: Optional[float] = Field(None, description="Parsed lower bound if applicable")
    max_val: Optional[float] = Field(None, description="Parsed upper bound if applicable")

class BiomarkerRecord(BaseModel):
    raw_name: str = Field(..., description="Exact test name as printed on the lab PDF")
    canonical_name: Optional[str] = Field(None, description="Standardized biomarker key, e.g., HbA1c, LDL, TSH")
    raw_value: str = Field(..., description="Exact string value from PDF, e.g., '5.7', '<0.5', '>200'")
    value_operator: Literal["=", "<", ">", "<=", ">="] = Field("=", description="Comparison operator if present")
    numeric_value: float = Field(..., description="Parsed float value for charting and math")
    raw_unit: str = Field(..., description="Exact unit printed on the PDF")
    standard_unit: Optional[str] = Field(None, description="Normalized unit after conversion")
    standard_value: Optional[float] = Field(None, description="Value converted to standard_unit")
    reference_range: ReferenceRange
    method: Optional[str] = Field(None, description="Assay method if printed, e.g., HPLC, Immunoassay, Calculated")
    comparable_flag: bool = Field(True, description="False if method/assay differences prevent direct comparison")
    comparability_note: Optional[str] = Field(None, description="Reason why test may not be directly comparable")
    page_number: int = Field(1, description="1-indexed page number where the row appears")
    source_line_text: Optional[str] = Field(None, description="Raw line text used for anti-hallucination cross-check")

class LabReportGroundTruth(BaseModel):
    report_id: str = Field(..., description="Unique identifier for the report, e.g., syn_thyro_01")
    lab_name: str = Field(..., description="Diagnostic chain, e.g., Thyrocare, Dr Lal PathLabs, Metropolis")
    collection_date: str = Field(..., description="Sample collection date in DD/MM/YYYY format")
    report_date: str = Field(..., description="Report generation date in DD/MM/YYYY format")
    patient_age: Optional[int] = None
    patient_sex: Optional[Literal["M", "F", "Other"]] = None
    biomarkers: List[BiomarkerRecord]
