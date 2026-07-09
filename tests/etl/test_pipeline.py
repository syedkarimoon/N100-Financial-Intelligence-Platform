from src.etl.pipeline import ETLPipeline


def test_pipeline():
    pipeline = ETLPipeline()

    datasets = pipeline.load_all()

    assert len(datasets) == 7

    for name, df in datasets.items():
        print(f"\n{name}")
        print(f"Rows    : {df.shape[0]}")
        print(f"Columns : {df.shape[1]}")

        assert df.shape[0] > 0
        assert df.shape[1] > 0
