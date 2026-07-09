from src.etl.pipeline import ETLPipeline


def test_load_audit_exists():
    pipeline = ETLPipeline()

    pipeline.load_all()

    audit = pipeline.get_load_audit()

    assert audit is not None


def test_load_audit_is_list():
    pipeline = ETLPipeline()

    pipeline.load_all()

    audit = pipeline.get_load_audit()

    assert isinstance(audit, list)


def test_load_audit_length():
    pipeline = ETLPipeline()

    pipeline.load_all()

    audit = pipeline.get_load_audit()

    assert len(audit) == 7


def test_load_audit_required_fields():
    pipeline = ETLPipeline()

    pipeline.load_all()

    audit = pipeline.get_load_audit()

    required = {
        "dataset",
        "filename",
        "rows",
        "columns",
        "status",
    }

    for record in audit:
        assert required.issubset(record.keys())


def test_load_audit_success_status():
    pipeline = ETLPipeline()

    pipeline.load_all()

    audit = pipeline.get_load_audit()

    for record in audit:
        assert record["status"] == "SUCCESS"