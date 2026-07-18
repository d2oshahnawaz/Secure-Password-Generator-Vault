# =====================================================
# HISTORY EXPORT
# Version 5.0 Professional
# =====================================================

from __future__ import annotations

import json
from typing import Any, Dict, List

import pandas as pd

from database import get_history

from io import BytesIO

# =====================================================
# CONSTANTS
# =====================================================

EXPORT_COLUMNS = [
    "ID",
    "Password",
    "Strength",
    "Entropy",
    "Crack Time",
    "Created",
]

SUPPORTED_FORMATS = [
    "CSV",
    "TXT",
    "JSON",
    "Excel",
]

# =====================================================
# LOAD HISTORY
# =====================================================

def load_history() -> List[tuple]:
    """
    Load password history from database.
    """

    try:

        history = get_history()

        return history if history else []

    except Exception:

        return []

# =====================================================
# DATAFRAME
# =====================================================

def export_dataframe() -> pd.DataFrame:
    """
    Return history as DataFrame.
    """

    return pd.DataFrame(
        load_history(),
        columns=EXPORT_COLUMNS,
    )

# Backward compatibility
export_csv = export_dataframe

# =====================================================
# TO DICTIONARY
# =====================================================

def history_to_dict() -> List[Dict[str, Any]]:
    """
    Convert database rows into dictionaries.
    """

    records = []

    for row in load_history():

        records.append({

            "id": row[0],

            "password": row[1],

            "strength": row[2],

            "entropy": row[3],

            "crack_time": row[4],

            "created": row[5],

        })

    return records

# =====================================================
# EXPORT JSON
# =====================================================

def export_json() -> str:
    """
    Export history as JSON.
    """

    return json.dumps(
        history_to_dict(),
        indent=4,
        ensure_ascii=False,
    )

# =====================================================
# EXPORT TEXT
# =====================================================

def export_txt() -> str:
    """
    Export history as plain text.
    """

    lines = []

    for item in history_to_dict():

        lines.extend([
            f"Password   : {item['password']}",
            f"Strength   : {item['strength']}",
            f"Entropy    : {item['entropy']}",
            f"Crack Time : {item['crack_time']}",
            f"Created    : {item['created']}",
            "-" * 60,
        ])

    return "\n".join(lines)

# =====================================================
# EXPORT EXCEL
# =====================================================

def export_excel() -> bytes:
    """
    Export history as Microsoft Excel (.xlsx)
    """

    output = BytesIO()

    df = export_dataframe()

    with pd.ExcelWriter(
        output,
        engine="openpyxl",
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Password History",
        )

    output.seek(0)

    return output.getvalue()

# =====================================================
# EXPORT SUMMARY
# =====================================================

def export_summary() -> Dict[str, Any]:
    """
    Return export statistics.
    """

    history = load_history()

    strengths = {}

    for row in history:

        label = row[2]

        strengths[label] = strengths.get(label, 0) + 1

    return {

        "total_passwords": len(history),

        "columns": EXPORT_COLUMNS,

        "formats": SUPPORTED_FORMATS,

        "strength_distribution": strengths,

    }

# =====================================================
# FILE SIZE ESTIMATION
# =====================================================

def estimated_export_size() -> Dict[str, str]:
    """
    Estimate export sizes for all supported formats.
    """

    data = export_dataframe()

    csv_size = len(
        data.to_csv(index=False).encode("utf-8")
    )

    json_size = len(
        export_json().encode("utf-8")
    )

    txt_size = len(
        export_txt().encode("utf-8")
    )

    excel_size = len(
        export_excel()
    )

    return {

        "csv": f"{csv_size:,} bytes",

        "excel": f"{excel_size:,} bytes",

        "json": f"{json_size:,} bytes",

        "txt": f"{txt_size:,} bytes",

    }

# =====================================================
# HISTORY STATISTICS
# =====================================================

def history_statistics() -> Dict[str, Any]:
    """
    Return history analytics.
    """

    df = export_dataframe()

    if df.empty:

        return {

            "total": 0,

            "average_entropy": 0,

            "latest": None,

        }

    return {

        "total": len(df),

        "average_entropy": round(
            df["Entropy"].mean(),
            2,
        ),

        "latest": df.iloc[-1]["Created"],

    }

# =====================================================
# SELF TEST
# =====================================================

if __name__ == "__main__":

    print("=" * 60)

    print("History Export Module")

    print("=" * 60)

    print("Summary")

    print(export_summary())

    print()

    print("Statistics")

    print(history_statistics())

    print()

    print("Estimated Size")

    print(estimated_export_size())

    print()

    print("TXT Preview")

    print(export_txt()[:500])

    print()

    print("JSON Preview")

    print(export_json()[:500])

    print("=" * 60)