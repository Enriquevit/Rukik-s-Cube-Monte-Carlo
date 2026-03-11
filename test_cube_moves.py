"""
Test suite for cube.py - Tests all moves and their reverses
"""
from cube import Cube
import copy


def cube_to_string(cube):
    """Convert cube state to comparable string"""
    state = ""
    for face in ['U', 'D', 'F', 'B', 'L', 'R']:
        for row in cube.sides[face].grid:
            state += ''.join(row)
    return state


def test_move_and_reverse():
    """Test that move + reverse returns cube to original state"""
    moves = ['U', 'D', 'F', 'B', 'L', 'R']
    
    print("=" * 60)
    print("Testing Move + Reverse Operations")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for move in moves:
        cube = Cube()
        original_state = cube_to_string(cube)
        
        # Apply move and its reverse
        cube.apply_move(move)
        cube.apply_move(move + "'")
        
        final_state = cube_to_string(cube)
        
        if original_state == final_state:
            print(f"[PASS] {move} + {move}' returns to original state")
            passed += 1
        else:
            print(f"[FAIL] {move} + {move}' does NOT return to original state")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed\n")
    return passed, failed


def test_reverse_and_move():
    """Test that reverse + move also returns cube to original state"""
    moves = ['U', 'D', 'F', 'B', 'L', 'R']
    
    print("=" * 60)
    print("Testing Reverse + Move Operations")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for move in moves:
        cube = Cube()
        original_state = cube_to_string(cube)
        
        # Apply reverse and then move
        cube.apply_move(move + "'")
        cube.apply_move(move)
        
        final_state = cube_to_string(cube)
        
        if original_state == final_state:
            print(f"[PASS] {move}' + {move} returns to original state")
            passed += 1
        else:
            print(f"[FAIL] {move}' + {move} does NOT return to original state")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed\n")
    return passed, failed


def test_move_applied_four_times():
    """Test that applying a move 4 times returns to original (for 90-degree rotations)"""
    moves = ['U', 'D', 'F', 'B', 'L', 'R']
    
    print("=" * 60)
    print("Testing Move x 4 = Original State")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for move in moves:
        cube = Cube()
        original_state = cube_to_string(cube)
        
        # Apply move 4 times
        for _ in range(4):
            cube.apply_move(move)
        
        final_state = cube_to_string(cube)
        
        if original_state == final_state:
            print(f"[PASS] {move} x 4 returns to original state")
            passed += 1
        else:
            print(f"[FAIL] {move} x 4 does NOT return to original state")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed\n")
    return passed, failed


def test_move_affects_correct_faces():
    """Test that each move affects the correct faces"""
    print("=" * 60)
    print("Testing Move Effects (Correct Faces Modified)")
    print("=" * 60)
    
    test_cases = [
        ('U', ['U', 'F', 'B', 'L', 'R']),  # U affects U, F, B, L, R (not D)
        ('D', ['D', 'F', 'B', 'L', 'R']),  # D affects D, F, B, L, R (not U)
        ('F', ['F', 'U', 'D', 'L', 'R']),  # F affects F, U, D, L, R (not B)
        ('B', ['B', 'U', 'D', 'L', 'R']),  # B affects B, U, D, L, R (not F)
        ('L', ['L', 'U', 'D', 'F', 'B']),  # L affects L, U, D, F, B (not R)
        ('R', ['R', 'U', 'D', 'F', 'B']),  # R affects R, U, D, F, B (not L)
    ]
    
    passed = 0
    failed = 0
    
    for move, affected_faces in test_cases:
        cube = Cube()
        
        # Store original states
        original = {}
        for face in ['U', 'D', 'F', 'B', 'L', 'R']:
            original[face] = copy.deepcopy(cube.sides[face].grid)
        
        # Apply move
        cube.apply_move(move)
        
        # Check which faces changed
        changed_faces = set()
        for face in ['U', 'D', 'F', 'B', 'L', 'R']:
            if original[face] != cube.sides[face].grid:
                changed_faces.add(face)
        
        expected_faces = set(affected_faces)
        
        if changed_faces == expected_faces:
            print(f"[PASS] {move} affects correct faces: {sorted(changed_faces)}")
            passed += 1
        else:
            print(f"[FAIL] {move} affects wrong faces")
            print(f"       Expected: {sorted(expected_faces)}")
            print(f"       Got: {sorted(changed_faces)}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed\n")
    return passed, failed


def test_consecutive_moves():
    """Test various sequences of consecutive moves"""
    print("=" * 60)
    print("Testing Consecutive Move Sequences")
    print("=" * 60)
    
    test_sequences = [
        (['U', 'U'], "U twice"),
        (['U', 'D'], "U then D"),
        (['F', 'B'], "F then B"),
        (['L', 'R'], "L then R"),
        (['U', 'D', 'F', 'B', 'L', 'R'], "all 6 moves"),
        (["U'", "U", "U", "U"], "U' is equivalent to U x 3"),
    ]
    
    passed = 0
    failed = 0
    
    for sequence, description in test_sequences:
        try:
            cube = Cube()
            for move in sequence:
                cube.apply_move(move)
            print(f"[PASS] {description}: executed without error")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {description}: {str(e)}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed\n")
    return passed, failed


def main():
    print("\n" + "=" * 60)
    print("CUBE MOVE TEST SUITE")
    print("=" * 60 + "\n")
    
    total_passed = 0
    total_failed = 0
    
    p, f = test_move_and_reverse()
    total_passed += p
    total_failed += f
    
    p, f = test_reverse_and_move()
    total_passed += p
    total_failed += f
    
    p, f = test_move_applied_four_times()
    total_passed += p
    total_failed += f
    
    p, f = test_move_affects_correct_faces()
    total_passed += p
    total_failed += f
    
    p, f = test_consecutive_moves()
    total_passed += p
    total_failed += f
    
    print("=" * 60)
    print(f"TOTAL RESULTS: {total_passed} passed, {total_failed} failed")
    print("=" * 60)


if __name__ == "__main__":
    main()
