"""Candidate-vetting summaries for Sardis workflow outputs."""

import numpy as np


def summarize_vetting_result(result: dict) -> dict[str, object]:
    """Summarize classifier performance against simulated truth labels."""

    true_type_names = list(result["listnameclastruetype"])
    target_type = result["typesyst"]
    if target_type not in true_type_names:
        raise ValueError(f"Target type {target_type!r} is absent from truth labels.")

    true_type_index = np.asarray(result["indxclastruetypetarg"], dtype=int)
    positive_truth = true_type_index == true_type_names.index(target_type)
    classifier_labels = list(result["listlablclasdisp"])
    predictions = [np.asarray(values, dtype=bool) for values in result["boolpositarg"]]
    if len(predictions) != len(classifier_labels):
        raise ValueError("Classifier labels and prediction arrays must have equal length.")
    if any(values.shape != positive_truth.shape for values in predictions):
        raise ValueError("Each prediction array must match the truth-label shape.")

    confusion_matrices = np.empty((len(predictions), 2, 2), dtype=int)
    precision = np.zeros(len(predictions))
    recall = np.zeros(len(predictions))
    for index, predicted_positive in enumerate(predictions):
        true_positive = np.count_nonzero(predicted_positive & positive_truth)
        false_positive = np.count_nonzero(predicted_positive & ~positive_truth)
        false_negative = np.count_nonzero(~predicted_positive & positive_truth)
        true_negative = np.count_nonzero(~predicted_positive & ~positive_truth)
        confusion_matrices[index] = [
            [true_negative, false_positive],
            [false_negative, true_positive],
        ]
        if true_positive + false_positive > 0:
            precision[index] = true_positive / (true_positive + false_positive)
        if true_positive + false_negative > 0:
            recall[index] = true_positive / (true_positive + false_negative)

    return {
        "classifier_labels": classifier_labels,
        "confusion_matrices": confusion_matrices,
        "precision": precision,
        "recall": recall,
        "positive_truth": positive_truth,
    }