# sardis

## Scientific purpose
Sardis is a workflow for exoplanet candidate vetting and occurrence-style evaluation based on time-domain photometric data and related model diagnostics. It acts as a pipeline layer around shared time-domain and modeling functionality rather than as a monolithic analysis script.

## Repository role in the ecosystem
Sardis is a workflow-focused package that uses the shared time-domain infrastructure in the broader ecosystem, especially the path conventions and plotting utilities provided by the active scientific stack. It is designed to keep project-specific candidate-vetting logic separate from the lower-level numerical and plotting library layers.

## Installation

```bash
cd /path/to/sardis
pip install -e .
```

## Minimal usage

```python
import sardis

result = sardis.init(pathbase='.', strgcnfg='TransitVet')
print(type(result))
```

The exact configuration depends on the target system and dataset, but the package is intended to be initialized through the `init()` workflow rather than by ad hoc script execution.

## Outputs and diagnostics
The package writes its processed data products and visualization outputs under a normalized project path tree rooted in the configured data directory. This keeps the candidate-vetting workflow inspectable and reproducible without hard-coded machine-specific paths.

## Current maintenance status
The repository is active as a workflow package but remains narrower in scope than the shared numerical and plotting libraries. The supported entry points are the package import surface and the `init()` workflow; legacy exploratory scripts should not be treated as the active API.

