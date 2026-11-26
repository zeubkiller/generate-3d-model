# CAD-as-Code instructions

When creating or modifying a part in this repository:

- Always use `build123d` and its context API (`BuildPart`, `BuildSketch`, and
  `BuildLine` where appropriate). Do not use another CAD kernel or construct
  geometry through opaque, unparameterized scripts.
- Do not use magic numbers for dimensions or tolerances. Expose dimensions and
  tolerances as typed `float` parameters at the top of a function or in a
  `dataclass`. Give parameters meaningful names and units.
- Import manufacturing clearances and tolerance defaults from
  `cad_lib.tolerances`; do not redefine them in part modules.
- Check `part.is_valid` before treating generated geometry as complete. Use the
  `build123d-mcp` server tools to measure hole spacing, check interferences, and
  validate geometry before concluding that a design is ready.
- Provide a reusable export function for every part. Export STEP and STL files
  to `exports/<part_name>.step` and `exports/<part_name>.stl`, creating the
  output directory when needed.
- Keep each part parametric, document its public parameters, and add focused
  `pytest` tests for validity, expected geometry, and relevant dimensions.
