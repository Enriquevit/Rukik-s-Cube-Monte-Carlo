"""
cube3.py — Geometry-driven Rubik's Cube with sticker-based piece representation.

Moves are defined by face-cycle geometry. Orientation is derived from sticker
positions — no hardcoded orientation deltas.

Coordinate system: +x=R, -x=L, +y=U, -y=D, +z=B, -z=F
Color scheme: U=White, D=Yellow, F=Green, B=Blue, R=Red, L=Orange
"""

import random

# ============================================================
# Slot Faces: which faces each piece position touches
# ============================================================

# Corner slots: (face0, face1, face2) — face0 is always U or D
CORNER_SLOT_FACES = (
    ('U', 'R', 'F'),  # 0: URF
    ('U', 'F', 'L'),  # 1: UFL
    ('U', 'L', 'B'),  # 2: ULB
    ('U', 'B', 'R'),  # 3: UBR
    ('D', 'F', 'R'),  # 4: DFR
    ('D', 'L', 'F'),  # 5: DLF
    ('D', 'B', 'L'),  # 6: DBL
    ('D', 'R', 'B'),  # 7: DRB
)

# Edge slots: (face0, face1) — face0 is U/D for top/bottom, F/B for middle
EDGE_SLOT_FACES = (
    ('U', 'R'),  # 0:  UR
    ('U', 'F'),  # 1:  UF
    ('U', 'L'),  # 2:  UL
    ('U', 'B'),  # 3:  UB
    ('D', 'R'),  # 4:  DR
    ('D', 'F'),  # 5:  DF
    ('D', 'L'),  # 6:  DL
    ('D', 'B'),  # 7:  DB
    ('F', 'R'),  # 8:  FR
    ('F', 'L'),  # 9:  FL
    ('B', 'L'),  # 10: BL
    ('B', 'R'),  # 11: BR
)

# ============================================================
# Face Cycles: CW rotation viewed from outside the face
# Maps old_face → new_face for the 4 adjacent faces
# ============================================================

FACE_CYCLES = {
    'U': {'F': 'R', 'R': 'B', 'B': 'L', 'L': 'F'},
    'D': {'F': 'L', 'L': 'B', 'B': 'R', 'R': 'F'},
    'R': {'U': 'F', 'F': 'D', 'D': 'B', 'B': 'U'},
    'L': {'U': 'B', 'B': 'D', 'D': 'F', 'F': 'U'},
    'F': {'U': 'R', 'R': 'D', 'D': 'L', 'L': 'U'},
    'B': {'U': 'L', 'L': 'D', 'D': 'R', 'R': 'U'},
}

# ============================================================
# Move Cycles: which positions cycle for each CW face move
# Notation: piece at cycle[0] goes to cycle[1], etc.
#
# NOTE: D cycles are (4,5,6,7) — derived from D face cycle
# F→L,L→B,B→R,R→F.  The plan listed (4,7,6,5) which was
# consistent with the OLD (incorrect) D face cycle.
# ============================================================

MOVE_CYCLES = {
    'U': {'corners': (0, 3, 2, 1), 'edges': (0, 3, 2, 1)},
    'D': {'corners': (4, 5, 6, 7), 'edges': (4, 5, 6, 7)},
    'R': {'corners': (0, 4, 7, 3), 'edges': (0, 8, 4, 11)},
    'L': {'corners': (1, 2, 6, 5), 'edges': (2, 10, 6, 9)},
    'F': {'corners': (0, 4, 5, 1), 'edges': (1, 8, 5, 9)},
    'B': {'corners': (3, 2, 6, 7), 'edges': (3, 10, 7, 11)},
}

# ============================================================
# Center colors and solved stickers
# ============================================================

FACE_COLORS = {'U': 'W', 'D': 'Y', 'F': 'G', 'B': 'B', 'R': 'R', 'L': 'O'}

SOLVED_CORNERS = [[FACE_COLORS[f] for f in slot] for slot in CORNER_SLOT_FACES]
SOLVED_EDGES = [[FACE_COLORS[f] for f in slot] for slot in EDGE_SLOT_FACES]

# ============================================================
# Face → Sticker Map
# Maps (face, row, col) to ('corner'|'edge', piece_idx, sticker_idx)
# Center at (1,1) handled separately in get_sticker()
# ============================================================

FACE_STICKER_MAP = {
    'U': {
        (0, 0): ('corner', 2, 0), (0, 1): ('edge', 3, 0), (0, 2): ('corner', 3, 0),
        (1, 0): ('edge', 2, 0),                             (1, 2): ('edge', 0, 0),
        (2, 0): ('corner', 1, 0), (2, 1): ('edge', 1, 0), (2, 2): ('corner', 0, 0),
    },
    'D': {
        (0, 0): ('corner', 5, 0), (0, 1): ('edge', 5, 0), (0, 2): ('corner', 4, 0),
        (1, 0): ('edge', 6, 0),                             (1, 2): ('edge', 4, 0),
        (2, 0): ('corner', 6, 0), (2, 1): ('edge', 7, 0), (2, 2): ('corner', 7, 0),
    },
    'F': {
        (0, 0): ('corner', 1, 1), (0, 1): ('edge', 1, 1), (0, 2): ('corner', 0, 2),
        (1, 0): ('edge', 9, 0),                             (1, 2): ('edge', 8, 0),
        (2, 0): ('corner', 5, 2), (2, 1): ('edge', 5, 1), (2, 2): ('corner', 4, 1),
    },
    'B': {
        (0, 0): ('corner', 3, 1), (0, 1): ('edge', 3, 1), (0, 2): ('corner', 2, 2),
        (1, 0): ('edge', 11, 0),                            (1, 2): ('edge', 10, 0),
        (2, 0): ('corner', 7, 2), (2, 1): ('edge', 7, 1), (2, 2): ('corner', 6, 1),
    },
    'R': {
        (0, 0): ('corner', 0, 1), (0, 1): ('edge', 0, 1), (0, 2): ('corner', 3, 2),
        (1, 0): ('edge', 8, 1),                             (1, 2): ('edge', 11, 1),
        (2, 0): ('corner', 4, 2), (2, 1): ('edge', 4, 1), (2, 2): ('corner', 7, 1),
    },
    'L': {
        (0, 0): ('corner', 2, 1), (0, 1): ('edge', 2, 1), (0, 2): ('corner', 1, 2),
        (1, 0): ('edge', 10, 1),                            (1, 2): ('edge', 9, 1),
        (2, 0): ('corner', 6, 2), (2, 1): ('edge', 6, 1), (2, 2): ('corner', 5, 1),
    },
}


class Cube:
    def __init__(self):
        self.reset()

    def reset(self):
        self.corners = [list(c) for c in SOLVED_CORNERS]
        self.edges = [list(e) for e in SOLVED_EDGES]

    def is_solved(self):
        return self.corners == SOLVED_CORNERS and self.edges == SOLVED_EDGES

    def copy(self):
        new = Cube.__new__(Cube)
        new.corners = [list(c) for c in self.corners]
        new.edges = [list(e) for e in self.edges]
        return new

    # ============================================================
    # Core Move Engine
    # ============================================================

    @staticmethod
    def _remap_stickers(src_stickers, src_faces, dst_faces, inv_cycle):
        result = []
        for df in dst_faces:
            sf = inv_cycle.get(df, df)
            result.append(src_stickers[src_faces.index(sf)])
        return result

    def _apply_cycle(self, pieces, slot_faces, cycle, face_cycle):
        inv_cycle = {v: k for k, v in face_cycle.items()}
        saved = [list(pieces[i]) for i in cycle]
        n = len(cycle)
        for j in range(n):
            src_slot = cycle[j]
            dst_slot = cycle[(j + 1) % n]
            pieces[dst_slot] = self._remap_stickers(
                saved[j], slot_faces[src_slot], slot_faces[dst_slot], inv_cycle
            )

    def _apply_face_cw(self, face):
        cycles = MOVE_CYCLES[face]
        fc = FACE_CYCLES[face]
        self._apply_cycle(self.corners, CORNER_SLOT_FACES, cycles['corners'], fc)
        self._apply_cycle(self.edges, EDGE_SLOT_FACES, cycles['edges'], fc)

    def apply_move(self, move_str):
        if not move_str:
            raise ValueError("Empty move string")
        face = move_str[0]
        if face not in FACE_CYCLES:
            raise ValueError(f"Unknown face: {face}")
        is_prime = "'" in move_str
        is_double = "2" in move_str
        reps = 2 if is_double else (3 if is_prime else 1)
        for _ in range(reps):
            self._apply_face_cw(face)

    def apply_moves(self, move_list):
        for move in move_list:
            self.apply_move(move)

    def scramble(self, num_moves=20):
        faces = ['U', 'D', 'L', 'R', 'F', 'B']
        modifiers = ['', "'", '2']
        moves = []
        last_face = None
        for _ in range(num_moves):
            face = random.choice([f for f in faces if f != last_face])
            modifier = random.choice(modifiers)
            move = face + modifier
            self.apply_move(move)
            moves.append(move)
            last_face = face
        return moves

    # ============================================================
    # Orientation (derived from sticker positions)
    # ============================================================

    def get_corner_orientation(self, idx):
        """0 = U/D sticker on face 0 (correct), 1 or 2 = twisted."""
        for i, s in enumerate(self.corners[idx]):
            if s in ('W', 'Y'):
                return i
        return 0

    def get_edge_orientation(self, idx):
        """0 = oriented, 1 = flipped.

        Reference sticker = U/D color if present, else F/B color.
        Oriented iff reference sticker is at face-index 0 of the slot.
        This ensures U,D,R,L preserve orientation; F,B flip all 4 affected edges.
        """
        stickers = self.edges[idx]
        for i, s in enumerate(stickers):
            if s in ('W', 'Y'):
                return 0 if i == 0 else 1
        for i, s in enumerate(stickers):
            if s in ('G', 'B'):
                return 0 if i == 0 else 1
        return 0

    # ============================================================
    # Sticker Access (for visualization)
    # ============================================================

    def get_sticker(self, face, row, col):
        if row == 1 and col == 1:
            return FACE_COLORS[face]
        ptype, pidx, sidx = FACE_STICKER_MAP[face][(row, col)]
        if ptype == 'corner':
            return self.corners[pidx][sidx]
        return self.edges[pidx][sidx]

    # ============================================================
    # Convenience
    # ============================================================

    def get_corner_position(self, idx):
        return self.corners[idx]

    def get_edge_position(self, idx):
        return self.edges[idx]

    # ============================================================
    # Serialization
    # ============================================================

    _VALID_COLORS = frozenset('WYGBRO')

    def serialize(self) -> str:
        """Return a compact one-line string representing the cube state.

        Format: ``WRG/WGO/.../YRB|WR/WG/.../BR``

        - ``|`` separates corners from edges
        - ``/`` separates individual pieces
        - each piece is its sticker colors concatenated
        """
        corners_str = '/'.join(''.join(c) for c in self.corners)
        edges_str = '/'.join(''.join(e) for e in self.edges)
        return f"{corners_str}|{edges_str}"

    @classmethod
    def deserialize(cls, s: str) -> 'Cube':
        """Create a Cube from a serialized string produced by serialize().

        Raises ValueError for malformed input.  Paste a line from
        logs/cube_states.log directly into this call to recreate a
        state as a test fixture.
        """
        parts = s.strip().split('|')
        if len(parts) != 2:
            raise ValueError(f"Expected 'corners|edges', got {len(parts)} section(s)")
        corner_parts = parts[0].split('/')
        edge_parts = parts[1].split('/')
        if len(corner_parts) != 8:
            raise ValueError(f"Expected 8 corners, got {len(corner_parts)}")
        if len(edge_parts) != 12:
            raise ValueError(f"Expected 12 edges, got {len(edge_parts)}")
        corners = []
        for i, cp in enumerate(corner_parts):
            if len(cp) != 3:
                raise ValueError(f"Corner {i} must have 3 stickers, got {cp!r}")
            if not all(c in cls._VALID_COLORS for c in cp):
                raise ValueError(f"Corner {i} contains invalid color in {cp!r}")
            corners.append(list(cp))
        edges = []
        for i, ep in enumerate(edge_parts):
            if len(ep) != 2:
                raise ValueError(f"Edge {i} must have 2 stickers, got {ep!r}")
            if not all(c in cls._VALID_COLORS for c in ep):
                raise ValueError(f"Edge {i} contains invalid color in {ep!r}")
            edges.append(list(ep))
        cube = cls.__new__(cls)
        cube.corners = corners
        cube.edges = edges
        return cube

    def log_state(self, filepath: str = "logs/cube_states.log") -> None:
        """Append the serialized cube state as one line to *filepath*.

        Creates the directory if it does not exist.
        """
        import os
        dirpath = os.path.dirname(filepath)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        with open(filepath, 'a') as f:
            f.write(self.serialize() + '\n')

    def __repr__(self):
        return (f"Cube(corners={len(self.corners)}, edges={len(self.edges)}, "
                f"solved={self.is_solved()})")


if __name__ == "__main__":
    cube = Cube()
    print(f"Initialized: {cube}")

    cube.apply_move("R")
    print(f"After R: solved={cube.is_solved()}")
    cube.apply_move("R'")
    print(f"After R R': solved={cube.is_solved()}")

    cube.reset()
    for _ in range(6):
        cube.apply_moves(["R", "U", "R'", "U'"])
    print(f"After (R U R' U')×6: solved={cube.is_solved()}")
