"""Geometry checks for the example bracket."""

import pytest

from cad_lib.tolerances import (
    FDM_M4_HOLE_DIAMETER_DEFAULT_MM,
    FDM_M4_HOLE_DIAMETER_MAX_MM,
    FDM_M4_HOLE_DIAMETER_MIN_MM,
)
from parts.example_bracket import build_bracket


EXPECTED_VOLUME_MM3 = 41403.13105173061
EXPECTED_DIMENSIONS_MM = (60.0, 40.0, 50.0)


def test_bracket_is_valid() -> None:
    """The generated solid must pass the CAD kernel validity check."""
    assert build_bracket().is_valid is True


def test_bracket_volume_matches_expected_value() -> None:
    """The generated volume must remain within one percent of its reference."""
    part = build_bracket()
    assert part.volume == pytest.approx(EXPECTED_VOLUME_MM3, rel=0.01)


def test_bracket_bounding_box_matches_requested_dimensions() -> None:
    """The outer dimensions must match the default design parameters."""
    bounds = build_bracket().bounding_box()
    expected_width, expected_depth, expected_height = EXPECTED_DIMENSIONS_MM
    assert bounds.size.X == pytest.approx(expected_width, rel=0.0, abs=1e-7)
    assert bounds.size.Y == pytest.approx(expected_depth, rel=0.0, abs=1e-7)
    assert bounds.size.Z == pytest.approx(expected_height, rel=0.0, abs=1e-7)


@pytest.mark.parametrize(
    "hole_diameter",
    [FDM_M4_HOLE_DIAMETER_MIN_MM, FDM_M4_HOLE_DIAMETER_MAX_MM],
)
def test_bracket_accepts_hole_diameter_limits(hole_diameter: float) -> None:
    """Both ends of the recommended FDM M4 hole range produce valid geometry."""
    assert build_bracket(hole_diameter=hole_diameter).is_valid is True


@pytest.mark.parametrize(
    "hole_diameter",
    [FDM_M4_HOLE_DIAMETER_MIN_MM - 0.01, FDM_M4_HOLE_DIAMETER_MAX_MM + 0.01],
)
def test_bracket_rejects_hole_diameter_outside_limits(hole_diameter: float) -> None:
    """Hole sizes beyond the recommended FDM range must fail explicitly."""
    with pytest.raises(ValueError, match="hole_diameter must be between"):
        build_bracket(hole_diameter=hole_diameter)


def test_default_hole_diameter_is_inside_allowed_range() -> None:
    """The default design value must remain within the FDM M4 size limits."""
    assert FDM_M4_HOLE_DIAMETER_MIN_MM < FDM_M4_HOLE_DIAMETER_DEFAULT_MM
    assert FDM_M4_HOLE_DIAMETER_DEFAULT_MM < FDM_M4_HOLE_DIAMETER_MAX_MM
