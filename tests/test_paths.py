import os

from sardis.main import retr_pathsard


def test_retr_pathsard_creates_expected_directories(monkeypatch, tmp_path):
    monkeypatch.setenv('SARDIS_DATA_PATH', str(tmp_path / 'repo'))

    dictpath = retr_pathsard(strgcnfg='TransitVet')

    assert os.path.isdir(dictpath['pathbase'])
    assert os.path.isdir(dictpath['pathdatapipe'])
    assert os.path.isdir(dictpath['pathvisupipe'])
    assert os.path.isdir(dictpath['pathcnfg'])
    assert os.path.isdir(dictpath['pathsimu'])
    assert os.path.isdir(dictpath['pathobsd'])
    assert os.path.normpath(dictpath['pathcnfg']).endswith(os.path.normpath('TransitVet'))
