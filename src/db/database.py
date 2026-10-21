import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional

DB_PATH = Path("data/healthtrack.db")

def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: Path = DB_PATH) -> None:
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        sex TEXT,
        relationship TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS lab_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        report_id TEXT NOT NULL,
        lab_name TEXT,
        collection_date TEXT,
        report_date TEXT,
        pdf_filename TEXT,
        verified INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    );

    CREATE TABLE IF NOT EXISTS biomarkers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_id INTEGER,
        raw_name TEXT,
        canonical_name TEXT,
        raw_value TEXT,
        numeric_value REAL,
        raw_unit TEXT,
        standard_value REAL,
        standard_unit TEXT,
        ref_min REAL,
        ref_max REAL,
        ref_text TEXT,
        method TEXT,
        comparable_flag INTEGER DEFAULT 1,
        source_line_text TEXT,
        page_number INTEGER DEFAULT 1,
        verified INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (report_id) REFERENCES lab_reports(id)
    );
    """)

    # Pre-populate default profiles if table is empty
    cursor.execute("SELECT COUNT(*) FROM patients")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO patients (name, age, sex, relationship) VALUES ('Ramesh Natani', 68, 'M', 'Father')")
        cursor.execute("INSERT INTO patients (name, age, sex, relationship) VALUES ('Suman Natani', 64, 'F', 'Mother')")
        cursor.execute("INSERT INTO patients (name, age, sex, relationship) VALUES ('Manan Natani', 34, 'M', 'Self')")

    conn.commit()
    conn.close()

def save_verified_report(patient_name: str, report_data: Dict[str, Any], biomarkers: List[Dict[str, Any]]) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    # Find or insert patient
    cursor.execute("SELECT id FROM patients WHERE name = ?", (patient_name,))
    row = cursor.fetchone()
    if row:
        patient_id = row["id"]
    else:
        cursor.execute("INSERT INTO patients (name, age, sex, relationship) VALUES (?, ?, ?, ?)",
                       (patient_name, report_data.get("age", 0), report_data.get("sex", "U"), "Family"))
        patient_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO lab_reports (patient_id, report_id, lab_name, collection_date, report_date, pdf_filename, verified)
    VALUES (?, ?, ?, ?, ?, ?, 1)
    """, (
        patient_id,
        report_data.get("report_id", "manual_entry"),
        report_data.get("lab_name", "Unknown"),
        report_data.get("collection_date", ""),
        report_data.get("report_date", ""),
        report_data.get("pdf_filename", "")
    ))
    report_db_id = cursor.lastrowid

    for b in biomarkers:
        cursor.execute("""
        INSERT INTO biomarkers (
            report_id, raw_name, canonical_name, raw_value, numeric_value,
            raw_unit, standard_value, standard_unit, ref_min, ref_max,
            ref_text, method, comparable_flag, source_line_text, page_number, verified
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            report_db_id,
            b.get("raw_name"),
            b.get("canonical_name"),
            b.get("raw_value"),
            b.get("numeric_value"),
            b.get("raw_unit"),
            b.get("standard_value"),
            b.get("standard_unit"),
            b.get("ref_min"),
            b.get("ref_max"),
            b.get("ref_text"),
            b.get("method"),
            1 if b.get("comparable_flag", True) else 0,
            b.get("source_line_text"),
            b.get("page_number", 1)
        ))

    conn.commit()
    conn.close()
    return report_db_id

def get_longitudinal_trends(patient_name: str, canonical_name: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        r.collection_date,
        r.lab_name,
        b.canonical_name,
        b.numeric_value,
        b.standard_value,
        b.standard_unit,
        b.ref_min,
        b.ref_max,
        b.ref_text,
        b.method,
        b.comparable_flag
    FROM biomarkers b
    JOIN lab_reports r ON b.report_id = r.id
    JOIN patients p ON r.patient_id = p.id
    WHERE p.name = ? AND b.canonical_name = ?
    ORDER BY r.collection_date ASC
    """, (patient_name, canonical_name))

    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_reports(patient_name: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()

    if patient_name:
        cursor.execute("""
        SELECT r.*, p.name as patient_name, count(b.id) as biomarker_count
        FROM lab_reports r
        JOIN patients p ON r.patient_id = p.id
        LEFT JOIN biomarkers b ON b.report_id = r.id
        WHERE p.name = ?
        GROUP BY r.id
        ORDER BY r.created_at DESC
        """, (patient_name,))
    else:
        cursor.execute("""
        SELECT r.*, p.name as patient_name, count(b.id) as biomarker_count
        FROM lab_reports r
        JOIN patients p ON r.patient_id = p.id
        LEFT JOIN biomarkers b ON b.report_id = r.id
        GROUP BY r.id
        ORDER BY r.created_at DESC
        """)

    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
