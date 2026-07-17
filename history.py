# =====================================================
# HISTORY EXPORT
# Version 4.0 Professional
# =====================================================

from __future__ import annotations

import json
from typing import Any, Dict, List

import pandas as pd

from database import get_history

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

# =====================================================
# LOAD HISTORY
# =====================================================

def load_history() -> List[tuple]:
    """
    Load password history from the database.
    """

    history = get_history()

    return history if history else []


# =====================================================
# CONVERT TO DATAFRAME
# =====================================================

def export_csv() -> pd.DataFrame:
    """
    Export history as a Pandas DataFrame.
    """

    return pd.DataFrame(

        load_history(),

        columns=EXPORT_COLUMNS,

    )


# =====================================================
# CONVERT TO DICTIONARY
# =====================================================

def history_to_dict() -> List[Dict[str, Any]]:
    """
    Convert database rows into dictionaries.
    """

    data: List[Dict[str, Any]] = []

    for row in load_history():

        data.append({

            "id": row[0],

            "password": row[1],

            "strength": row[2],

            "entropy": row[3],

            "crack_time": row[4],

            "created": row[5],

        })

    return data


# =====================================================
# EXPORT AS TEXT
# =====================================================

def export_txt() -> str:
    """
    Export history as plain text.
    """

    records = []

    for item in history_to_dict():

        records.append(

            "\n".join([

                f"Password   : {item['password']}",

                f"Strength   : {item['strength']}",

                f"Entropy    : {item['entropy']}",

                f"Crack Time : {item['crack_time']}",

                f"Created    : {item['created']}",

                "-" * 50,

            ])

        )

    return "\n".join(records)


# =====================================================
# EXPORT AS JSON
# =====================================================

def export_json() -> str:
    """
    Export history as formatted JSON.
    """

    return json.dumps(

        history_to_dict(),

        indent=4,

        ensure_ascii=False,

    )


# =====================================================
# EXPORT SUMMARY
# =====================================================

def export_summary() -> Dict[str, Any]:
    """
    Return export statistics.
    """

    history = load_history()

    return {

        "total_passwords": len(history),

        "columns": EXPORT_COLUMNS,

        "formats": [

            "CSV",

            "TXT",

            "JSON",

        ],

    }


# =====================================================
# SELF TEST
# =====================================================

if __name__ == "__main__":

    print("=" * 60)

    print("History Export Module")

    print("=" * 60)

    print(export_summary())

    print()

    print(export_txt()[:500])

    print()

    print(export_json()[:500])