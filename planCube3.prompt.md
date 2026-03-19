## Plan: Geometry-Driven cube3.py

**TL;DR**: Create `cube3.py` with a sticker-based piece representation where moves are defined by face-cycle geometry. Orientation is derived automatically from sticker positions — no hardcoded orientation deltas. This eliminates the error-prone manual approach in cube2.py.

---

### Core Insight

Instead of tracking `(piece_colors, orientation_number)` and manually specifying +1/+2 orientation deltas per move per piece (as cube2.py does), **store the actual sticker colors in face order** for each slot. When a move cycles a piece between slots, remap stickers using the geometric face cycle. One generic method handles all 6 faces. Orientation is computed on demand from where the U/D color sits.

**Example**: Corner slot 0 = URF has faces (U, R, F). Stickers `['W', 'R', 'G']` means White on U face, Red on R face, Green on F face. After R CW, this piece moves to UBR (slot 3, faces U, B, R). The R face cycle says U→B, F→U, R stays. So the stickers remap to `['G', 'W', 'R']` — Green on U, White on B, Red on R. No magic numbers needed.

---

### Why Not Fix cube2.py?

During research I found several issues in cube2.py that stem from the fundamental design:
1. **R move has a permutation bug** — `corners[3]` receives its own piece back (temp[1] = old corners[3]) instead of old corners[7], creating a 3-cycle instead of a 4-cycle. The edge cycle also uses index 3 (UB) instead of 4 (DR).
2. **CW/CCW labels are inconsistent** — U "clockwise" implements 0→1→2→3 which is actually CCW from above.
3. **Temp-index indirection is fragile** — extracting `[0,3,4,7]` into temp then assigning `temp[0], temp[2], temp[1], temp[3]` to positions `[4,7,3,0]` makes errors invisible.
4. **Orientation deltas are magic numbers** — no derivation, hard to verify, easy to get wrong.

A clean rewrite with a geometry-driven engine is more reliable than patching these issues.

---

### Steps

**Phase 1 — Core Data & Move Engine** (cube3.py)

1. Define `CORNER_SLOT_FACES` (8 triples) and `EDGE_SLOT_FACES` (12 pairs) — each slot's face ordering, documented
2. Define `FACE_CYCLES` — 6 entries, one per face, derived from rotation matrices (see table below)
3. Define `MOVE_CYCLES` — corner and edge position cycles per move (see table below)
4. Implement `_cycle_stickers(pieces, slot_faces, cycle, face_cycle)` — **the single generic move method** that remaps stickers through the face cycle for any move
5. Implement `apply_move(move_str)` — parses "U", "R'", "F2" and calls `_cycle_stickers` for both corners and edges

**Phase 2 — Cube Class API**

6. `__init__` / `reset()` — initialize corners/edges to solved sticker values
7. `is_solved()` — compare against solved constant
8. `copy()` — deep copy (needed by CFOP_solver.py)
9. `apply_moves(move_list)`, `scramble(num_moves)`
10. `get_corner_orientation(idx)` and `get_edge_orientation(idx)` — derived from sticker position, for solver compatibility
11. `get_sticker(face, row, col)` — returns color at a specific face position, for visualizer compatibility

**Phase 3 — Tests** (test_cube3.py)

12. Port all test categories from test_cube2.py: initialization, single moves, sequences, orientation invariants, piece identity, scramble, round-trips
13. Add **sticker-level correctness tests**: verify specific sticker positions after each single move (e.g., after R CW, verify URF piece is at UBR with correct face mapping)
14. Add **known algorithm tests**: (R U R' U')^6 = identity, T-perm preserves parity, superflip, etc.

---

### Verified Geometry

Coordinate system: +x=R, -x=L, +y=U, -y=D, +z=B, -z=F

**Face Cycles** (CW when viewed from outside the face):

| Move | Cycle | Derivation |
|------|-------|-----------|
| U | F→R, R→B, B→L, L→F | -90deg about +y |
| D | F→L, L→B, B→R, R→F | +90deg about +y (opposite to U) |
| R | U→B, B→D, D→F, F→U | +90deg about +x |
| L | U→F, F→D, D→B, B→U | inverse of R |
| F | U→R, R→D, D→L, L→U | CW from -z |
| B | U→L, L→D, D→R, R→U | inverse of F |

**Corner Slot Faces** (index → name → face triple, ordered so index 0 = the U/D face):

| Slot | Name | Face 0 | Face 1 | Face 2 |
|------|------|--------|--------|--------|
| 0 | URF | U | R | F |
| 1 | UFL | U | F | L |
| 2 | ULB | U | L | B |
| 3 | UBR | U | B | R |
| 4 | DFR | D | F | R |
| 5 | DLF | D | L | F |
| 6 | DBL | D | B | L |
| 7 | DRB | D | R | B |

**Edge Slot Faces** (index → name → face pair, ordered so index 0 = the U/D face when in U/D layer, else F/B face):

| Slot | Name | Face 0 | Face 1 |
|------|------|--------|--------|
| 0 | UR | U | R |
| 1 | UF | U | F |
| 2 | UL | U | L |
| 3 | UB | U | B |
| 4 | DR | D | R |
| 5 | DF | D | F |
| 6 | DL | D | L |
| 7 | DB | D | B |
| 8 | FR | F | R |
| 9 | FL | F | L |
| 10 | BL | B | L |
| 11 | BR | B | R |

**Position Cycles** (piece at first index goes to second, etc.):

| Move | Corner Cycle | Edge Cycle |
|------|-------------|------------|
| U | 0→3→2→1 | 0→3→2→1 |
| D | 4→7→6→5 | 4→7→6→5 |
| R | 0→3→7→4 | 0→11→4→8 |
| L | 1→5→6→2 | 2→9→6→10 |
| F | 0→4→5→1 | 1→8→5→9 |
| B | 3→2→6→7 | 3→10→7→11 |

---

### Relevant Files
- `cube3.py` — **NEW**, geometry-driven cube
- `test_cube3.py` — **NEW**, comprehensive tests
- `cube2.py` — Reference for slot definitions and solved colors only
- `test_cube2.py` — Reference for test structure
- `CFOP_solver.py` — Consumer expecting `copy()`, `apply_move()`, `apply_moves()`

### Verification
1. `pytest test_cube3.py` — all pass
2. M^4 = identity for all 6 faces (catches the cube2 R bug)
3. M + M' = identity for all faces
4. (R U R' U')^6 = identity
5. Orientation parity invariants after random scrambles
6. Specific sticker positions verified after known moves

### Decisions
- **CW = standard Rubik's notation** (CW from outside the face). Differs from cube2.py on some faces.
- **CCW = CW x 3**: No separate inverse code. Eliminates need to maintain/verify 12 separate move implementations.
- **Scope**: cube3.py + test_cube3.py only. Solver/visualizer integration is out of scope.
