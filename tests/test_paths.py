from config.paths import PROJECT_ROOT, RAW_DATA_DIR


def test_paths():
    assert PROJECT_ROOT.exists()
    assert RAW_DATA_DIR.exists()