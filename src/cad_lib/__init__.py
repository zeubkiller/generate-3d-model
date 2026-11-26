"""Shared configuration for the cad-lib parametric CAD project."""

from .tolerances import (
    CNC_CLEARANCE_MM,
    DEFAULT_TOLERANCES,
    FDM_CLEARANCE_MM,
    FDM_M4_HOLE_DIAMETER_DEFAULT_MM,
    FDM_M4_HOLE_DIAMETER_MAX_MM,
    FDM_M4_HOLE_DIAMETER_MIN_MM,
    ManufacturingTolerances,
)

__all__ = [
    "CNC_CLEARANCE_MM",
    "DEFAULT_TOLERANCES",
    "FDM_CLEARANCE_MM",
    "FDM_M4_HOLE_DIAMETER_DEFAULT_MM",
    "FDM_M4_HOLE_DIAMETER_MAX_MM",
    "FDM_M4_HOLE_DIAMETER_MIN_MM",
    "ManufacturingTolerances",
]
