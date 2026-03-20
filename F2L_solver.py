"""
F2L_solver.py  —  First Two Layers solver for cube3.py

Solves 4 corner-edge pairs into the D-layer slots after the cross is done.

F2L slots (corner_slot, edge_slot):
  FR: corner 4 (DFR) + edge 8  (FR)
  FL: corner 5 (DLF) + edge 9  (FL)
  BL: corner 6 (DBL) + edge 10 (BL)
  BR: corner 7 (DRB) + edge 11 (BR)

Architecture:
  1. classify_f2l_case() — returns a case_id string
  2. F2L_ALGORITHMS     — auto-generated lookup table: case_id → moves
  3. solve_f2l_slot()   — table lookup with BFS fallback
  4. solve_f2l()        — solve all 4 slots in order
"""

from typing import List, Tuple, Optional, Dict
from collections import deque
from cube3 import (Cube, CORNER_SLOT_FACES, EDGE_SLOT_FACES,
                   FACE_COLORS, SOLVED_CORNERS, SOLVED_EDGES)

# ────────────────────────────────────────────────────────────
# Slot definitions
# ────────────────────────────────────────────────────────────

# (corner_slot, edge_slot, u_corner_partner, right_face, front_face)
SLOT_INFO = {
    'FR': (4, 8,  0, 'R', 'F'),
    'FL': (5, 9,  1, 'F', 'L'),
    'BL': (6, 10, 2, 'L', 'B'),
    'BR': (7, 11, 3, 'B', 'R'),
}
SLOT_ORDER = ['FR', 'FL', 'BL', 'BR']

F2L_TARGETS = {
    name: {'corner': SOLVED_CORNERS[info[0]], 'edge': SOLVED_EDGES[info[1]]}
    for name, info in SLOT_INFO.items()
}

# Moves available for each slot (the two adjacent faces + D)
# Cross is on U, so D is the free working layer (like U in standard CFOP)
SLOT_MOVES = {
    'FR': ["R", "R'", "F", "F'", "D", "D'"],
    'FL': ["F", "F'", "L", "L'", "D", "D'"],
    'BL': ["L", "L'", "B", "B'", "D", "D'"],
    'BR': ["B", "B'", "R", "R'", "D", "D'"],
}

INVERSE_MAP = {
    "R": "R'", "R'": "R", "R2": "R2",
    "F": "F'", "F'": "F", "F2": "F2",
    "U": "U'", "U'": "U", "U2": "U2",
    "L": "L'", "L'": "L", "L2": "L2",
    "B": "B'", "B'": "B", "B2": "B2",
    "D": "D'", "D'": "D", "D2": "D2",
}

SLOT_ROTATIONS = {
    'FR': {},
    'FL': {'R': 'F', 'F': 'L', 'L': 'B', 'B': 'R'},
    'BL': {'R': 'L', 'F': 'B', 'L': 'R', 'B': 'F'},
    'BR': {'R': 'B', 'F': 'R', 'L': 'F', 'B': 'L'},
}


def _rotate_move(move: str, rotation: dict) -> str:
    face = move[0]
    suffix = move[1:]
    return rotation.get(face, face) + suffix


def _rotate_alg(alg: List[str], slot: str) -> List[str]:
    rot = SLOT_ROTATIONS[slot]
    if not rot:
        return list(alg)
    return [_rotate_move(m, rot) for m in alg]


def _inverse_alg(alg: List[str]) -> List[str]:
    return [INVERSE_MAP[m] for m in reversed(alg)]


# ────────────────────────────────────────────────────────────
# Piece finding
# ────────────────────────────────────────────────────────────

def _find_corner(cube: Cube, target_stickers: list) -> int:
    tc = frozenset(target_stickers)
    for i in range(8):
        if frozenset(cube.corners[i]) == tc:
            return i
    return -1


def _find_edge(cube: Cube, target_stickers: list) -> int:
    tc = frozenset(target_stickers)
    for i in range(12):
        if frozenset(cube.edges[i]) == tc:
            return i
    return -1


# ────────────────────────────────────────────────────────────
# Case classification
# ────────────────────────────────────────────────────────────

def classify_f2l_case(cube: Cube, slot: str) -> str:
    """Classify an F2L case and return a case_id string.

    Format: "c{slot}o{ori}_e{slot}o{ori}"
    """
    target = F2L_TARGETS[slot]
    cp = _find_corner(cube, target['corner'])
    ep = _find_edge(cube, target['edge'])
    co = cube.get_corner_orientation(cp)
    eo = cube.get_edge_orientation(ep)
    return "c%do%d_e%do%d" % (cp, co, ep, eo)


def _case_key(cube: Cube, slot: str) -> Tuple[int, int, int, int]:
    """Return raw case tuple: (corner_pos, corner_ori, edge_pos, edge_ori)."""
    target = F2L_TARGETS[slot]
    cp = _find_corner(cube, target['corner'])
    ep = _find_edge(cube, target['edge'])
    co = cube.get_corner_orientation(cp)
    eo = cube.get_edge_orientation(ep)
    return (cp, co, ep, eo)


# ────────────────────────────────────────────────────────────
# Algorithm table generation (static lookup for common cases)
# ────────────────────────────────────────────────────────────

def _u_to_d(alg: List[str]) -> List[str]:
    """Convert standard CFOP algorithm (cross-on-D, U working layer)
    to cross-on-U convention (D working layer).
    U→D, U'→D', U2→D2. Other moves unchanged."""
    mapping = {"U": "D", "U'": "D'", "U2": "D2"}
    return [mapping.get(m, m) for m in alg]


# FR-relative base algorithms (standard CFOP notation with U as working layer)
# These get converted to D-notation at table build time.
_FR_BASE_ALGS_STD = [
    ["R", "U", "R'"],
    ["F'", "U'", "F"],
    ["R", "U'", "R'"],
    ["F'", "U", "F"],
    ["R", "U2", "R'"],
    ["F'", "U2", "F"],
    ["R", "U", "R'", "U'", "R", "U", "R'"],
    ["F'", "U'", "F", "U", "F'", "U'", "F"],
    ["R", "U'", "R'", "U", "R", "U", "R'"],
    ["R", "U", "R'", "U'", "R", "U'", "R'"],
    ["F'", "U", "F", "U'", "F'", "U'", "F"],
    ["F'", "U'", "F", "U", "F'", "U", "F"],
    ["R", "U2", "R'", "U", "R", "U'", "R'"],
    ["F'", "U2", "F", "U'", "F'", "U", "F"],
    ["R", "U2", "R'", "U'", "R", "U", "R'"],
    ["F'", "U2", "F", "U", "F'", "U'", "F"],
    ["R", "U'", "R'", "U2", "R", "U", "R'"],
    ["F'", "U", "F", "U2", "F'", "U'", "F"],
    ["R", "U'", "R'", "U2", "R", "U'", "R'"],
    ["F'", "U", "F", "U2", "F'", "U", "F"],
    ["R", "U'", "R'", "U'", "F'", "U", "F"],
    ["F'", "U", "F", "U", "R", "U'", "R'"],
    ["R", "U", "R'", "U'", "F'", "U'", "F"],
    ["F'", "U'", "F", "U", "R", "U", "R'"],
    ["R'", "F", "R", "F'"],
    ["F", "R'", "F'", "R"],
    ["R", "U'", "R'", "U", "R", "U'", "R'"],
    ["F'", "U", "F", "U'", "F'", "U", "F"],
    ["R", "U", "R'", "U'", "R", "U", "R'", "U'", "R", "U", "R'"],
    ["R", "U'", "R'", "U", "R", "U2", "R'", "U", "R", "U'", "R'"],
    ["F'", "U", "F", "U'", "F'", "U2", "F", "U'", "F'", "U", "F"],
    ["R", "U", "R'", "U", "R", "U'", "R'"],
    ["F'", "U'", "F", "U'", "F'", "U", "F"],
    ["R", "U'", "R'", "U'", "F'", "U", "F"],
    ["F'", "U", "F", "U", "R", "U'", "R'"],
]

# Convert to D-notation for cross-on-U
_FR_BASE_ALGS = [_u_to_d(alg) for alg in _FR_BASE_ALGS_STD]

# D premoves (D is the working layer with cross on U)
_D_PREMOVES = [[], ["D"], ["D'"], ["D2"]]


def _build_table_for_slot(slot: str) -> Dict[Tuple[int, int, int, int], List[str]]:
    """Build case_key -> algorithm mapping for one slot via inverse application."""
    cs, es, _, _, _ = SLOT_INFO[slot]
    target_c = SOLVED_CORNERS[cs]
    target_e = SOLVED_EDGES[es]

    table: Dict[Tuple[int, int, int, int], List[str]] = {}

    for base_alg in _FR_BASE_ALGS:
        alg = _rotate_alg(base_alg, slot)
        for premove in _D_PREMOVES:
            full_alg = premove + alg
            inv = _inverse_alg(full_alg)

            c = Cube()
            c.apply_moves(inv)

            cp = _find_corner(c, target_c)
            ep = _find_edge(c, target_e)
            co = c.get_corner_orientation(cp)
            eo = c.get_edge_orientation(ep)

            test = c.copy()
            test.apply_moves(full_alg)
            if test.corners[cs] != target_c or test.edges[es] != target_e:
                continue

            key = (cp, co, ep, eo)
            if key not in table or len(full_alg) < len(table[key]):
                table[key] = full_alg

    return table


def _build_all_tables() -> Dict[str, Dict[Tuple[int, int, int, int], List[str]]]:
    return {slot: _build_table_for_slot(slot) for slot in SLOT_ORDER}


F2L_ALGORITHMS = _build_all_tables()


# ────────────────────────────────────────────────────────────
# BFS solver for a single F2L pair
# ────────────────────────────────────────────────────────────

ALL_MOVES = ["R", "R'", "L", "L'", "F", "F'", "B", "B'", "D", "D'"]

def _bfs_solve_slot(cube: Cube, slot: str, solved_slots: List[str],
                    max_depth: int = 8) -> Optional[List[str]]:
    """IDA*-style DFS to solve one F2L slot, preserving cross and solved slots.

    Uses iterative deepening with the slot's 3-face move set first,
    then falls back to all non-U moves if needed.
    Applies/undoes moves in place for speed (no copies during search).
    """
    from cross_solver import CROSS_EDGE_TARGETS

    cs, es, _, _, _ = SLOT_INFO[slot]
    target_c = F2L_TARGETS[slot]['corner']
    target_e = F2L_TARGETS[slot]['edge']

    # Cross edge targets
    cross_indices = [0, 1, 2, 3]
    cross_tgts = [CROSS_EDGE_TARGETS[s] for s in cross_indices]

    # Preserved slot state
    preserved = []
    for ss in solved_slots:
        sci, sei, _, _, _ = SLOT_INFO[ss]
        preserved.append((sci, sei, list(cube.corners[sci]), list(cube.edges[sei])))

    def _is_goal(c: Cube) -> bool:
        if c.corners[cs] != target_c or c.edges[es] != target_e:
            return False
        for i, idx in enumerate(cross_indices):
            if c.edges[idx] != cross_tgts[i]:
                return False
        for ci, ei, cv, ev in preserved:
            if c.corners[ci] != cv or c.edges[ei] != ev:
                return False
        return True

    if _is_goal(cube):
        return []

    def _ids(move_set, depth_limit):
        """Run IDA* with given move set up to depth_limit."""
        inv = {m: INVERSE_MAP[m] for m in move_set}
        work = cube.copy()
        result = [None]

        def _dfs(path: List[str], depth: int) -> bool:
            if depth == 0:
                if _is_goal(work):
                    result[0] = list(path)
                    return True
                return False

            for move in move_set:
                if path and path[-1][0] == move[0]:
                    continue

                work.apply_move(move)
                path.append(move)

                if _dfs(path, depth - 1):
                    return True

                path.pop()
                work.apply_move(inv[move])

            return False

        for depth in range(1, depth_limit + 1):
            if _dfs([], depth):
                return result[0]
        return None

    # Try with slot-specific moves first (fast)
    slot_moves = SLOT_MOVES[slot]
    result = _ids(slot_moves, min(max_depth, 8))
    if result is not None:
        return result

    # Fallback: all non-U moves (wider search)
    result = _ids(ALL_MOVES, max_depth)
    return result


# ────────────────────────────────────────────────────────────
# Slot and full F2L solving
# ────────────────────────────────────────────────────────────

def is_slot_solved(cube: Cube, slot: str) -> bool:
    cs, es, _, _, _ = SLOT_INFO[slot]
    target = F2L_TARGETS[slot]
    return (cube.corners[cs] == target['corner'] and
            cube.edges[es] == target['edge'])


def is_f2l_complete(cube: Cube) -> bool:
    return all(is_slot_solved(cube, s) for s in SLOT_ORDER)


def _is_valid_solution(cube: Cube, slot: str,
                       solved_slots: List[str]) -> bool:
    from cross_solver import CROSS_EDGE_TARGETS
    if not is_slot_solved(cube, slot):
        return False
    for s in [0, 1, 2, 3]:
        if cube.edges[s] != CROSS_EDGE_TARGETS[s]:
            return False
    for ss in solved_slots:
        if not is_slot_solved(cube, ss):
            return False
    return True


def solve_f2l_slot(cube: Cube, slot: str,
                   solved_slots: Optional[List[str]] = None) -> Tuple[List[str], Cube]:
    """Solve a single F2L slot. Returns (moves, result_cube).

    Strategy: table lookup first (instant), BFS fallback (thorough).
    """
    if solved_slots is None:
        solved_slots = []

    work = cube.copy()

    if is_slot_solved(work, slot):
        return [], work

    # Fast path: static table lookup with U premoves
    table = F2L_ALGORITHMS[slot]
    for d_pre in _D_PREMOVES:
        if d_pre:
            test_pre = work.copy()
            test_pre.apply_moves(d_pre)
        else:
            test_pre = work

        key = _case_key(test_pre, slot)
        if key in table:
            alg = table[key]
            full = d_pre + alg
            test = work.copy()
            test.apply_moves(full)
            if _is_valid_solution(test, slot, solved_slots):
                work.apply_moves(full)
                return full, work

    # BFS fallback
    result = _bfs_solve_slot(work, slot, solved_slots, max_depth=10)
    if result is not None:
        work.apply_moves(result)
        return result, work

    return [], work


def solve_f2l(cube: Cube) -> Tuple[List[str], Cube]:
    """Solve all 4 F2L pairs. Assumes cross is already solved.

    Solves in order: FR -> FL -> BL -> BR.
    Returns (move_list, result_cube).
    """
    work = cube.copy()
    all_moves: List[str] = []
    solved_slots: List[str] = []

    for slot in SLOT_ORDER:
        if is_slot_solved(work, slot):
            solved_slots.append(slot)

    for slot in SLOT_ORDER:
        if slot in solved_slots:
            continue

        moves, work = solve_f2l_slot(work, slot, solved_slots)
        all_moves.extend(moves)

        if is_slot_solved(work, slot):
            solved_slots.append(slot)

    return all_moves, work


# ────────────────────────────────────────────────────────────
# Wrapper class for visualizer compatibility
# ────────────────────────────────────────────────────────────

class F2LSolver:
    """Wrapper providing the API expected by cube_visualizer_3d.py."""

    def solve_f2l(self, cube: Cube) -> Tuple[List[str], Cube]:
        return solve_f2l(cube)
