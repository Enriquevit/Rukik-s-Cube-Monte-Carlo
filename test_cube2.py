import pytest
from cube2 import Cube, Piece


# ========== Fixtures ==========

@pytest.fixture
def solved_cube():
    """Provide a solved cube for each test."""
    return Cube()


@pytest.fixture
def cube_with_scramble():
    """Provide a scrambled cube with known moves."""
    cube = Cube()
    cube.apply_moves(["R", "U", "R'", "U'"])
    return cube


# ========== Helper Functions ==========

def get_corner_colors(cube, idx):
    """Get the colors of a corner piece at position idx."""
    return cube.corners[idx].colors


def get_edge_colors(cube, idx):
    """Get the colors of an edge piece at position idx."""
    return cube.edges[idx].colors


def corner_orientation_sum(cube):
    """Sum of all corner orientations mod 3."""
    return sum(c.orientation for c in cube.corners) % 3


def edge_orientation_sum(cube):
    """Sum of all edge orientations mod 2."""
    return sum(e.orientation for e in cube.edges) % 2


def get_all_corner_colors(cube):
    """Get all corner color tuples in order."""
    return [c.colors for c in cube.corners]


def get_all_edge_colors(cube):
    """Get all edge color tuples in order."""
    return [e.colors for e in cube.edges]


def has_duplicate_pieces(cube):
    """Check if there are any duplicate corner or edge pieces."""
    corner_colors = get_all_corner_colors(cube)
    edge_colors = get_all_edge_colors(cube)
    return len(set(corner_colors)) < len(corner_colors) or len(set(edge_colors)) < len(edge_colors)


def reverse_move_sequence(moves):
    """Reverse a move sequence for inverse."""
    reversed_seq = []
    for move in reversed(moves):
        if "'" in move:
            reversed_seq.append(move.replace("'", ""))
        elif "2" in move:
            reversed_seq.append(move)  # Double move is its own inverse
        else:
            reversed_seq.append(move + "'")
    return reversed_seq


# ========== 1. Initialization Tests ==========

class TestInitialization:
    """Test cube initialization and initial state."""
    
    def test_cube_has_8_corners(self, solved_cube):
        """Test that cube has exactly 8 corners."""
        assert len(solved_cube.corners) == 8
    
    def test_cube_has_12_edges(self, solved_cube):
        """Test that cube has exactly 12 edges."""
        assert len(solved_cube.edges) == 12
    
    def test_all_corners_solved_orientation(self, solved_cube):
        """Test that all corners have orientation 0 in solved cube."""
        for i, corner in enumerate(solved_cube.corners):
            assert corner.orientation == 0, f"Corner {i} has orientation {corner.orientation}"
    
    def test_all_edges_solved_orientation(self, solved_cube):
        """Test that all edges have orientation 0 in solved cube."""
        for i, edge in enumerate(solved_cube.edges):
            assert edge.orientation == 0, f"Edge {i} has orientation {edge.orientation}"
    
    def test_is_solved_returns_true_for_new_cube(self, solved_cube):
        """Test that a new cube is identified as solved."""
        assert solved_cube.is_solved() is True
    
    def test_corner_colors_are_correct(self, solved_cube):
        """Test that corner colors match the solved state."""
        expected_colors = [
            ('W', 'R', 'G'),  # 0: URF
            ('W', 'G', 'O'),  # 1: UFL
            ('W', 'O', 'B'),  # 2: ULB
            ('W', 'B', 'R'),  # 3: UBR
            ('Y', 'G', 'R'),  # 4: DFR
            ('Y', 'O', 'G'),  # 5: DLF
            ('Y', 'B', 'O'),  # 6: DBL
            ('Y', 'R', 'B'),  # 7: DRB
        ]
        for i, expected in enumerate(expected_colors):
            assert solved_cube.corners[i].colors == expected
    
    def test_edge_colors_are_correct(self, solved_cube):
        """Test that edge colors match the solved state."""
        expected_colors = [
            ('W', 'R'),   # 0: UR
            ('W', 'G'),   # 1: UF
            ('W', 'O'),   # 2: UL
            ('W', 'B'),   # 3: UB
            ('Y', 'R'),   # 4: DR
            ('Y', 'G'),   # 5: DF
            ('Y', 'O'),   # 6: DL
            ('Y', 'B'),   # 7: DB
            ('R', 'G'),   # 8: FR
            ('G', 'O'),   # 9: FL
            ('O', 'B'),   # 10: BL
            ('B', 'R'),   # 11: BR
        ]
        for i, expected in enumerate(expected_colors):
            assert solved_cube.edges[i].colors == expected


# ========== 2. Single Move Tests ==========

class TestSingleMoves:
    """Test individual moves: U, D, L, R, F, B."""
    
    def test_U_only_affects_top_corners(self, solved_cube):
        """Test that U move only permutes corners 0, 1, 2, 3."""
        solved_cube.apply_move("U")
        # Bottom corners (4-7) should not move
        assert solved_cube.corners[4] == Cube.SOLVED_CORNERS[4]
        assert solved_cube.corners[5] == Cube.SOLVED_CORNERS[5]
        assert solved_cube.corners[6] == Cube.SOLVED_CORNERS[6]
        assert solved_cube.corners[7] == Cube.SOLVED_CORNERS[7]
    
    def test_U_only_affects_top_edges(self, solved_cube):
        """Test that U move only permutes edges 0, 1, 2, 3."""
        solved_cube.apply_move("U")
        # Bottom edges (4-7) should not move
        for i in range(4, 8):
            assert solved_cube.edges[i] == Cube.SOLVED_EDGES[i]
    
    def test_D_only_affects_bottom_corners(self, solved_cube):
        """Test that D move only permutes corners 4, 5, 6, 7."""
        solved_cube.apply_move("D")
        # Top corners (0-3) should not move
        for i in range(4):
            assert solved_cube.corners[i] == Cube.SOLVED_CORNERS[i]
    
    def test_D_only_affects_bottom_edges(self, solved_cube):
        """Test that D move only permutes edges 4, 5, 6, 7."""
        solved_cube.apply_move("D")
        # Top edges (0-3) should not move
        for i in range(4):
            assert solved_cube.edges[i] == Cube.SOLVED_EDGES[i]
    
    def test_U_D_maintain_corner_orientation(self, solved_cube):
        """Test that U and D moves don't change corner orientation."""
        solved_cube.apply_move("U")
        for corner in solved_cube.corners:
            assert corner.orientation == 0
        
        solved_cube.reset()
        solved_cube.apply_move("D")
        for corner in solved_cube.corners:
            assert corner.orientation == 0
    
    def test_U_D_maintain_edge_orientation(self, solved_cube):
        """Test that U and D moves don't change edge orientation."""
        solved_cube.apply_move("U")
        for edge in solved_cube.edges:
            assert edge.orientation == 0
        
        solved_cube.reset()
        solved_cube.apply_move("D")
        for edge in solved_cube.edges:
            assert edge.orientation == 0
    
    def test_R_changes_corner_orientation(self, solved_cube):
        """Test that R move changes corner orientations."""
        solved_cube.apply_move("R")
        # Corners 0, 3, 4, 7 are affected
        affected_corners = [0, 3, 4, 7]
        orientation_changed = False
        for idx in affected_corners:
            if solved_cube.corners[idx].orientation != 0:
                orientation_changed = True
                break
        assert orientation_changed, "R move should change corner orientation"
    
    def test_R_maintains_edge_orientation(self, solved_cube):
        """Test that R move doesn't change edge orientation."""
        solved_cube.apply_move("R")
        for edge in solved_cube.edges:
            assert edge.orientation == 0
    
    def test_L_changes_corner_orientation(self, solved_cube):
        """Test that L move changes corner orientations."""
        solved_cube.apply_move("L")
        orientation_changed = False
        for corner in solved_cube.corners:
            if corner.orientation != 0:
                orientation_changed = True
                break
        assert orientation_changed, "L move should change corner orientation"
    
    def test_L_maintains_edge_orientation(self, solved_cube):
        """Test that L move doesn't change edge orientation."""
        solved_cube.apply_move("L")
        for edge in solved_cube.edges:
            assert edge.orientation == 0
    
    def test_F_changes_corner_orientation(self, solved_cube):
        """Test that F move changes corner orientations."""
        solved_cube.apply_move("F")
        orientation_changed = False
        for corner in solved_cube.corners:
            if corner.orientation != 0:
                orientation_changed = True
                break
        assert orientation_changed, "F move should change corner orientation"
    
    def test_F_changes_edge_orientation(self, solved_cube):
        """Test that F move changes edge orientations."""
        solved_cube.apply_move("F")
        orientation_changed = False
        for edge in solved_cube.edges:
            if edge.orientation != 0:
                orientation_changed = True
                break
        assert orientation_changed, "F move should change edge orientation"
    
    def test_B_changes_corner_orientation(self, solved_cube):
        """Test that B move changes corner orientations."""
        solved_cube.apply_move("B")
        orientation_changed = False
        for corner in solved_cube.corners:
            if corner.orientation != 0:
                orientation_changed = True
                break
        assert orientation_changed, "B move should change corner orientation"
    
    def test_B_changes_edge_orientation(self, solved_cube):
        """Test that B move changes edge orientations."""
        solved_cube.apply_move("B")
        orientation_changed = False
        for edge in solved_cube.edges:
            if edge.orientation != 0:
                orientation_changed = True
                break
        assert orientation_changed, "B move should change edge orientation"
    
    def test_move_and_inverse_returns_to_solved(self, solved_cube):
        """Test that move + inverse = solved for all moves."""
        moves = ["U", "D", "L", "R", "F", "B"]
        for move in moves:
            test_cube = Cube()
            test_cube.apply_move(move)
            test_cube.apply_move(move + "'")
            assert test_cube.is_solved(), f"{move} + {move}' should return to solved"
    
    def test_double_move_is_equivalent_to_two_moves(self, solved_cube):
        """Test that M2 is equivalent to M + M."""
        moves = ["U", "D", "L", "R", "F", "B"]
        for move in moves:
            cube1 = Cube()
            cube1.apply_move(move + "2")
            
            cube2 = Cube()
            cube2.apply_move(move)
            cube2.apply_move(move)
            
            assert get_all_corner_colors(cube1) == get_all_corner_colors(cube2)
            assert get_all_edge_colors(cube1) == get_all_edge_colors(cube2)


# ========== 3. Move Sequence Tests ==========

class TestMoveSequences:
    """Test sequences of moves and known algorithms."""
    
    def test_U_four_times_returns_to_solved(self, solved_cube):
        """Test that U^4 returns to solved state."""
        for _ in range(4):
            solved_cube.apply_move("U")
        assert solved_cube.is_solved()
    
    def test_D_four_times_returns_to_solved(self, solved_cube):
        """Test that D^4 returns to solved state."""
        for _ in range(4):
            solved_cube.apply_move("D")
        assert solved_cube.is_solved()
    
    def test_R_four_times_returns_to_solved(self, solved_cube):
        """Test that R^4 returns to solved state."""
        for _ in range(4):
            solved_cube.apply_move("R")
        assert solved_cube.is_solved()
    
    def test_L_four_times_returns_to_solved(self, solved_cube):
        """Test that L^4 returns to solved state."""
        for _ in range(4):
            solved_cube.apply_move("L")
        assert solved_cube.is_solved()
    
    def test_F_four_times_returns_to_solved(self, solved_cube):
        """Test that F^4 returns to solved state."""
        for _ in range(4):
            solved_cube.apply_move("F")
        assert solved_cube.is_solved()
    
    def test_B_four_times_returns_to_solved(self, solved_cube):
        """Test that B^4 returns to solved state."""
        for _ in range(4):
            solved_cube.apply_move("B")
        assert solved_cube.is_solved()
    
    def test_commutator_R_U_Rp_Up(self, solved_cube):
        """Test R U R' U' commutator cycles specific pieces."""
        solved_cube.apply_moves(["R", "U", "R'", "U'"])
        # After one commutator, the cube should not be solved
        assert not solved_cube.is_solved()
        # Apply the commutator 6 times to return to solved
        for _ in range(5):
            solved_cube.apply_moves(["R", "U", "R'", "U'"])
        assert solved_cube.is_solved()
    
    def test_T_perm_no_orientation_change(self, solved_cube):
        """Test T-perm (corner swapping algorithm) preserves validness."""
        # T-perm: R U R' U' R' F R2 U' R' U' R U R' F'
        t_perm = ["R", "U", "R'", "U'", "R'", "F", "R", "R", "U'", "R'", "U'", "R", "U", "R'", "F'"]
        solved_cube.apply_moves(t_perm)
        # Cube should still be valid (orientations preserved)
        assert corner_orientation_sum(solved_cube) == 0
        assert edge_orientation_sum(solved_cube) == 0
        assert not has_duplicate_pieces(solved_cube)


# ========== 4. Orientation Rule Tests ==========

class TestOrientationRules:
    """Test orientation constraints and invariants."""
    
    def test_corner_orientation_sum_always_zero_mod_3(self, solved_cube):
        """Test that sum of corner orientations is always 0 mod 3."""
        moves_to_test = [
            ["U"],
            ["R"],
            ["F"],
            ["U", "R", "F", "U'", "R'", "F'"],
            ["R", "U", "R'", "U'"],
        ]
        for moves in moves_to_test:
            test_cube = Cube()
            test_cube.apply_moves(moves)
            assert corner_orientation_sum(test_cube) == 0, f"Corner sum failed for {moves}"
    
    def test_edge_orientation_sum_always_zero_mod_2(self, solved_cube):
        """Test that sum of edge orientations is always 0 mod 2."""
        moves_to_test = [
            ["U"],
            ["F"],
            ["B"],
            ["U", "R", "F", "U'", "R'", "F'"],
            ["R", "U", "R'", "U'"],
        ]
        for moves in moves_to_test:
            test_cube = Cube()
            test_cube.apply_moves(moves)
            assert edge_orientation_sum(test_cube) == 0, f"Edge sum failed for {moves}"
    
    def test_orientation_only_changes_on_appropriate_moves(self, solved_cube):
        """Test that orientation only changes on moves that affect orientation."""
        # U/D should not change orientation
        solved_cube.apply_move("U")
        for corner in solved_cube.corners:
            assert corner.orientation == 0
        for edge in solved_cube.edges:
            assert edge.orientation == 0


# ========== 5. Piece Identity Tests ==========

class TestPieceIdentity:
    """Test that piece colors are preserved and no duplicates occur."""
    
    def test_corner_colors_preserved_after_move(self, solved_cube):
        """Test that corner colors don't change after moves."""
        original_colors = get_all_corner_colors(solved_cube)
        solved_cube.apply_moves(["R", "U", "F", "D"])
        final_colors = sorted(get_all_corner_colors(solved_cube))
        original_sorted = sorted(original_colors)
        assert final_colors == original_sorted
    
    def test_edge_colors_preserved_after_move(self, solved_cube):
        """Test that edge colors don't change after moves."""
        original_colors = get_all_edge_colors(solved_cube)
        solved_cube.apply_moves(["R", "U", "F", "D"])
        final_colors = sorted(get_all_edge_colors(solved_cube))
        original_sorted = sorted(original_colors)
        assert final_colors == original_sorted
    
    def test_no_duplicate_corners_after_moves(self, solved_cube):
        """Test that no corner pieces are duplicated after move sequences."""
        solved_cube.apply_moves(["R", "U", "R'", "U'", "F", "D", "F'", "D'"])
        corner_colors = get_all_corner_colors(solved_cube)
        assert len(set(corner_colors)) == 8, "Duplicate corners found"
    
    def test_no_duplicate_edges_after_moves(self, solved_cube):
        """Test that no edge pieces are duplicated after move sequences."""
        solved_cube.apply_moves(["R", "U", "R'", "U'", "F", "D", "F'", "D'"])
        edge_colors = get_all_edge_colors(solved_cube)
        assert len(set(edge_colors)) == 12, "Duplicate edges found"
    
    def test_no_duplicates_with_complex_sequence(self, solved_cube):
        """Test no duplicates after complex move sequence."""
        sequence = ["R", "U", "R'", "U'"] * 10
        solved_cube.apply_moves(sequence)
        assert not has_duplicate_pieces(solved_cube)


# ========== 6. Scramble Tests ==========

class TestScramble:
    """Test the scramble function and its properties."""
    
    def test_scramble_produces_unsolved_cube(self, solved_cube):
        """Test that scramble almost always produces an unsolved cube."""
        unsolved_count = 0
        for _ in range(10):
            cube = Cube()
            cube.scramble(20)
            if not cube.is_solved():
                unsolved_count += 1
        assert unsolved_count >= 9, "Scramble should almost always produce unsolved cube"
    
    def test_scramble_preserves_piece_colors(self, solved_cube):
        """Test that scramble preserves piece colors."""
        original_corners = sorted(get_all_corner_colors(solved_cube))
        solved_cube.scramble(20)
        final_corners = sorted(get_all_corner_colors(solved_cube))
        assert original_corners == final_corners
    
    def test_scramble_preserves_corner_orientation_parity(self, solved_cube):
        """Test that corner orientation sum is 0 mod 3 after scramble."""
        solved_cube.scramble(20)
        assert corner_orientation_sum(solved_cube) == 0
    
    def test_scramble_preserves_edge_orientation_parity(self, solved_cube):
        """Test that edge orientation sum is 0 mod 2 after scramble."""
        solved_cube.scramble(20)
        assert edge_orientation_sum(solved_cube) == 0
    
    def test_scramble_no_duplicate_pieces(self, solved_cube):
        """Test that scramble doesn't create duplicate pieces."""
        solved_cube.scramble(20)
        assert not has_duplicate_pieces(solved_cube)
    
    def test_scramble_returns_move_list(self, solved_cube):
        """Test that scramble returns the list of applied moves."""
        moves = solved_cube.scramble(5)
        assert isinstance(moves, list)
        assert len(moves) == 5
        for move in moves:
            assert isinstance(move, str)


# ========== 7. Round-Trip Tests ==========

class TestRoundTrip:
    """Test applying sequences and their inverses."""
    
    def test_random_sequence_plus_inverse_returns_solved(self, solved_cube):
        """Test that sequence + inverse returns to solved."""
        sequence = ["R", "U", "F", "D", "L", "B", "U'", "R'"]
        solved_cube.apply_moves(sequence)
        assert not solved_cube.is_solved()
        
        inverse = reverse_move_sequence(sequence)
        solved_cube.apply_moves(inverse)
        assert solved_cube.is_solved()
    
    def test_multiple_round_trips(self, solved_cube):
        """Test multiple sequences and their inverses."""
        sequences = [
            ["R"],
            ["R", "U"],
            ["R", "U", "R'", "U'"],
            ["F", "R", "U"],
        ]
        for sequence in sequences:
            cube = Cube()
            cube.apply_moves(sequence)
            inverse = reverse_move_sequence(sequence)
            cube.apply_moves(inverse)
            assert cube.is_solved(), f"Failed for sequence {sequence}"
    
    def test_double_move_inverse(self, solved_cube):
        """Test that double moves work correctly with inverses."""
        solved_cube.apply_move("R2")
        assert not solved_cube.is_solved()
        solved_cube.apply_move("R2")
        assert solved_cube.is_solved()
    
    def test_complex_sequence_round_trip(self, solved_cube):
        """Test complex sequence and inverse."""
        sequence = ["R", "U", "R'", "U'"] * 3
        solved_cube.apply_moves(sequence)
        assert not solved_cube.is_solved()
        
        inverse = reverse_move_sequence(sequence)
        solved_cube.apply_moves(inverse)
        assert solved_cube.is_solved()


# ========== 8. Reset and State Management ==========

class TestResetAndState:
    """Test reset and state management."""
    
    def test_reset_returns_to_solved(self, cube_with_scramble):
        """Test that reset returns the cube to solved state."""
        assert not cube_with_scramble.is_solved()
        cube_with_scramble.reset()
        assert cube_with_scramble.is_solved()
    
    def test_reset_restores_all_pieces(self, cube_with_scramble):
        """Test that reset restores all piece positions and orientations."""
        cube_with_scramble.reset()
        for i in range(8):
            assert cube_with_scramble.corners[i] == Cube.SOLVED_CORNERS[i]
        for i in range(12):
            assert cube_with_scramble.edges[i] == Cube.SOLVED_EDGES[i]


# ========== 9. Move Notation Tests ==========

class TestMoveNotation:
    """Test move notation parsing and application."""
    
    def test_prime_notation(self, solved_cube):
        """Test that move' applies the inverse."""
        cube1 = Cube()
        cube1.apply_move("U")
        cube1.apply_move("U'")
        assert cube1.is_solved()
    
    def test_double_move_notation(self, solved_cube):
        """Test that move2 applies the move twice."""
        cube1 = Cube()
        cube1.apply_move("R2")
        
        cube2 = Cube()
        cube2.apply_move("R")
        cube2.apply_move("R")
        
        assert get_all_corner_colors(cube1) == get_all_corner_colors(cube2)
        assert get_all_edge_colors(cube1) == get_all_edge_colors(cube2)
    
    def test_all_faces_with_notation(self, solved_cube):
        """Test move notation for all faces."""
        faces = ['U', 'D', 'L', 'R', 'F', 'B']
        notations = ['', "'", '2']
        
        for face in faces:
            for notation in notations:
                cube = Cube()
                move = face + notation
                cube.apply_move(move)
                # Just verify it doesn't crash
                assert len(cube.corners) == 8
                assert len(cube.edges) == 12
    
    def test_invalid_move_raises_error(self, solved_cube):
        """Test that invalid moves raise ValueError."""
        with pytest.raises(ValueError):
            solved_cube.apply_move("X")
        
        with pytest.raises(ValueError):
            solved_cube.apply_move("")


# ========== 10. Convenience Tests ==========

class TestConvenience:
    """Test convenience methods."""
    
    def test_get_corner_position(self, solved_cube):
        """Test get_corner_position method."""
        corner = solved_cube.get_corner_position(0)
        assert corner.colors == ('W', 'R', 'G')
        assert corner.orientation == 0
    
    def test_get_edge_position(self, solved_cube):
        """Test get_edge_position method."""
        edge = solved_cube.get_edge_position(0)
        assert edge.colors == ('W', 'R')
        assert edge.orientation == 0
    
    def test_apply_moves_list(self, solved_cube):
        """Test apply_moves with a list of moves."""
        moves = ["U", "R", "F"]
        solved_cube.apply_moves(moves)
        assert not solved_cube.is_solved()
    
    def test_repr_shows_solved_status(self, solved_cube):
        """Test that __repr__ includes solved status."""
        repr_str = repr(solved_cube)
        assert "solved=True" in repr_str
        
        solved_cube.apply_move("R")
        repr_str = repr(solved_cube)
        assert "solved=False" in repr_str
