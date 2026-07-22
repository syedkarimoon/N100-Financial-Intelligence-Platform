import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

print("\n" + "=" * 70)
print("PEER PERCENTILES DATABASE VALIDATION")
print("=" * 70)

# ---------------------------------------------------------
# Table Schema
# ---------------------------------------------------------

print("\n========== TABLE SCHEMA ==========")

schema = conn.execute(
    "PRAGMA table_info(peer_percentiles)"
).fetchall()

for row in schema:
    print(row)

# ---------------------------------------------------------
# Total Rows
# ---------------------------------------------------------

count = conn.execute(
    "SELECT COUNT(*) FROM peer_percentiles"
).fetchone()[0]

print(
    "\nTotal Rows:",
    count
)

# ---------------------------------------------------------
# Unique Companies
# ---------------------------------------------------------

companies = conn.execute(
    "SELECT COUNT(DISTINCT company_id) "
    "FROM peer_percentiles"
).fetchone()[0]

print(
    "Unique Companies:",
    companies
)

# ---------------------------------------------------------
# Unique Peer Groups
# ---------------------------------------------------------

peer_groups = conn.execute(
    "SELECT COUNT(DISTINCT peer_group_name) "
    "FROM peer_percentiles"
).fetchone()[0]

print(
    "Unique Peer Groups:",
    peer_groups
)

# ---------------------------------------------------------
# Unique Metrics
# ---------------------------------------------------------

metrics = conn.execute(
    "SELECT COUNT(DISTINCT metric) "
    "FROM peer_percentiles"
).fetchone()[0]

print(
    "Unique Metrics:",
    metrics
)

# ---------------------------------------------------------
# Metric Distribution
# ---------------------------------------------------------

print(
    "\n========== METRIC DISTRIBUTION =========="
)

metric_df = pd.read_sql_query(
    """
    SELECT
        metric,
        COUNT(*) AS records
    FROM peer_percentiles
    GROUP BY metric
    ORDER BY metric
    """,
    conn
)

print(
    metric_df.to_string(
        index=False
    )
)

# ---------------------------------------------------------
# Percentile Range
# ---------------------------------------------------------

print(
    "\n========== PERCENTILE RANGE =========="
)

min_rank, max_rank = conn.execute(
    """
    SELECT
        MIN(percentile_rank),
        MAX(percentile_rank)
    FROM peer_percentiles
    """
).fetchone()

print(
    "Minimum Percentile:",
    min_rank
)

print(
    "Maximum Percentile:",
    max_rank
)

# ---------------------------------------------------------
# Invalid Percentiles
# ---------------------------------------------------------

invalid = conn.execute(
    """
    SELECT COUNT(*)
    FROM peer_percentiles
    WHERE percentile_rank < 0
       OR percentile_rank > 1
    """
).fetchone()[0]

print(
    "Invalid Percentiles:",
    invalid
)

# ---------------------------------------------------------
# D/E Validation
# ---------------------------------------------------------

print(
    "\n========== D/E SAMPLE =========="
)

de_df = pd.read_sql_query(
    """
    SELECT
        company_id,
        peer_group_name,
        value,
        percentile_rank,
        year
    FROM peer_percentiles
    WHERE metric = 'D/E'
    ORDER BY percentile_rank DESC
    LIMIT 10
    """,
    conn
)

print(
    de_df.to_string(
        index=False
    )
)

conn.close()

print(
    "\nPeer percentile validation completed."
)
