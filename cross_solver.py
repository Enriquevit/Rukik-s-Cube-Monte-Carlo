"""
cross_solver.py

CrossSolver class for Rubik's Cube cross solving (beginner).
Uses cube3.py (piece-based representation).

The white cross is solved when the four U-layer edge slots (UR, UF, UL, UB)
each contain the correct edge piece: white on U and the adjacent color matching
the face center.

Edge slot indices:
  0=UR  1=UF  2=UL  3=UB
  4=DR  5=DF  6=DL  7=DB
  8=FR  9=FL  10=BL 11=BR

Edge sticker layout: edges[i] = [face0_color, face1_color]
  where EDGE_SLOT_FACES[i] = (face0, face1)
"""

from collections import deque
from typing import List, Tuple, Dict, Any
from cube3 import Cube, EDGE_SLOT_FACES, FACE_COLORS


# The four cross edge slots and their expected solved colors
CROSS_EDGES = {
    0: ('U', 'R'),
    1: ('U', 'F'),
    2: ('U', 'L'),
    3: ('U', 'B'),
}

CROSS_EDGE_TARGETS = {
    slot: [FACE_COLORS[f] for f in faces]
    for slot, faces in CROSS_EDGES.items()
}

ALL_MOVES = [f + m for f in "UDLRFB" for m in ("", "'", "2")]

# For pruning: moves on the same face are redundant after each other
MOVE_FACE = {mv: mv[0] for mv in ALL_MOVES}
OPPOSITE = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L', 'F': 'B', 'B': 'F'}


class CrossSolver:
    def __init__(self, cross_color: str = 'W'):
        self.cross_color = cross_color

    def is_cross_complete(self, cube: Cube) -> bool:
        """Check if the white cross is complete (edges 0-3 solved)."""
        for slot, target in CROSS_EDGE_TARGETS.items():
            if cube.edges[slot] != target:
                return False
        return True

    def _cross_edges_solved(self, cube: Cube, slots: list) -> bool:
        """Check if specific cross edge slots are solved."""
        for s in slots:
            if cube.edges[s] != CROSS_EDGE_TARGETS[s]:
                return False
        return True

    def _bfs_one_edge(self, cube: Cube, target_slot: int,
                      protected_slots: list, max_depth: int = 7) -> List[str]:
        """BFS to find a short move sequence that places one cross edge
        into target_slot without disturbing any protected_slots.

        Returns the move list, or [] if already solved.
        """
        target_stickers = CROSS_EDGE_TARGETS[target_slot]

        def is_goal(c):
            if c.edges[target_slot] != target_stickers:
                return False
            for s in protected_slots:
                if c.edges[s] != CROSS_EDGE_TARGETS[s]:
                    return False
            return True

        if is_goal(cube):
            return []

        queue = deque()
        queue.append((cube, []))

        while queue:
            state, moves = queue.popleft()
            if len(moves) >= max_depth:
                continue
            last_face = MOVE_FACE[moves[-1]] if moves else None
            for mv in ALL_MOVES:
                mf = MOVE_FACE[mv]
                # Prune: skip moves on same face as last move
                if mf == last_face:
                    continue
                # Prune: for opposite faces (U/D, L/R, F/B) enforce order
                if last_face and mf < last_face and OPPOSITE.get(mf) == last_face:
                    continue
                # Prune: skip moves on same face as last move
                if MOVE_FACE[mv] == last_face:
                    continue
                nxt = state.copy()
                nxt.apply_move(mv)
                new_moves = moves + [mv]
                if is_goal(nxt):
                    return new_moves
                if len(new_moves) < max_depth:
                    queue.append((nxt, new_moves))

        return []  # fallback: couldn't solve within depth limit

    def solve_cross(self, cube: Cube, skill: str = 'beginner') -> Tuple[List[str], Cube]:
        """Solve the cross. Returns (move_list, updated_cube_copy)."""
        return self.solve_cross_beginner(cube)

    def solve_cross_beginner(self, cube: Cube) -> Tuple[List[str], Cube]:
        """Solve the white cross one edge at a time using BFS.

        Each edge is placed with a short BFS search (≤7 moves) that
        also protects all previously-solved cross edges.
        """
        work = cube.copy()
        all_moves: List[str] = []
        solved_so_far: List[int] = []

        for target_slot in [1, 0, 3, 2]:  # UF, UR, UB, UL
            edge_moves = self._bfs_one_edge(work, target_slot, solved_so_far)
            if edge_moves:
                work.apply_moves(edge_moves)
                all_moves.extend(edge_moves)
            solved_so_far.append(target_slot)

        return all_moves, work
