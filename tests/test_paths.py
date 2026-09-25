import os

import pytest

from sardis.main import retr_pathsard
from sardis.paths import get_data_path, get_repository_path, get_visuals_path


def test_repository_runtime_paths(monkeypatch, tmp_path):
    monkeypatch.setenv("SARDIS_PATH", str(tmp_path))
    assert get_repository_path() == tmp_path
    assert get_data_path() == tmp_path / "data"
    assert get_visuals_path() == tmp_path / "visuals"


def test_repository_path_is_required(monkeypatch):
    monkeypatch.delenv("SARDIS_PATH", raising=False)
    with pytest.raises(EnvironmentError, match="SARDIS_PATH"):
        get_repository_path()


def test_retr_pathsard_creates_expected_directories(monkeypatch, tmp_path):
    monkeypatch.setenv('SARDIS_PATH', str(tmp_path / 'repo'))

    dictpath = retr_pathsard(strgcnfg='TransitVet')

    assert os.path.isdir(dictpath['pathbase'])
    assert os.path.isdir(dictpath['pathdatapipe'])
    assert os.path.isdir(dictpath['pathvisupipe'])
    assert os.path.isdir(dictpath['pathcnfg'])
    assert os.path.isdir(dictpath['pathsimu'])
    assert os.path.isdir(dictpath['pathobsd'])
    assert os.path.normpath(dictpath['pathcnfg']).endswith(os.path.normpath('TransitVet'))
