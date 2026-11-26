"""Parametric L-bracket with a reinforcing web and four counterbored holes."""

import argparse
from pathlib import Path

from build123d import (
    Align,
    Axis,
    BuildPart,
    BuildSketch,
    Box,
    Cylinder,
    Locations,
    Mode,
    Plane,
    Part,
    Polygon,
    extrude,
    export_step,
    export_stl,
    fillet,
)

from cad_lib.tolerances import (
    FDM_M4_HOLE_DIAMETER_DEFAULT_MM,
    FDM_M4_HOLE_DIAMETER_MAX_MM,
    FDM_M4_HOLE_DIAMETER_MIN_MM,
)


def build_bracket(
    *,
    width: float = 60.0,
    depth: float = 40.0,
    height: float = 50.0,
    thickness: float = 8.0,
    rib_width: float = 10.0,
    rib_run: float = 25.0,
    rib_rise: float = 25.0,
    hole_edge_offset: float = 10.0,
    hole_diameter: float = FDM_M4_HOLE_DIAMETER_DEFAULT_MM,
    counterbore_diameter: float = 8.0,
    counterbore_depth: float = 4.0,
    fillet_radius: float = 0.8,
) -> Part:
    """Build and return a bracket in millimeters.

    The width runs along X, the foot depth along Y, and the upright height
    along Z. The four M4 clearance holes are arranged in a 2-by-2 pattern on
    the foot. The counterbores open on the top face of the foot.
    """
    if not FDM_M4_HOLE_DIAMETER_MIN_MM <= hole_diameter <= FDM_M4_HOLE_DIAMETER_MAX_MM:
        raise ValueError(
            "hole_diameter must be between "
            f"{FDM_M4_HOLE_DIAMETER_MIN_MM} and "
            f"{FDM_M4_HOLE_DIAMETER_MAX_MM} mm for the FDM M4 profile; "
            f"got {hole_diameter} mm."
        )

    x_rib_start = (width - rib_width) / 2.0
    hole_x_positions = (hole_edge_offset, width - hole_edge_offset)
    hole_y_positions = (
        thickness + hole_edge_offset,
        depth - hole_edge_offset,
    )
    min_corner_align = (Align.MIN, Align.MIN, Align.MIN)

    with BuildPart() as bracket:
        Box(width, thickness, height, align=min_corner_align)
        Box(width, depth, thickness, align=min_corner_align)

        fillet(
            bracket.edges().filter_by(Axis.X),
            radius=fillet_radius,
        )

        with BuildSketch(Plane.YZ.offset(x_rib_start)):
            Polygon(
                (thickness, thickness),
                (thickness + rib_run, thickness),
                (thickness, thickness + rib_rise),
                align=None,
            )
        extrude(amount=rib_width)

        for x_position in hole_x_positions:
            for y_position in hole_y_positions:
                with Locations((x_position, y_position, 0.0)):
                    Cylinder(
                        hole_diameter / 2.0,
                        thickness,
                        align=(Align.CENTER, Align.CENTER, Align.MIN),
                        mode=Mode.SUBTRACT,
                    )
                with Locations(
                    (x_position, y_position, thickness - counterbore_depth)
                ):
                    Cylinder(
                        counterbore_diameter / 2.0,
                        counterbore_depth,
                        align=(Align.CENTER, Align.CENTER, Align.MIN),
                        mode=Mode.SUBTRACT,
                    )

    return bracket.part


def export_bracket(
    part: Part,
    name: str = "example_bracket",
    output_dir: Path | str = Path("exports"),
) -> tuple[Path, Path]:
    """Export a bracket as STEP and STL and return both output paths."""
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    step_path = destination / f"{name}.step"
    stl_path = destination / f"{name}.stl"
    export_step(part, str(step_path))
    export_stl(part, str(stl_path))
    return step_path, stl_path


def main() -> None:
    """Build and export the bracket, optionally overriding the M4 hole size."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--hole-diameter",
        type=float,
        default=FDM_M4_HOLE_DIAMETER_DEFAULT_MM,
        help=(
            "M4 clearance-hole diameter in mm "
            f"({FDM_M4_HOLE_DIAMETER_MIN_MM}-{FDM_M4_HOLE_DIAMETER_MAX_MM}; "
            f"default: {FDM_M4_HOLE_DIAMETER_DEFAULT_MM})"
        ),
    )
    arguments = parser.parse_args()

    bracket_part = build_bracket(hole_diameter=arguments.hole_diameter)
    if not bracket_part.is_valid:
        raise ValueError("The generated bracket geometry is invalid.")
    step_path, stl_path = export_bracket(bracket_part)
    print(f"STEP exported to: {step_path}")
    print(f"STL exported to:  {stl_path}")


if __name__ == "__main__":
    main()
