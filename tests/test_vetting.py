import numpy as np
import pytest

from sardis.vetting import summarize_vetting_result


def test_summarize_vetting_result_computes_classifier_metrics():
    result = {
        "typesyst": "PlanetarySystem",
        "listnameclastruetype": ["PlanetarySystem", "StellarBinary"],
        "indxclastruetypetarg": np.array([0, 0, 1, 1]),
        "listlablclasdisp": ["Selective", "Inclusive"],
        "boolpositarg": [
            np.array([True, False, True, False]),
            np.array([True, True, True, True]),
        ],
    }

    summary = summarize_vetting_result(result)

    np.testing.assert_array_equal(
        summary["confusion_matrices"],
        np.array([[[1, 1], [1, 1]], [[0, 2], [0, 2]]]),
    )
    np.testing.assert_allclose(summary["precision"], np.array([0.5, 0.5]))
    np.testing.assert_allclose(summary["recall"], np.array([0.5, 1.0]))


def test_summarize_vetting_result_rejects_unknown_target_type():
    with pytest.raises(ValueError, match="absent from truth labels"):
        summarize_vetting_result(
            {
                "typesyst": "PlanetarySystem",
                "listnameclastruetype": ["StellarBinary"],
                "indxclastruetypetarg": np.array([0]),
                "listlablclasdisp": [],
                "boolpositarg": [],
            }
        )