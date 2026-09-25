#!/usr/bin/env python3
"""Evaluate Sardis candidate vetting on its seeded synthetic population."""

import argparse
import contextlib
import io
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("agg")

import matplotlib.pyplot as plt
import numpy as np

import sardis


def run_synthetic_pipeline(pathbase: Path) -> dict:
    """Run Sardis on Troia's deterministic synthetic target population."""

    configuration = {
        "pathbase": str(pathbase),
        "typesyst": "PlanetarySystem",
        "listlablinst": [["TESS"], []],
        "liststrgtypedata": [["simutargsynt"], []],
        "boolplot": False,
        "typeverb": 0,
    }
    legacy_output = io.StringIO()
    with contextlib.redirect_stdout(legacy_output), contextlib.redirect_stderr(
        legacy_output
    ):
        return sardis.init(
            dicttroiinpt=configuration,
            strgcnfg="SyntheticVetting",
        )


def run_example(
    output_path: Path,
    result: dict | None = None,
) -> dict[str, object]:
    """Plot truth composition and vetting performance from a Sardis run."""

    if result is None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_synthetic_pipeline(Path(directory))
    summary = sardis.summarize_vetting_result(result)

    truth_type_index = np.asarray(result["indxclastruetypetarg"], dtype=int)
    truth_counts = np.bincount(
        truth_type_index,
        minlength=len(result["listnameclastruetype"]),
    )
    classifier_labels = [
        label.replace(" ", "\n", 1) for label in summary["classifier_labels"]
    ]

    figure, axes = plt.subplots(
        1,
        3,
        figsize=(12.5, 4.2),
        facecolor="white",
        constrained_layout=True,
    )
    truth_positions = np.arange(len(truth_counts))
    axes[0].bar(truth_positions, truth_counts, color=["#2E7D32", "#6A6A6A"])
    axes[0].set_xticks(
        truth_positions,
        [name.replace("System", "\nSystem") for name in result["listnameclastruetype"]],
    )
    axes[0].set_ylabel("Simulated targets")
    axes[0].set_title("Input population")

    confusion_matrix = summary["confusion_matrices"][0]
    image = axes[1].imshow(confusion_matrix, cmap="Blues", vmin=0)
    figure.colorbar(image, ax=axes[1], label="Targets")
    axes[1].set_xticks([0, 1], ["Rejected", "Selected"])
    axes[1].set_yticks([0, 1], ["Nonplanet", "Planet"])
    axes[1].set_xlabel("Vetting decision")
    axes[1].set_ylabel("Simulated truth")
    axes[1].set_title("Low-threshold confusion matrix")
    for row_index in range(2):
        for column_index in range(2):
            axes[1].text(
                column_index,
                row_index,
                str(confusion_matrix[row_index, column_index]),
                ha="center",
                va="center",
                color="black",
                fontweight="bold",
            )

    classifier_positions = np.arange(len(classifier_labels))
    bar_width = 0.36
    axes[2].bar(
        classifier_positions - bar_width / 2.0,
        summary["precision"],
        width=bar_width,
        color="#1B6CA8",
        label="Precision",
    )
    axes[2].bar(
        classifier_positions + bar_width / 2.0,
        summary["recall"],
        width=bar_width,
        color="#D18B00",
        label="Recall",
    )
    axes[2].set_xticks(classifier_positions, classifier_labels)
    axes[2].set_ylim(0.0, 1.05)
    axes[2].set_ylabel("Classification metric")
    axes[2].set_title("Threshold tradeoff")
    legend = axes[2].legend(frameon=True, fancybox=True, framealpha=1.0)
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_edgecolor("black")

    for axis in axes:
        axis.grid(False)
    figure.suptitle(
        "Seeded simulation of TESS planetary-system vetting",
        fontweight="bold",
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Writing to {output_path}...")
    figure.savefig(
        output_path,
        dpi=300 if output_path.suffix == ".png" else None,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(figure)
    return summary


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot Sardis performance on its seeded synthetic population."
    )
    parser.add_argument(
        "--typefileplot",
        choices=("png", "pdf"),
        default="png",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    output_path = Path(__file__).with_name(
        f"synthetic_vetting_performance.{arguments.typefileplot}"
    )
    run_example(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())