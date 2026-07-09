"""
loader.py

Loads Excel datasets for the N100 Financial Intelligence Platform.
"""

from pathlib import Path
import pandas as pd

from src.etl.normalizer import DataNormalizer


class ExcelLoader:
    """
    Reads Excel files from the raw data directory.
    """

    def __init__(self, data_directory: Path):
        """
        Initialize the loader.

        Parameters
        ----------
        data_directory : Path
            Path to the folder containing Excel files.
        """
        self.data_directory = data_directory

    def load_excel(self, filename: str) -> pd.DataFrame:
        """
        Load a single Excel file.
        """

        file_path = self.data_directory / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        df = pd.read_excel(file_path, skiprows=1)

        # Standardize column names
        df = DataNormalizer.normalize_columns(df)

        # Remove duplicate records
        df = DataNormalizer.remove_duplicates(df)

        return df