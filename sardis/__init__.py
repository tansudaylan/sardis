"""Sardis package.

This package provides the supported exoplanet-candidate vetting workflow and the
normalized path helpers used to route its data and diagnostics. The public API is
kept intentionally small to preserve a clear workflow boundary.
"""

from .main import init, retr_pathsard

__all__ = ["init", "retr_pathsard"]
