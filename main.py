"""
Main entry point for the N100 Financial Intelligence Platform.
"""

from src.etl.pipeline import ETLPipeline


def main():
    pipeline = ETLPipeline()
    pipeline.run_pipeline()


if __name__ == "__main__":
    main()
    