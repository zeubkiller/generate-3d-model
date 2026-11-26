"""Manufacturing clearances and tolerances, expressed in millimeters."""

from dataclasses import dataclass

FDM_CLEARANCE_MM = 0.2
CNC_CLEARANCE_MM = 0.05
FDM_M4_HOLE_DIAMETER_MIN_MM: float = 4.2
FDM_M4_HOLE_DIAMETER_DEFAULT_MM: float = 4.4
FDM_M4_HOLE_DIAMETER_MAX_MM: float = 4.8


@dataclass(frozen=True)
class ManufacturingTolerances:
    """Default clearances for common manufacturing processes."""

    fdm_clearance_mm: float = FDM_CLEARANCE_MM
    cnc_clearance_mm: float = CNC_CLEARANCE_MM


DEFAULT_TOLERANCES = ManufacturingTolerances()
