"""
test_cross_solver.py

Test suite for the CrossSolver class.
Tests include:
- is_cross_complete() for solved and unsolved cubes
- recognize_cross_edges() for edge detection
- solve_cross_beginner() and solve_cross_intermediate() solvers
"""

from cube import Cube
from cross_solver import CrossSolver


def test_solved_cube():
    """Test that a solved cube is recognized as having a complete cross."""
    print("\n=== Test 1: Solved Cube ===")
    cube = Cube()  # Create a solved cube
    solver = CrossSolver()
    
    result = solver.is_cross_complete(cube)
    print(f"Solved cube has complete cross: {result}")
    assert result is True, "Solved cube should have complete cross"
    print("[PASS] Test passed")


def test_unsolved_cube():
    """Test that a scrambled cube is not recognized as having a complete cross."""
    print("\n=== Test 2: Scrambled Cube (No Complete Cross) ===")
    cube = Cube()
    # Apply some moves to scramble
    cube.apply_move('F')
    cube.apply_move('R')
    cube.apply_move('U')
    
    solver = CrossSolver()
    result = solver.is_cross_complete(cube)
    print(f"Scrambled cube has complete cross: {result}")
    assert result is False, "Scrambled cube should not have complete cross"
    print("[PASS] Test passed")


def test_partially_solved_cube():
    """Test a cube with only some edges on the white cross."""
    print("\n=== Test 3: Partially Solved Cube ===")
    cube = Cube()
    # Apply a move that disrupts only some edges
    cube.apply_move('R')
    
    solver = CrossSolver()
    result = solver.is_cross_complete(cube)
    print(f"Partially solved cube has complete cross: {result}")
    assert result is False, "Partially solved cube should not have complete cross"
    print("[PASS] Test passed")


def test_cross_edges_solved_cube():
    """Test edge recognition on a solved cube."""
    print("\n=== Test 4: Edge Recognition - Solved Cube ===")
    cube = Cube()
    solver = CrossSolver()
    
    edges = solver.recognize_cross_edges(cube)
    print("Edge status for solved cube:")
    for face, info in edges.items():
        print(f"  {face}: correct={info['correct']}")
    
    # All edges should be correct on a solved cube
    for face in ['F', 'L', 'R', 'B']:
        assert edges[face]['correct'] is True, f"{face} edge should be correct on solved cube"
    print("[PASS] Test passed - all edges are correct")


def test_cross_edges_scrambled_cube():
    """Test edge recognition on a scrambled cube."""
    print("\n=== Test 5: Edge Recognition - Scrambled Cube ===")
    cube = Cube()
    cube.apply_move('F')
    cube.apply_move('U')
    cube.apply_move('R')
    
    solver = CrossSolver()
    edges = solver.recognize_cross_edges(cube)
    print("Edge status for scrambled cube:")
    for face, info in edges.items():
        print(f"  {face}: correct={info['correct']}")
    
    # At least one edge should be incorrect after scrambling
    correct_count = sum(1 for info in edges.values() if info['correct'])
    print(f"Number of correct edges: {correct_count}/4")
    assert correct_count < 4, "Scrambled cube should have some incorrect edges"
    print("[PASS] Test passed - edges correctly identified as incorrect")


def test_beginner_solver():
    """Test the beginner cross solver."""
    print("\n=== Test 6: Beginner Cross Solver ===")
    cube = Cube()
    
    # Apply a simple scramble
    scramble = ['F', 'U', 'R']
    for move in scramble:
        cube.apply_move(move)
    
    print(f"Applied scramble: {scramble}")
    print(f"Cross complete before solving: {CrossSolver().is_cross_complete(cube)}")
    
    solver = CrossSolver()
    moves, solved_cube = solver.solve_cross_beginner(cube)
    
    print(f"Moves used by beginner solver: {moves}")
    print(f"Cross complete after solving: {solver.is_cross_complete(solved_cube)}")
    
    assert solver.is_cross_complete(solved_cube), "Beginner solver should complete the cross"
    print(f"[PASS] Test passed - cross solved in {len(moves)} moves")


def test_beginner_solver_already_solved():
    """Test beginner solver on an already solved cube."""
    print("\n=== Test 7: Beginner Solver - Already Solved Cube ===")
    cube = Cube()
    
    solver = CrossSolver()
    moves, solved_cube = solver.solve_cross_beginner(cube)
    
    print(f"Moves used: {moves}")
    print(f"Cross still complete: {solver.is_cross_complete(solved_cube)}")
    
    assert solver.is_cross_complete(solved_cube), "Should remain solved"
    print("[PASS] Test passed")


def test_intermediate_solver():
    """Test the intermediate cross solver."""
    print("\n=== Test 8: Intermediate Cross Solver ===")
    cube = Cube()
    
    # Apply a simple scramble
    scramble = ['F', 'U', 'R', 'L']
    for move in scramble:
        cube.apply_move(move)
    
    print(f"Applied scramble: {scramble}")
    print(f"Cross complete before solving: {CrossSolver().is_cross_complete(cube)}")
    
    solver = CrossSolver()
    moves, solved_cube = solver.solve_cross_intermediate(cube)
    
    print(f"Moves used by intermediate solver: {moves}")
    print(f"Cross complete after solving: {solver.is_cross_complete(solved_cube)}")
    
    assert solver.is_cross_complete(solved_cube), "Intermediate solver should complete the cross"
    print(f"[PASS] Test passed - cross solved in {len(moves)} moves")


def test_intermediate_solver_already_solved():
    """Test intermediate solver on an already solved cube."""
    print("\n=== Test 9: Intermediate Solver - Already Solved Cube ===")
    cube = Cube()
    
    solver = CrossSolver()
    moves, solved_cube = solver.solve_cross_intermediate(cube)
    
    print(f"Moves used: {moves}")
    print(f"Cross still complete: {solver.is_cross_complete(solved_cube)}")
    
    assert solver.is_cross_complete(solved_cube), "Should remain solved"
    print("[PASS] Test passed")


def test_solver_method_dispatch():
    """Test that the solve_cross method correctly dispatches to different skill levels."""
    print("\n=== Test 10: Solver Method Dispatch ===")
    cube = Cube()
    cube.apply_move('F')
    cube.apply_move('U')
    
    solver = CrossSolver()
    
    # Test beginner dispatch
    moves_b, cube_b = solver.solve_cross(cube, skill='beginner')
    print(f"Beginner moves: {len(moves_b)}, Cross complete: {solver.is_cross_complete(cube_b)}")
    assert solver.is_cross_complete(cube_b), "Beginner should solve"
    
    # Test intermediate dispatch
    cube2 = Cube()
    cube2.apply_move('F')
    cube2.apply_move('U')
    moves_i, cube_i = solver.solve_cross(cube2, skill='intermediate')
    print(f"Intermediate moves: {len(moves_i)}, Cross complete: {solver.is_cross_complete(cube_i)}")
    assert solver.is_cross_complete(cube_i), "Intermediate should solve"
    
    print("[PASS] Test passed - method dispatch working")


def test_larger_scramble():
    """Test solvers with a larger scramble."""
    print("\n=== Test 11: Larger Scramble Test ===")
    cube = Cube()
    
    # Apply a larger scramble
    scramble = ['F', 'U', 'R', 'B', 'L', 'D', 'F', 'U']
    for move in scramble:
        cube.apply_move(move)
    
    print(f"Applied scramble: {scramble}")
    print(f"Cross complete before solving: {CrossSolver().is_cross_complete(cube)}")
    
    solver = CrossSolver()
    moves, solved_cube = solver.solve_cross_intermediate(cube)
    
    print(f"Moves used: {moves}")
    print(f"Cross complete after solving: {solver.is_cross_complete(solved_cube)}")
    
    assert solver.is_cross_complete(solved_cube), "Should solve cross regardless"
    print(f"[PASS] Test passed - cross solved in {len(moves)} moves")


def test_edge_recognition_details():
    """Test edge recognition with detailed output."""
    print("\n=== Test 12: Edge Recognition Details ===")
    cube = Cube()
    cube.apply_move('F')
    
    solver = CrossSolver()
    edges = solver.recognize_cross_edges(cube)
    
    print("Detailed edge information:")
    for face, info in edges.items():
        print(f"  {face}:")
        print(f"    Positions: {info['positions']}")
        print(f"    On U face: {info['on_U']}")
        print(f"    Correct: {info['correct']}")
    
    print("[PASS] Test passed - edge details available")


def run_all_tests():
    """Run all test cases."""
    print("=" * 60)
    print("Running Cross Solver Test Suite")
    print("=" * 60)
    
    tests = [
        test_solved_cube,
        test_unsolved_cube,
        test_partially_solved_cube,
        test_cross_edges_solved_cube,
        test_cross_edges_scrambled_cube,
        test_beginner_solver,
        test_beginner_solver_already_solved,
        test_intermediate_solver,
        test_intermediate_solver_already_solved,
        test_solver_method_dispatch,
        test_larger_scramble,
        test_edge_recognition_details,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] Test error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()
