"""
SQLite Database Loader

Creates the SQLite database and loads
all DataFrames into individual tables.
"""

import sqlite3
from pathlib import Path


class SQLiteLoader:
    """
    Loads pandas DataFrames into SQLite.
    """

    def __init__(self, db_path="db/nifty100.db"):
        """
        Initialize database path.
        """
        self.db_path = Path(db_path)

    def connect(self):
        """
        Create SQLite connection.
        """

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        conn = sqlite3.connect(self.db_path)

        conn.execute(
            "PRAGMA foreign_keys = ON;"
        )

        return conn

    def load_dataframe(
        self,
        dataframe,
        table_name
    ):
        """
        Load one DataFrame into SQLite.
        """

        conn = self.connect()

        dataframe.to_sql(
            name=table_name,
            con=conn,
            if_exists="replace",
            index=False
        )

        conn.commit()

        conn.close()

        print(
            f"✓ Loaded '{table_name}' into SQLite"
        )

    def load_all(
        self,
        datasets
    ):
        """
        Load all DataFrames.
        """

        for table_name, dataframe in datasets.items():

            self.load_dataframe(
                dataframe,
                table_name
            )

        print(
            "\n✓ All tables loaded successfully."
        )