# cad-lib

Parametric CAD parts built with `build123d`.

Create a local environment and install the project in editable mode:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .
```

## Generate a part

From the repository root, run:

```bash
.venv/bin/python parts/example_bracket.py
```

This builds the parametric bracket, checks that the solid is valid, then writes:

- `exports/example_bracket.step` for opening in FreeCAD or another CAD tool.
- `exports/example_bracket.stl` for importing into a slicer for 3D printing.

The script prints both output paths. Open the STEP file in FreeCAD with
`File > Open`, or open the STL file in your slicer. You can also use FreeCAD's
**File > Import** to bring an STL mesh into an existing document.

The M4 screw-hole diameter can be set within the recommended FDM range of
4.2–4.8 mm (default: 4.4 mm). For example:

```bash
.venv/bin/python parts/example_bracket.py --hole-diameter 4.6
```

Values outside this range are rejected with an error. When calling the builder
from another Python script, pass the same parameter to
`build_bracket(hole_diameter=4.6)`.

STEP preserves precise solid geometry for CAD exchange, but it does not carry
the original Python parameters or build history. Edit the source parameters in
`build_bracket()` and rerun the script to regenerate the part; use the Python
source as the editable parametric model. The STL is a tessellated mesh intended
for slicing, not precise parametric CAD editing.

Run the geometry tests with `.venv/bin/python -m pytest`.
