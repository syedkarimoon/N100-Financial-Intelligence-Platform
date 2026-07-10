-- =====================================================
-- N100 Financial Intelligence Platform
-- SQLite Database Schema
-- Sprint 1 - Day 4
-- =====================================================

PRAGMA foreign_keys = ON;
-- =====================================================
-- Companies Table
-- =====================================================
"""
SQLite Database Loader
Creates nifty100.db and loads all DataFrames.
"""

import sqlite3
from pathlib import Path


class SQLiteLoader:
    """
    Loads DataFrames into SQLite.
    """

    def __init__(self, db_path="db/nifty100.db"):
        self.db_path = Path(db_path)

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def load_dataframe(self, df, table_name):
        conn = self.connect()

        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        conn.commit()
        conn.close()

        print(f"Loaded {table_name}")