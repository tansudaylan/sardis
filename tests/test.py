import sardis


def test_init_smoke(monkeypatch, tmp_path):
    monkeypatch.setenv('SARDIS_DATA_PATH', str(tmp_path / 'repo'))

    result = sardis.init(pathbase=str(tmp_path / 'repo'), strgcnfg='TransitVet')

    assert isinstance(result, dict)
