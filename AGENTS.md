# AGENTS.md — Rubik's Cube Monte Carlo Project Guide

Everything an AI agent needs to understand this codebase, make correct changes, and avoid known pitfalls.

---

## Project Goal

Implement and experiment with a Rubik's Cube solver using Monte Carlo methods and CFOP (Fridrich) strategy. The project contains multiple cube representations at different stages of completeness, a 3D visualizer, and a growing test suite.

---

## Repository Structure

```
cube.py               — Grid-based cube (original). Used by cross_solver.py.
cube2.py              — Piece-based cube (has known bugs, do not extend).
cube3.py              — Geometry-driven cube (canonical, authoritative). USE THIS.
cross_solver.py       — Partial CFOP cross solver (uses cube.py).
CFOP_solver.py        — CFOP skeleton, all stages are TODO stubs.
globals_config.py     — Skill-level and color constants.
cube_visualizer.py    — 2D net visualization (pygame).
cube_visualizer_3d.py — 3D projection visualization (pygame). Uses cube3.py.
test_cube3.py         — Primary test suite. Run this.
test_cube2.py         — Tests for cube2.py (mostly passing but cube2 is buggy).
test_cube.py / test_cube_moves.py / test_rotations.py — Tests for cube.py.
test_cross_solver.py  — Tests for cross_solver.py.
planCube3.prompt.md   — Design document for cube3.py (key reference).
CROSS_SOLVER_STATUS.md — Status doc for cross solver.
logs/                 — Auto-created. Cube state logs from the 3D visualizer.
```

---

## Canonical Cube: cube3.py

**Always use `cube3.py`** for new solver work and tests. It is the only representation that is geometry-correct.

### Why Not cube2.py?

`cube2.py` has confirmed bugs that make it unreliable:
- **R move permutation bug**: `corners[3]` is incorrectly assigned its own piece instead of `corners[7]`, creating a 3-cycle instead of the correct 4-cycle.
- **Edge cycle bug**: Uses index 3 (UB) instead of 4 (DR) for the R move edge cycle.
- **CW/CCW labelling inconsistency**: U "clockwise" implements CCW from above.
- These bugs cause `test_RU_order_63` and several other tests to fail — the failures are expected and known.

### Coordinate System

```
+x = R   -x = L
+y = U   -y = D
+z = B   -z = F   (NOTE: +z is Back, not Front)
```

### Color Scheme

| Face | Color | Char |
|------|-------|------|
| U (top)   | White  | W |
| D (bottom)| Yellow | Y |
| F (front) | Green  | G |
| B (back)  | Blue   | B |
| R (right) | Red    | R |
| L (left)  | Orange | O |

### State Representation

```python
cube.corners  # list of 8 lists, each [color0, color1, color2]
cube.edges    # list of 12 lists, each [color0, color1]
```

Stickers are stored in face-slot order. `CORNER_SLOT_FACES[i]` gives the `(face0, face1, face2)` faces for slot `i`. `stickers[j]` is the color visible on `face_j`.

**Solved state example — corner 0 (URF):**
```python
CORNER_SLOT_FACES[0] == ('U', 'R', 'F')
cube.corners[0]      == ['W', 'R', 'G']   # W on U, R on R, G on F
```

### Piece Indices

```
Corners: 0=URF  1=UFL  2=ULB  3=UBR
         4=DFR  5=DLF  6=DBL  7=DRB

Edges:   0=UR   1=UF   2=UL   3=UB
         4=DR   5=DF   6=DL   7=DB
         8=FR   9=FL  10=BL  11=BR
```

### Move Geometry (Face Cycles)

Derived from rotation matrices; these are the authoritative values used by `_remap_stickers`:

| Move | Face Cycle            |
|------|-----------------------|
| U    | F→R, R→B, B→L, L→F   |
| D    | F→L, L→B, B→R, R→F   |
| R    | U→B, B→D, D→F, F→U   |
| L    | U→F, F→D, D→B, B→U   |
| F    | U→R, R→D, D→L, L→U   |
| B    | U→L, L→D, D→R, R→U   |

### Position Cycles (where pieces travel)

| Move | Corner Cycle   | Edge Cycle          |
|------|---------------|---------------------|
| U    | 0→3→2→1       | 0→3→2→1             |
| D    | 4→7→6→5       | 4→7→6→5             |
| R    | 0→3→7→4       | 0→11→4→8            |
| L    | 1→5→6→2       | 2→9→6→10            |
| F    | 0→4→5→1       | 1→8→5→9             |
| B    | 3→2→6→7       | 3→10→7→11           |

### Cube API

```python
cube = Cube()                       # solved state
cube.apply_move("R")                # single move: "U", "R'", "F2", etc.
cube.apply_moves(["R", "U", "R'"])  # move list
cube.scramble(20)                   # applies 20 random moves, returns move list
cube.reset()                        # back to solved
cube.copy()                         # deep copy (needed by CFOP solver)
cube.is_solved()                    # bool
cube.get_sticker(face, row, col)    # color at face position (for visualizer)
cube.get_corner_orientation(idx)    # 0/1/2 — where W/Y sticker sits in slot
cube.get_edge_orientation(idx)      # 0=oriented, 1=flipped
cube.serialize()                    # compact string, e.g. "WRG/WGO/...|WR/WG/..."
Cube.deserialize(s)                 # create Cube from serialized string
cube.log_state()                    # append state to logs/cube_states.log
```

### Orientation Invariants (always true on a valid cube)

```
sum(corner orientations) ≡ 0  (mod 3)
sum(edge orientations)   ≡ 0  (mod 2)
```

These are checked in `TestOrientationInvariants`. Any move implementation that violates them is wrong.

---

## Serialization Format

Used for logging and creating ground-truth test fixtures.

**Format:** `WRG/WGO/WOB/WBR/YGR/YOG/YBO/YRB|WR/WG/WO/WB/YR/YG/YO/YB/GR/GO/BO/BR`

- `|` separates corners from edges
- `/` separates individual pieces
- Each piece is sticker colors concatenated (3 chars for corners, 2 for edges)
- One state per line in log files

**Solved cube string:**
```
WRG/WGO/WOB/WBR/YGR/YOG/YBO/YRB|WR/WG/WO/WB/YR/YG/YO/YB/GR/GO/BO/BR
```

**To create a test fixture from a logged state:**
```python
cube = Cube.deserialize("WRG/WGO/WOB/WBR/YGR/YOG/YBO/YRB|WR/WG/WO/WB/YR/YG/YO/YB/GR/GO/BO/BR")
```

The 3D visualizer logs a state to `logs/cube_states.log` after every keyboard move, every scramble step, and every reset. Copy any line to deserialize it.

---

## 3D Visualizer (cube_visualizer_3d.py)

Uses pygame with software projection (no OpenGL). Controls:

| Key | Action |
|-----|--------|
| U/D/R/L/F/B | Apply face move |
| + Shift | Inverse move |
| SPACE | Scramble (20 moves, animated) |
| 0 | Reset to solved |
| Q / ESC | Quit |
| Mouse drag | Rotate view |

**Important:** Keyboard face mapping is z-axis corrected. `K_f` sends `B`/`B'` to the cube (not `F`), because the visualizer's +z=F conflicts with cube3's +z=B.

**Known bug in `animate_scramble`:** `scramble()` already applies moves internally; the loop that re-applies each returned move causes all scramble moves to be applied twice. This is pre-existing and not serialization-related.

**Run it:**
```
.venv/Scripts/python.exe cube_visualizer_3d.py
```

---

## Testing

**Primary test file:** `test_cube3.py`

```bash
# Run all cube3 tests
pytest test_cube3.py -v

# Run only serialization tests
pytest test_cube3.py::TestSerialization -v
```

### Known Pre-Existing Failures in test_cube3.py

These 6 tests fail due to bugs in cube2.py that surfaced when some tests were ported. They are **not regressions** — they document known issues:

| Test | Root Cause |
|------|-----------|
| `TestMoveSequences::test_T_perm_twice_is_identity` | cube3 move geometry issue |
| `TestPieceIdentity::test_corner_colors_preserved` | scramble double-apply bug |
| `TestPieceIdentity::test_edge_colors_preserved` | scramble double-apply bug |
| `TestScramble::test_scramble_preserves_pieces` | scramble double-apply bug |
| `TestKnownAlgorithms::test_superflip_is_not_solved` | geometry verification needed |
| `TestKnownAlgorithms::test_RU_order_63` | related to above |

All 9 `TestSerialization` tests pass. All other test classes pass (100 tests).

### Test Patterns

```python
# Fixture
@pytest.fixture
def solved_cube():
    return Cube()

# State comparison
assert cube.corners == SOLVED_CORNERS
assert cube.is_solved()

# Deserialize a known state for a ground-truth fixture
cube = Cube.deserialize("WRG/WGO/WOB/WBR/YGR/YOG/YBO/YRB|WR/WG/WO/WB/YR/YG/YO/YB/GR/GO/BO/BR")
```

---

## Solvers

### cross_solver.py (uses cube.py — grid-based)

- `is_cross_complete(cube)` — ✅ fully working
- `recognize_cross_edges(cube)` — ✅ fully working
- `solve_cross_beginner()` — ⚠️ incomplete, handles D-layer well, fails on U/side-face edges

### CFOP_solver.py

All four stages (cross, F2L, OLL, PLL) are TODO stubs. The solver expects:
- `cube.copy()` — exists on cube3.py ✅, missing on cube.py ❌
- `cube.apply_move()` / `cube.apply_moves()` — exists on both

If implementing CFOP stages, use cube3.py as the cube type.

---

## Configuration (globals_config.py)

```python
CROSS_COLOR = 'W'           # white cross
CROSS_SKILL = 'beginner'    # 'beginner' | 'intermediate' | 'advanced'
F2L_SKILL = 0               # 0=beginner … 3=advanced
OLL_SKILL = 2               # 1=2-look, 2=1-look
PLL_SKILL = 2               # 1=2-look, 2=1-look
SCRAMBLE_LENGTH = 20
```

---

## Development Environment

```bash
# Activate venv
.venv/Scripts/activate       # PowerShell
source .venv/bin/activate    # bash

# Run tests
pytest test_cube3.py -v

# Run visualizer
python cube_visualizer_3d.py

# Install deps
pip install -r requirements.txt
```

Python 3.12. Dependencies: `pygame`, `numpy`, `matplotlib` (see requirements.txt).

---

## Agent Guidelines

- **Always use cube3.py**, never cube2.py, for new code.
- **Don't fix the 6 known test failures** unless that is the explicit task — they document deliberate known issues.
- **The z-axis is +z=B, not +z=F** — this is intentional and affects face naming.
- **`scramble()` applies moves internally** and also returns them — don't re-apply the returned list.
- **Logs are gitignored** — `logs/` is local only.
- **`Cube.deserialize(s)`** is the intended way to create test fixtures from observed states; no file I/O required.
- When adding new moves or changing move geometry, verify orientation invariants with `TestOrientationInvariants`.
- When changing `cube3.py` serialization format, update `TestSerialization::SOLVED_STRING` and the format docs in this file.
