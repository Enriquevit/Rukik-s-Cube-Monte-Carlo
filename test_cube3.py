import pytest
from cube3 import (
    Cube, SOLVED_CORNERS, SOLVED_EDGES,
    CORNER_SLOT_FACES, EDGE_SLOT_FACES, FACE_COLORS,
)


# ========== Fixtures ==========

@pytest.fixture
def solved_cube():
    return Cube()


@pytest.fixture
def cube_with_scramble():
    cube = Cube()
    cube.apply_moves(["R", "U", "R'", "U'"])
    return cube


# ========== Helpers ==========

def corner_orientation_sum(cube):
    return sum(cube.get_corner_orientation(i) for i in range(8)) % 3


def edge_orientation_sum(cube):
    return sum(cube.get_edge_orientation(i) for i in range(12)) % 2


def all_corner_stickers(cube):
    return [list(c) for c in cube.corners]


def all_edge_stickers(cube):
    return [list(e) for e in cube.edges]


def has_duplicate_pieces(cube):
    cs = [tuple(c) for c in cube.corners]
    es = [tuple(e) for e in cube.edges]
    return len(set(cs)) < len(cs) or len(set(es)) < len(es)


def reverse_moves(moves):
    rev = []
    for m in reversed(moves):
        if "'" in m:
            rev.append(m.replace("'", ""))
        elif "2" in m:
            rev.append(m)
        else:
            rev.append(m + "'")
    return rev


# ========== 1. Initialization ==========

class TestInitialization:
    def test_8_corners(self, solved_cube):
        assert len(solved_cube.corners) == 8

    def test_12_edges(self, solved_cube):
        assert len(solved_cube.edges) == 12

    def test_is_solved(self, solved_cube):
        assert solved_cube.is_solved()

    def test_corner_stickers_match_solved(self, solved_cube):
        for i in range(8):
            assert solved_cube.corners[i] == SOLVED_CORNERS[i]

    def test_edge_stickers_match_solved(self, solved_cube):
        for i in range(12):
            assert solved_cube.edges[i] == SOLVED_EDGES[i]

    def test_all_corner_orientations_zero(self, solved_cube):
        for i in range(8):
            assert solved_cube.get_corner_orientation(i) == 0

    def test_all_edge_orientations_zero(self, solved_cube):
        for i in range(12):
            assert solved_cube.get_edge_orientation(i) == 0

    def test_solved_stickers_via_get_sticker(self, solved_cube):
        for face in "UDFRBL":
            assert solved_cube.get_sticker(face, 1, 1) == FACE_COLORS[face]
        # Spot-check a corner sticker: URF's U sticker at U(2,2)
        assert solved_cube.get_sticker('U', 2, 2) == 'W'
        # Spot-check an edge sticker: UF's F sticker at F(0,1)
        assert solved_cube.get_sticker('F', 0, 1) == 'G'


# ========== 2. Single Move Tests ==========

class TestSingleMoves:
    # --- U ---
    def test_U_only_moves_top_corners(self, solved_cube):
        solved_cube.apply_move("U")
        for i in range(4, 8):
            assert solved_cube.corners[i] == SOLVED_CORNERS[i]

    def test_U_only_moves_top_edges(self, solved_cube):
        solved_cube.apply_move("U")
        for i in range(4, 12):
            assert solved_cube.edges[i] == SOLVED_EDGES[i]

    def test_U_no_corner_orientation_change(self, solved_cube):
        solved_cube.apply_move("U")
        for i in range(8):
            assert solved_cube.get_corner_orientation(i) == 0

    def test_U_no_edge_orientation_change(self, solved_cube):
        solved_cube.apply_move("U")
        for i in range(12):
            assert solved_cube.get_edge_orientation(i) == 0

    # --- D ---
    def test_D_only_moves_bottom_corners(self, solved_cube):
        solved_cube.apply_move("D")
        for i in range(4):
            assert solved_cube.corners[i] == SOLVED_CORNERS[i]

    def test_D_only_moves_bottom_edges(self, solved_cube):
        solved_cube.apply_move("D")
        for i in range(4):
            assert solved_cube.edges[i] == SOLVED_EDGES[i]
        for i in range(8, 12):
            assert solved_cube.edges[i] == SOLVED_EDGES[i]

    def test_D_no_corner_orientation_change(self, solved_cube):
        solved_cube.apply_move("D")
        for i in range(8):
            assert solved_cube.get_corner_orientation(i) == 0

    def test_D_no_edge_orientation_change(self, solved_cube):
        solved_cube.apply_move("D")
        for i in range(12):
            assert solved_cube.get_edge_orientation(i) == 0

    # --- R ---
    def test_R_changes_corner_orientation(self, solved_cube):
        solved_cube.apply_move("R")
        changed = any(solved_cube.get_corner_orientation(i) != 0 for i in range(8))
        assert changed

    def test_R_no_edge_orientation_change(self, solved_cube):
        solved_cube.apply_move("R")
        for i in range(12):
            assert solved_cube.get_edge_orientation(i) == 0

    # --- L ---
    def test_L_changes_corner_orientation(self, solved_cube):
        solved_cube.apply_move("L")
        changed = any(solved_cube.get_corner_orientation(i) != 0 for i in range(8))
        assert changed

    def test_L_no_edge_orientation_change(self, solved_cube):
        solved_cube.apply_move("L")
        for i in range(12):
            assert solved_cube.get_edge_orientation(i) == 0

    # --- F ---
    def test_F_changes_corner_orientation(self, solved_cube):
        solved_cube.apply_move("F")
        changed = any(solved_cube.get_corner_orientation(i) != 0 for i in range(8))
        assert changed

    def test_F_changes_edge_orientation(self, solved_cube):
        solved_cube.apply_move("F")
        changed = any(solved_cube.get_edge_orientation(i) != 0 for i in range(12))
        assert changed

    # --- B ---
    def test_B_changes_corner_orientation(self, solved_cube):
        solved_cube.apply_move("B")
        changed = any(solved_cube.get_corner_orientation(i) != 0 for i in range(8))
        assert changed

    def test_B_changes_edge_orientation(self, solved_cube):
        solved_cube.apply_move("B")
        changed = any(solved_cube.get_edge_orientation(i) != 0 for i in range(12))
        assert changed

    # --- move + inverse = identity ---
    @pytest.mark.parametrize("face", list("UDLRFB"))
    def test_move_plus_inverse_is_identity(self, face):
        cube = Cube()
        cube.apply_move(face)
        cube.apply_move(face + "'")
        assert cube.is_solved()

    @pytest.mark.parametrize("face", list("UDLRFB"))
    def test_double_move_equals_two_singles(self, face):
        c1 = Cube()
        c1.apply_move(face + "2")
        c2 = Cube()
        c2.apply_move(face)
        c2.apply_move(face)
        assert c1.corners == c2.corners and c1.edges == c2.edges


# ========== 3. Move Sequences ==========

class TestMoveSequences:
    @pytest.mark.parametrize("face", list("UDLRFB"))
    def test_quarter_turn_x4_is_identity(self, face):
        cube = Cube()
        for _ in range(4):
            cube.apply_move(face)
        assert cube.is_solved(), f"{face}^4 should be identity"

    def test_sexy_move_x6_is_identity(self, solved_cube):
        for _ in range(6):
            solved_cube.apply_moves(["R", "U", "R'", "U'"])
        assert solved_cube.is_solved()

    def test_T_perm_preserves_orientation_parity(self, solved_cube):
        t_perm = ["R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'", "U'",
                   "R", "U", "R'", "F'"]
        solved_cube.apply_moves(t_perm)
        assert corner_orientation_sum(solved_cube) == 0
        assert edge_orientation_sum(solved_cube) == 0
        assert not has_duplicate_pieces(solved_cube)

    def test_T_perm_twice_is_identity(self, solved_cube):
        t_perm = ["R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'", "U'",
                   "R", "U", "R'", "F'"]
        solved_cube.apply_moves(t_perm)
        solved_cube.apply_moves(t_perm)
        assert solved_cube.is_solved()


# ========== 4. Orientation Invariants ==========

class TestOrientationInvariants:
    @pytest.mark.parametrize("moves", [
        ["U"], ["R"], ["F"], ["B"], ["L"], ["D"],
        ["R", "U", "R'", "U'"],
        ["U", "R", "F", "U'", "R'", "F'"],
        ["F", "R", "U", "B", "L", "D"],
    ])
    def test_corner_sum_mod3_zero(self, moves):
        cube = Cube()
        cube.apply_moves(moves)
        assert corner_orientation_sum(cube) == 0

    @pytest.mark.parametrize("moves", [
        ["U"], ["R"], ["F"], ["B"], ["L"], ["D"],
        ["R", "U", "R'", "U'"],
        ["F", "B", "F'", "B'"],
    ])
    def test_edge_sum_mod2_zero(self, moves):
        cube = Cube()
        cube.apply_moves(moves)
        assert edge_orientation_sum(cube) == 0


# ========== 5. Piece Identity ==========

class TestPieceIdentity:
    def test_corner_colors_preserved(self, solved_cube):
        orig = sorted(frozenset(c) for c in solved_cube.corners)
        solved_cube.apply_moves(["R", "U", "F", "D"])
        final = sorted(frozenset(c) for c in solved_cube.corners)
        assert orig == final

    def test_edge_colors_preserved(self, solved_cube):
        orig = sorted(frozenset(e) for e in solved_cube.edges)
        solved_cube.apply_moves(["R", "U", "F", "D"])
        final = sorted(frozenset(e) for e in solved_cube.edges)
        assert orig == final

    def test_no_duplicate_corners(self, solved_cube):
        solved_cube.apply_moves(["R", "U", "R'", "U'", "F", "D", "F'", "D'"])
        assert len(set(tuple(c) for c in solved_cube.corners)) == 8

    def test_no_duplicate_edges(self, solved_cube):
        solved_cube.apply_moves(["R", "U", "R'", "U'", "F", "D", "F'", "D'"])
        assert len(set(tuple(e) for e in solved_cube.edges)) == 12

    def test_no_duplicates_after_long_sequence(self, solved_cube):
        solved_cube.apply_moves(["R", "U", "R'", "U'"] * 10)
        assert not has_duplicate_pieces(solved_cube)


# ========== 6. Scramble ==========

class TestScramble:
    def test_scramble_almost_always_unsolved(self):
        unsolved = sum(1 for _ in range(10) if not Cube().scramble(20) or True
                       if not Cube() or True)
        # Redo properly:
        unsolved = 0
        for _ in range(10):
            c = Cube()
            c.scramble(20)
            if not c.is_solved():
                unsolved += 1
        assert unsolved >= 9

    def test_scramble_preserves_pieces(self):
        c = Cube()
        orig_c = sorted(frozenset(x) for x in c.corners)
        orig_e = sorted(frozenset(x) for x in c.edges)
        c.scramble(20)
        assert sorted(frozenset(x) for x in c.corners) == orig_c
        assert sorted(frozenset(x) for x in c.edges) == orig_e

    def test_scramble_preserves_corner_parity(self):
        c = Cube()
        c.scramble(20)
        assert corner_orientation_sum(c) == 0

    def test_scramble_preserves_edge_parity(self):
        c = Cube()
        c.scramble(20)
        assert edge_orientation_sum(c) == 0

    def test_scramble_returns_move_list(self):
        c = Cube()
        moves = c.scramble(5)
        assert isinstance(moves, list) and len(moves) == 5


# ========== 7. Round-Trip ==========

class TestRoundTrip:
    def test_sequence_plus_inverse(self, solved_cube):
        seq = ["R", "U", "F", "D", "L", "B", "U'", "R'"]
        solved_cube.apply_moves(seq)
        assert not solved_cube.is_solved()
        solved_cube.apply_moves(reverse_moves(seq))
        assert solved_cube.is_solved()

    @pytest.mark.parametrize("seq", [
        ["R"], ["R", "U"], ["R", "U", "R'", "U'"], ["F", "R", "U"],
    ])
    def test_round_trip_parameterized(self, seq):
        c = Cube()
        c.apply_moves(seq)
        c.apply_moves(reverse_moves(seq))
        assert c.is_solved()

    def test_double_move_self_inverse(self, solved_cube):
        solved_cube.apply_move("R2")
        assert not solved_cube.is_solved()
        solved_cube.apply_move("R2")
        assert solved_cube.is_solved()


# ========== 8. Reset / State ==========

class TestResetAndState:
    def test_reset_returns_to_solved(self, cube_with_scramble):
        assert not cube_with_scramble.is_solved()
        cube_with_scramble.reset()
        assert cube_with_scramble.is_solved()

    def test_copy_is_independent(self, solved_cube):
        c2 = solved_cube.copy()
        c2.apply_move("R")
        assert solved_cube.is_solved()
        assert not c2.is_solved()


# ========== 9. Move Notation ==========

class TestMoveNotation:
    def test_all_faces_all_modifiers(self):
        for face in "UDLRFB":
            for mod in ["", "'", "2"]:
                c = Cube()
                c.apply_move(face + mod)
                assert len(c.corners) == 8 and len(c.edges) == 12

    def test_invalid_move(self, solved_cube):
        with pytest.raises(ValueError):
            solved_cube.apply_move("X")
        with pytest.raises(ValueError):
            solved_cube.apply_move("")


# ========== 10. Sticker-Level Correctness ==========

class TestStickerLevel:
    """Verify exact sticker positions after specific moves."""

    def test_R_corner_stickers(self):
        """After R CW, check the 4 affected corner slots."""
        c = Cube()
        c.apply_move("R")
        # Cycle 0→4→7→3.  R face cycle: U→F,F→D,D→B,B→U. inv: F←U,D←F,B←D,U←B
        # Old URF=[W,R,G] → DFR(4). DFR faces (D,F,R).
        # D←inv[D]=F, F stays, R stays → D=G(was F@2), F=W(was U@0→inv F←U), R=R
        # Actually: D: inv[D]=F → src F@idx2=G. F: F stays → src F@idx2... no.
        # For DFR dst faces (D,F,R): D←inv[D]=F→src(U,R,F) F@2=G; F stays→F@2=G? No!
        # Correct: For each dst face, find inv mapping:
        # D: inv[D]=F → look up F in src (U,R,F) → idx 2 → sticker G
        # F: inv[F]=U → look up U in src (U,R,F) → idx 0 → sticker W
        # R: R stays → idx 1 → sticker R
        assert c.corners[4] == ['G', 'W', 'R']
        # Old DFR=[Y,G,R] → DRB(7). DRB faces (D,R,B).
        # D: inv[D]=F → src(D,F,R) F@1=G. R: R→R@2=R. B: inv[B]=D→D@0=Y.
        assert c.corners[7] == ['G', 'R', 'Y']
        # Old DRB=[Y,R,B] → UBR(3). UBR faces (U,B,R).
        # U: inv[U]=B → src(D,R,B) B@2=B. B: inv[B]=D→D@0=Y. R: R→R@1=R.
        assert c.corners[3] == ['B', 'Y', 'R']
        # Old UBR=[W,B,R] → URF(0). URF faces (U,R,F).
        # U: inv[U]=B → src(U,B,R) B@1=B. R: R→R@2=R. F: inv[F]=U→U@0=W.
        assert c.corners[0] == ['B', 'R', 'W']

    def test_R_edge_stickers(self):
        """After R CW, check the 4 affected edge slots."""
        c = Cube()
        c.apply_move("R")
        # Cycle 0→8→4→11.  R inv: F←U, D←F, B←D, U←B
        # Old UR=[W,R] → FR(8): F←U=W, R=R → [W,R]
        assert c.edges[8] == ['W', 'R']
        # Old FR=[G,R] → DR(4): D←F=G, R=R → [G,R]
        assert c.edges[4] == ['G', 'R']
        # Old DR=[Y,R] → BR(11): B←D=Y, R=R → [Y,R]
        assert c.edges[11] == ['Y', 'R']
        # Old BR=[B,R] → UR(0): U←B=B, R=R → [B,R]
        assert c.edges[0] == ['B', 'R']

    def test_F_corner_stickers(self):
        """After F CW, check affected corners."""
        c = Cube()
        c.apply_move("F")
        # Cycle 0→4→5→1. Face cycle: U→R,R→D,D→L,L→U. inv: R←U,D←R,L←D,U←L
        # Old URF=[W,R,G] → DFR(4). DFR faces (D,F,R).
        # D: inv[D]=R → src(U,R,F) R@1=R. F: F→F@2=G. R: inv[R]=U→U@0=W.
        assert c.corners[4] == ['R', 'G', 'W']
        # Old DFR=[Y,G,R] → DLF(5). DLF faces (D,L,F).
        # D: inv[D]=R → src(D,F,R) R@2=R. L: inv[L]=D→D@0=Y. F: F→F@1=G.
        assert c.corners[5] == ['R', 'Y', 'G']
        # Old DLF=[Y,O,G] → UFL(1). UFL faces (U,F,L).
        # U: inv[U]=L → src(D,L,F) L@1=O. F: F→F@2=G. L: inv[L]=D→D@0=Y.
        assert c.corners[1] == ['O', 'G', 'Y']
        # Old UFL=[W,G,O] → URF(0). URF faces (U,R,F).
        # U: inv[U]=L → src(U,F,L) L@2=O. R: inv[R]=U→U@0=W. F: F→F@1=G.
        assert c.corners[0] == ['O', 'W', 'G']

    def test_U_corner_permutation(self):
        """After U CW, corners cycle 0→3→2→1 with no sticker twist."""
        c = Cube()
        c.apply_move("U")
        # Old URF=[W,R,G] → UBR. UBR faces (U,B,R). inv: R←F,B←R,L←B,F←L.
        # U: U. B: inv[B]=R → R@1=R. R: inv[R]=F → F@2=G.
        assert c.corners[3] == ['W', 'R', 'G']
        # Old UBR=[W,B,R] → ULB.
        # U: W. L: inv[L]=B → B@1=B. B: inv[B]=R → R@2=R.
        assert c.corners[2] == ['W', 'B', 'R']
        # Old ULB=[W,O,B] → UFL.
        # U: W. F: inv[F]=L → L@1=O. L: inv[L]=B → B@2=B.
        assert c.corners[1] == ['W', 'O', 'B']
        # Old UFL=[W,G,O] → URF.
        # U: W. R: inv[R]=F → F@1=G. F: inv[F]=L → L@2=O.
        assert c.corners[0] == ['W', 'G', 'O']

    def test_D_corner_permutation(self):
        """After D CW, corners cycle 4→5→6→7."""
        c = Cube()
        c.apply_move("D")
        # D face cycle: F→L,L→B,B→R,R→F. inv: L←F,B←L,R←B,F←R.
        # Old DFR=[Y,G,R] → DLF. DLF faces (D,L,F).
        # D: Y. L: inv[L]=F → src F@1=G. F: inv[F]=R → src R@2=R.
        assert c.corners[5] == ['Y', 'G', 'R']
        # Old DLF=[Y,O,G] → DBL. DBL faces (D,B,L).
        # D: Y. B: inv[B]=L → src L@1=O. L: inv[L]=F → src F@2=G.
        assert c.corners[6] == ['Y', 'O', 'G']
        # Old DBL=[Y,B,O] → DRB. DRB faces (D,R,B).
        # D: Y. R: inv[R]=B → src B@1=B. B: inv[B]=L → src L@2=O.
        assert c.corners[7] == ['Y', 'B', 'O']
        # Old DRB=[Y,R,B] → DFR. DFR faces (D,F,R).
        # D: Y. F: inv[F]=R → src R@1=R. R: inv[R]=B → src B@2=B.
        assert c.corners[4] == ['Y', 'R', 'B']

    def test_get_sticker_after_R(self):
        """Verify specific face stickers after R CW."""
        c = Cube()
        c.apply_move("R")
        # After R, URF corner slot 0 has [B,R,W].
        # U face (2,2) = corner 0 sticker 0 = B
        assert c.get_sticker('U', 2, 2) == 'B'
        # R face (0,0) = corner 0 sticker 1 = R
        assert c.get_sticker('R', 0, 0) == 'R'
        # F face (0,2) = corner 0 sticker 2 = W
        assert c.get_sticker('F', 0, 2) == 'W'


# ========== 11. Known Algorithm Tests ==========

class TestKnownAlgorithms:
    def test_superflip_is_not_solved(self):
        """Superflip flips all 12 edges in place."""
        superflip = "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2".split()
        c = Cube()
        c.apply_moves(superflip)
        assert not c.is_solved()
        # All corners should be in place with orientation 0
        for i in range(8):
            assert c.corners[i] == SOLVED_CORNERS[i]
        # All edges should be flipped (orientation 1)
        for i in range(12):
            assert c.get_edge_orientation(i) == 1

    @pytest.mark.parametrize("face", list("UDLRFB"))
    def test_half_turn_x2_is_identity(self, face):
        c = Cube()
        c.apply_move(face + "2")
        c.apply_move(face + "2")
        assert c.is_solved()

    def test_RU_order_63(self):
        """(R U) has order 63 — applying 63 times returns to solved."""
        c = Cube()
        for _ in range(63):
            c.apply_moves(["R", "U"])
        assert c.is_solved()

    def test_sune_x6_is_identity(self):
        """Sune (R U R' U R U2 R') applied 6 times = identity."""
        sune = ["R", "U", "R'", "U", "R", "U2", "R'"]
        c = Cube()
        for _ in range(6):
            c.apply_moves(sune)
        assert c.is_solved()
