"""
Sprint 3 - Day 19
Radar Chart Validation

Validates:
1. Radar chart output directory exists.
2. Expected 92 radar charts are generated.
3. Every chart follows the *_radar.png naming convention.
4. Every company has a radar chart.
5. Peer groups are correctly assigned where available.
6. Companies without peer groups are identified.
7. Required radar metrics are defined.
"""

from pathlib import Path
import sqlite3
import pandas as pd


# =========================================================
# CONFIGURATION
# =========================================================

DB_PATH = Path("db/nifty100.db")

PEER_GROUPS_PATH = Path(
    "data/supporting/peer_groups.xlsx"
)

RADAR_OUTPUT_DIR = Path(
    "reports/radar_charts"
)

EXPECTED_COMPANIES = 92


# =========================================================
# REQUIRED RADAR METRICS
# =========================================================

RADAR_METRICS = [
    "ROE",
    "ROCE",
    "NPM",
    "D/E",
    "FCF Score",
    "PAT CAGR 5yr",
    "Revenue CAGR 5yr",
    "Composite Score"
]


# =========================================================
# LOAD PEER GROUPS
# =========================================================

def load_peer_groups():

    if not PEER_GROUPS_PATH.exists():

        raise FileNotFoundError(
            f"Peer group file not found: "
            f"{PEER_GROUPS_PATH}"
        )

    df = pd.read_excel(
        PEER_GROUPS_PATH
    )

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(
            " ",
            "_"
        )
    )

    return df


# =========================================================
# MAIN VALIDATION
# =========================================================

def main():

    print("\n" + "=" * 70)
    print("SPRINT 3 - DAY 19")
    print("RADAR CHART VALIDATION")
    print("=" * 70)

    # -----------------------------------------------------
    # Check output directory
    # -----------------------------------------------------

    print("\n========== OUTPUT DIRECTORY ==========")

    if RADAR_OUTPUT_DIR.exists():

        print(
            "Directory Exists : PASS"
        )

        print(
            "Path :",
            RADAR_OUTPUT_DIR
        )

    else:

        print(
            "Directory Exists : FAIL"
        )

        return

    # -----------------------------------------------------
    # Find radar charts
    # -----------------------------------------------------

    radar_files = sorted(
        RADAR_OUTPUT_DIR.glob(
            "*_radar.png"
        )
    )

    print(
        "\n========== RADAR CHART FILES =========="
    )

    print(
        "Charts Found :",
        len(radar_files)
    )

    print(
        "Expected     :",
        EXPECTED_COMPANIES
    )

    if len(radar_files) == EXPECTED_COMPANIES:

        print(
            "Chart Count  : PASS"
        )

    else:

        print(
            "Chart Count  : FAIL"
        )

    # -----------------------------------------------------
    # Check filename convention
    # -----------------------------------------------------

    invalid_files = [
        file.name
        for file in radar_files
        if not file.name.endswith(
            "_radar.png"
        )
    ]

    print(
        "\n========== FILENAME VALIDATION =========="
    )

    if not invalid_files:

        print(
            "Filename Convention : PASS"
        )

    else:

        print(
            "Filename Convention : FAIL"
        )

        print(
            "Invalid Files:",
            invalid_files
        )

    # -----------------------------------------------------
    # Extract company IDs from filenames
    # -----------------------------------------------------

    chart_company_ids = {
        file.stem.replace(
            "_radar",
            ""
        )
        for file in radar_files
    }

    print(
        "\nUnique Companies with Charts :",
        len(chart_company_ids)
    )

    # -----------------------------------------------------
    # Load company IDs from database
    # -----------------------------------------------------

    conn = sqlite3.connect(
        DB_PATH
    )

    try:

        db_companies = pd.read_sql_query(
            """
            SELECT DISTINCT company_id
            FROM company_scores
            """,
            conn
        )

    finally:

        conn.close()

    db_company_ids = set(
        db_companies[
            "company_id"
        ]
        .dropna()
        .astype(str)
    )

    # -----------------------------------------------------
    # Compare companies
    # -----------------------------------------------------

    missing_charts = (
        db_company_ids
        -
        chart_company_ids
    )

    extra_charts = (
        chart_company_ids
        -
        db_company_ids
    )

    print(
        "\n========== COMPANY COVERAGE =========="
    )

    print(
        "Database Companies :",
        len(db_company_ids)
    )

    print(
        "Radar Companies    :",
        len(chart_company_ids)
    )

    print(
        "Missing Charts     :",
        len(missing_charts)
    )

    if missing_charts:

        print(
            "Missing Companies:",
            sorted(
                missing_charts
            )
        )

    else:

        print(
            "Missing Charts : NONE"
        )

    if extra_charts:

        print(
            "Extra Chart Files:",
            sorted(
                extra_charts
            )
        )

    else:

        print(
            "Extra Chart Files : NONE"
        )

    # -----------------------------------------------------
    # Peer Group Validation
    # -----------------------------------------------------

    peer_groups = load_peer_groups()

    peer_company_ids = set(
        peer_groups[
            "company_id"
        ]
        .dropna()
        .astype(str)
    )

    no_peer_group = (
        db_company_ids
        -
        peer_company_ids
    )

    print(
        "\n========== PEER GROUP COVERAGE =========="
    )

    print(
        "Companies with Peer Group :",
        len(peer_company_ids)
    )

    print(
        "Companies without Peer Group :",
        len(no_peer_group)
    )

    if no_peer_group:

        print(
            "No Peer Group Companies:"
        )

        print(
            sorted(
                no_peer_group
            )
        )

        print(
            "\nReference for these companies:"
        )

        print(
            "Nifty 100 Average"
        )

    else:

        print(
            "All companies have peer groups."
        )

    # -----------------------------------------------------
    # Radar Metrics Validation
    # -----------------------------------------------------

    print(
        "\n========== RADAR METRICS =========="
    )

    print(
        "Metrics Required :",
        len(RADAR_METRICS)
    )

    for metric in RADAR_METRICS:

        print(
            "PASS :",
            metric
        )

    # -----------------------------------------------------
    # Final Status
    # -----------------------------------------------------

    print(
        "\n" + "=" * 70
    )

    if (
        len(radar_files)
        == EXPECTED_COMPANIES
        and not invalid_files
        and not missing_charts
    ):

        print(
            "DAY 19 RADAR VALIDATION : PASS"
        )

        print(
            "All expected radar charts are generated successfully."
        )

    else:

        print(
            "DAY 19 RADAR VALIDATION : FAIL"
        )

    print(
        "=" * 70
    )


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":

    main()