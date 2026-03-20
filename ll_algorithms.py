"""
ll_algorithms.py  —  Last-Layer algorithm database (57 OLL + 21 PLL)

All algorithms are stored in **standard notation** (yellow = U, white = D,
last layer on top).  Since cube3.py has white = U and yellow = D, the
``to_d_layer`` helper applies an x2 rotation so the algorithms target the
D layer instead:

    U ↔ D,  F ↔ B,  R → R,  L → L   (suffixes preserved)

Face-move-only — no wide moves, slice moves, or rotations.
"""

from typing import Dict, List

# ────────────────────────────────────────────────────────────
#  Helpers
# ────────────────────────────────────────────────────────────

_X2_MAP = {"U": "D", "D": "U", "R": "R", "L": "L", "F": "B", "B": "F"}


def _convert_move(move: str) -> str:
    """Convert a single move token via x2 (U↔D, F↔B)."""
    return _X2_MAP[move[0]] + move[1:]


def to_d_layer(alg: str) -> List[str]:
    """Space-separated standard alg → list of D-layer move strings."""
    return [_convert_move(m) for m in alg.split()]


def invert_move(m: str) -> str:
    """R→R', R'→R, R2→R2."""
    if m.endswith("'"):
        return m[:-1]
    if m.endswith("2"):
        return m
    return m + "'"


def invert_alg(moves: List[str]) -> List[str]:
    """Return the inverse of a move sequence (reverse + invert each)."""
    return [invert_move(m) for m in reversed(moves)]


# ────────────────────────────────────────────────────────────
#  OLL — 57 cases  (standard notation, U = last layer)
# ────────────────────────────────────────────────────────────

_OLL_STD: Dict[int, str] = {
    # ── All edges oriented (cross on U already) ──────────
    21: "R U2 R' U' R U R' U' R U' R'",
    22: "R U2 R2 U' R2 U' R2 U2 R",
    23: "R2 D' R U2 R' D R U2 R",
    24: "L F R' F' L' F R F'",
    25: "F' L F R' F' L' F R",
    26: "R U2 R' U' R U' R'",
    27: "R U R' U R U2 R'",

    # ── T-shapes ─────────────────────────────────────────
    33: "R U R' U' R' F R F'",
    45: "F R U R' U' F'",

    # ── Squares ──────────────────────────────────────────
    5:  "L' B2 R B R' B L",
    6:  "R B2 L' B' L B' R'",

    # ── C-shapes ─────────────────────────────────────────
    34: "R U R2 U' R' F R U R U' F'",
    46: "R' U' R' F R F' U R",

    # ── W-shapes ─────────────────────────────────────────
    36: "L' U' L U' L' U L U L F' L' F",
    38: "R U R' U R U' R' U' R' F R F'",

    # ── P-shapes ─────────────────────────────────────────
    31: "R' U' F U R U' R' F' R",
    32: "L U F' U' L' U L F L'",
    43: "F' U' L' U L F",
    44: "F U R U' R' F'",

    # ── Fish shapes ──────────────────────────────────────
    9:  "R U R' U' R' F R2 U R' U' F'",
    10: "R U R' U R' F R F' R U2 R'",
    35: "R U2 R2 F R F' R U2 R'",
    37: "F R' F' R U R U' R'",

    # ── Knight-move shapes ───────────────────────────────
    13: "F U R U2 R' U' R U R' F'",
    14: "R' F R U R' F' R F U' F'",
    15: "L' B' L R' U' R U L' B L",
    16: "R B R' L U L' U' R B' R'",

    # ── Awkward shapes ───────────────────────────────────
    29: "R U R' U' R U' R' F' U' F R U R'",
    30: "F U R U2 R' U' R U2 R' U' F'",
    41: "R U R' U R U2 R' F R U R' U' F'",
    42: "R' U' R U' R' U2 R F R U R' U' F'",

    # ── L-shapes ─────────────────────────────────────────
    47: "R' U' R' F R F' U R",
    48: "F R U R' U' R U R' U' F'",
    49: "R B' R2 F R2 B R2 F' R",
    50: "R B' R B R2 F' R' F R'",
    51: "F U R U' R' U R U' R' F'",
    52: "R U R' U R U' B U' B' R'",
    53: "L' B' L U' R' U R U' R' U R L' B L",
    54: "R B R' U L U' L' U L U' L' R B' R'",
    55: "R U2 R2 U' R U' R' U2 F R F'",
    56: "F R U R' U' R F' L F R' F' L'",

    # ── Dot cases (no edges oriented) ────────────────────
    1:  "R U2 R2 F R F' U2 R' F R F'",
    2:  "F R U R' U' F' B U L U' L' B'",
    3:  "F U R U' R' F' U F R U R' U' F'",
    4:  "F U R U' R' F' U' F R U R' U' F'",
    17: "R U R' U R' F R F' U2 R' F R F'",
    18: "F R U R' U' F' U2 F R U R' U' F'",
    19: "R' U2 F R U R' U' F2 U2 F R",
    20: "R U R' U' R' F R F' R U R' U' R' F R F'",

    # ── Lightning / line shapes ──────────────────────────
    7:  "R B L' B' R' B L B'",
    8:  "L' B' R B L B' R' B",
    11: "F' L' U' L U F U' F' L' U' L U F",
    12: "F R U R' U' F' U F R U R' U' F'",

    # ── Big lightning ────────────────────────────────────
    39: "L F' L' U' L U F U' L'",
    40: "R' F R U R' U' F' U R",

    # ── Remaining ────────────────────────────────────────
    28: "R' F R B' R' F' R B",
    57: "R U R' U' L R' F R F' L'",
}

# ────────────────────────────────────────────────────────────
#  PLL — 21 cases  (standard notation, U = last layer)
# ────────────────────────────────────────────────────────────

_PLL_STD: Dict[str, str] = {
    # ── Edge-only permutations ───────────────────────────
    "Ua": "R U' R U R U R U' R' U' R2",
    "Ub": "R2 U R U R' U' R' U' R' U R'",
    "Z":  "R' U' R U' R U R U' R' U R U R2 U' R'",
    "H":  "R2 U2 R U2 R2 U2 R2 U2 R U2 R2",

    # ── Corner-only permutations ─────────────────────────
    "Aa": "R' F R' B2 R F' R' B2 R2",
    "Ab": "R2 B2 R F R' B2 R F' R",
    "E":  "R B' R' F R B R' F' R B R' F R B' R' F'",

    # ── Adjacent swap ────────────────────────────────────
    "T":  "R U R' U' R' F R2 U' R' U' R U R' F'",
    "F":  "R' U' F' R U R' U' R' F R2 U' R' U' R U R' U R",
    "Ja": "R' U L' U2 R U' R' U2 R L",
    "Jb": "R U R' F' R U R' U' R' F R2 U' R'",
    "Ra": "R U' R' U' R U R D R' U' R D' R' U2 R'",
    "Rb": "R' U2 R U2 R' F R U R' U' R' F' R2",

    # ── Diagonal swap ────────────────────────────────────
    "V":  "R' U R' U' B' R' B2 U' B' U B' R B R",
    "Y":  "F R U' R' U' R U R' F' R U R' U' R' F R F'",
    "Na": "R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'",
    "Nb": "R' U R' F R F' R U' R' F' U F R U R' U' R",

    # ── G permutations (double adjacent swap) ────────────
    "Ga": "R2 U R' U R' U' R U' R2 D U' R' U R D'",
    "Gb": "R' U' R U D' R2 U R' U R U' R U' R2 D",
    "Gc": "R2 U' R U' R U R' U R2 D' U R U' R' D",
    "Gd": "R U R' U' D R2 U' R U' R' U R' U R2 D'",
}

# ────────────────────────────────────────────────────────────
#  Pre-converted to D-layer notation for cube3.py
# ────────────────────────────────────────────────────────────

OLL_ALGORITHMS: Dict[int, List[str]] = {
    n: to_d_layer(a) for n, a in _OLL_STD.items()
}

PLL_ALGORITHMS: Dict[str, List[str]] = {
    n: to_d_layer(a) for n, a in _PLL_STD.items()
}

# Flat lists for random selection
ALL_OLL: List[List[str]] = list(OLL_ALGORITHMS.values())
ALL_PLL: List[List[str]] = list(PLL_ALGORITHMS.values())
