import importlib.util
from pathlib import Path

import matplotlib.image as mpimg
import numpy as np


EXAMPLE_PATH = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "synthetic_vetting_performance.py"
)
SPECIFICATION = importlib.util.spec_from_file_location(
    "sardis_synthetic_vetting_example", EXAMPLE_PATH
)
example = importlib.util.module_from_spec(SPECIFICATION)
SPECIFICATION.loader.exec_module(example)


def make_result() -> dict:
    return {
        "typesyst": "PlanetarySystem",
        "listnameclastruetype": ["PlanetarySystem", "StellarBinary"],
        "indxclastruetypetarg": np.array([0, 0, 0, 1]),
        "listlablclasdisp": ["Low threshold", "High threshold"],
        "boolpositarg": [
            np.array([True, True, False, False]),
            np.array([True, False, False, False]),
        ],
    }


def test_synthetic_vetting_example_writes_nonblank_png(tmp_path, capsys):
    output_path = tmp_path / "synthetic_vetting_performance.png"

    summary = example.run_example(output_path, result=make_result())

    image = mpimg.imread(output_path)
    assert image.shape[0] > 100
    assert image.shape[1] > 100
    assert image[..., :3].min() < 0.8
    np.testing.assert_allclose(summary["precision"], np.array([1.0, 1.0]))
    np.testing.assert_allclose(summary["recall"], np.array([2.0 / 3.0, 1.0 / 3.0]))
    assert f"Writing to {output_path}..." in capsys.readouterr().out