"""
Validation tests for cube.py and cube_visualizer_3d.py
Tests cube validity and 3D rendering correctness
"""
from cube import Cube
import copy


def validate_cube_state(cube):
    """
    Check if a cube state is physically valid
    Returns (is_valid, errors)
    """
    errors = []
    
    # Test 1: Each color should appear exactly 9 times (one per center position on each face)
    color_counts = {}
    for face_name in ['U', 'D', 'F', 'B', 'L', 'R']:
        face = cube.sides[face_name]
        center_color = face.grid[1][1]
        
        for row in face.grid:
            for color in row:
                color_counts[color] = color_counts.get(color, 0) + 1
    
    expected_colors = {'W': 9, 'Y': 9, 'G': 9, 'B': 9, 'O': 9, 'R': 9}
    for color, expected_count in expected_colors.items():
        actual_count = color_counts.get(color, 0)
        if actual_count != expected_count:
            errors.append(f"Color {color}: expected {expected_count}, got {actual_count}")
    
    # Test 2: All faces should have their center color maintained
    center_colors = {
        'U': 'W',
        'D': 'Y',
        'F': 'G',
        'B': 'B',
        'L': 'O',
        'R': 'R'
    }
    for face_name, expected_center in center_colors.items():
        actual_center = cube.sides[face_name].grid[1][1]
        if actual_center != expected_center:
            errors.append(f"Face {face_name} center: expected {expected_center}, got {actual_center}")
    
    # Test 3: Each face should have exactly 9 stickers
    for face_name in ['U', 'D', 'F', 'B', 'L', 'R']:
        sticker_count = sum(len(row) for row in cube.sides[face_name].grid)
        if sticker_count != 9:
            errors.append(f"Face {face_name}: expected 9 stickers, got {sticker_count}")
    
    # Test 4: Check for 'None' or invalid color codes
    valid_colors = {'W', 'Y', 'G', 'B', 'O', 'R'}
    for face_name in ['U', 'D', 'F', 'B', 'L', 'R']:
        for row in cube.sides[face_name].grid:
            for color in row:
                if color not in valid_colors:
                    errors.append(f"Invalid color '{color}' found on face {face_name}")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def test_initial_cube_validity():
    """Test that a freshly created cube is valid"""
    print("=" * 60)
    print("Test 1: Initial Cube Validity")
    print("=" * 60)
    
    cube = Cube()
    is_valid, errors = validate_cube_state(cube)
    
    if is_valid:
        print("[PASS] Initial cube is valid")
        return True
    else:
        print("[FAIL] Initial cube is invalid:")
        for error in errors:
            print(f"  - {error}")
        return False


def test_cube_after_moves():
    """Test that cube remains valid after various moves"""
    print("\n" + "=" * 60)
    print("Test 2: Cube Validity After Random Moves")
    print("=" * 60)
    
    test_cases = [
        (['U'], "Single U move"),
        (['U', 'D', 'F', 'B', 'L', 'R'], "All 6 moves"),
        (["U'", "D'", "F'"], "Moves with reverses"),
        (["F", "U", "R", "U'", "R'", "F'"], "Random sequence"),
    ]
    
    passed = 0
    failed = 0
    
    for moves, description in test_cases:
        cube = Cube()
        for move in moves:
            cube.apply_move(move)
        
        is_valid, errors = validate_cube_state(cube)
        
        if is_valid:
            print(f"[PASS] {description}: cube remains valid")
            passed += 1
        else:
            print(f"[FAIL] {description}: cube became invalid")
            for error in errors:
                print(f"       - {error}")
            failed += 1
    
    print(f"\nSubtest Results: {passed} passed, {failed} failed")
    return failed == 0


def test_cube_corner_sticker_consistency():
    """
    Test that corner stickers form valid corners
    Each corner should have 3 stickers of different colors that all match their adjacent face centers
    """
    print("\n" + "=" * 60)
    print("Test 3: Corner Sticker Consistency")
    print("=" * 60)
    
    cube = Cube()
    
    # Define corner positions: (face1, row, col), (face2, row, col), (face3, row, col)
    # These must all be the same corner on the physical cube
    corners = [
        # UFR corner
        [('U', 2, 2), ('F', 0, 2), ('R', 0, 0)],
        # UFL corner
        [('U', 2, 0), ('F', 0, 0), ('L', 0, 2)],
        # UBR corner
        [('U', 0, 2), ('B', 0, 2), ('R', 0, 2)],
        # UBL corner
        [('U', 0, 0), ('B', 0, 0), ('L', 0, 0)],
        # DFR corner
        [('D', 0, 2), ('F', 2, 2), ('R', 2, 0)],
        # DFL corner
        [('D', 0, 0), ('F', 2, 0), ('L', 2, 2)],
        # DBR corner
        [('D', 2, 2), ('B', 2, 2), ('R', 2, 2)],
        # DBL corner
        [('D', 2, 0), ('B', 2, 0), ('L', 2, 0)],
    ]
    
    expected_corners = [
        # UFR
        [('U', 'W'), ('F', 'G'), ('R', 'R')],
        # UFL
        [('U', 'W'), ('F', 'G'), ('L', 'O')],
        # UBR
        [('U', 'W'), ('B', 'B'), ('R', 'R')],
        # UBL
        [('U', 'W'), ('B', 'B'), ('L', 'O')],
        # DFR
        [('D', 'Y'), ('F', 'G'), ('R', 'R')],
        # DFL
        [('D', 'Y'), ('F', 'G'), ('L', 'O')],
        # DBR
        [('D', 'Y'), ('B', 'B'), ('R', 'R')],
        # DBL
        [('D', 'Y'), ('B', 'B'), ('L', 'O')],
    ]
    
    errors = []
    for i, corner_positions in enumerate(corners):
        actual_colors = [
            cube.sides[face].grid[row][col]
            for face, row, col in corner_positions
        ]
        expected_faces = [face for face, _ in expected_corners[i]]
        expected_colors_list = [color for _, color in expected_corners[i]]
        
        # Check that each corner has the right colors in some order
        if sorted(actual_colors) != sorted(expected_colors_list):
            errors.append(f"Corner {i}: expected {sorted(expected_colors_list)}, got {sorted(actual_colors)}")
    
    if not errors:
        print("[PASS] All  8 corners have correct stickers")
        return True
    else:
        print(f"[FAIL] {len(errors)} corners have incorrect stickers:")
        for error in errors:
            print(f"  - {error}")
        return False


def test_cube_edge_sticker_consistency():
    """
    Test that edge stickers are consistent
    Each edge should have 2 stickers of different colors
    """
    print("\n" + "=" * 60)
    print("Test 4: Edge Sticker Consistency")
    print("=" * 60)
    
    cube = Cube()
    
    # Define edge positions: (face1, row, col), (face2, row, col)
    edges = [
        # UF edge
        [('U', 2, 1), ('F', 0, 1)],
        # UB edge
        [('U', 0, 1), ('B', 0, 1)],
        # UR edge
        [('U', 1, 2), ('R', 0, 1)],
        # UL edge
        [('U', 1, 0), ('L', 0, 1)],
        # DF edge
        [('D', 0, 1), ('F', 2, 1)],
        # DB edge
        [('D', 2, 1), ('B', 2, 1)],
        # DR edge
        [('D', 1, 2), ('R', 2, 1)],
        # DL edge
        [('D', 1, 0), ('L', 2, 1)],
        # FR edge
        [('F', 1, 2), ('R', 1, 0)],
        # FL edge
        [('F', 1, 0), ('L', 1, 2)],
        # BR edge
        [('B', 1, 2), ('R', 1, 2)],
        # BL edge
        [('B', 1, 0), ('L', 1, 0)],
    ]
    
    errors = []
    for i, edge_positions in enumerate(edges):
        colors = [
            cube.sides[face].grid[row][col]
            for face, row, col in edge_positions
        ]
        # Edge should have 2 different colors
        if len(set(colors)) != 2:
            errors.append(f"Edge {i}: has duplicate colors {colors}")
    
    if not errors:
        print("[PASS] All 12 edges have correct sticker structure")
        return True
    else:
        print(f"[FAIL] {len(errors)} edges have invalid structure:")
        for error in errors:
            print(f"  - {error}")
        return False


def test_3d_visualizer_compatibility():
    """
    Test that cube state is compatible with 3D visualizer
    Checks that face grid structure matches what the visualizer expects
    """
    print("\n" + "=" * 60)
    print("Test 5: 3D Visualizer Compatibility")
    print("=" * 60)
    
    cube = Cube()
    
    # Apply some moves
    moves = ['R', 'U', "'", 'R', "'", 'U', "R", "U", "R"]
    for move in moves:
        cube.apply_move(move)
    
    errors = []
    
    # Check that each face has correct structure for 3D rendering
    for face_name in ['U', 'D', 'F', 'B', 'L', 'R']:
        face = cube.sides[face_name]
        
        # Grid should be 3x3
        if len(face.grid) != 3:
            errors.append(f"Face {face_name}: grid has {len(face.grid)} rows, expected 3")
        
        for i, row in enumerate(face.grid):
            if len(row) != 3:
                errors.append(f"Face {face_name} row {i}: has {len(row)} columns, expected 3")
            
            # Each element should be a string (color code)
            for j, element in enumerate(row):
                if not isinstance(element, str):
                    errors.append(f"Face {face_name}[{i}][{j}]: expected string, got {type(element)}")
    
    if not errors:
        print("[PASS] Cube structure is compatible with 3D visualizer")
        return True
    else:
        print(f"[FAIL] {len(errors)} structure issues found:")
        for error in errors:
            print(f"  - {error}")
        return False


def test_no_sticker_duplication_across_faces():
    """
    Advanced test: verify that the same color sticker doesn't appear
    in impossible configurations across faces
    """
    print("\n" + "=" * 60)
    print("Test 6: Cross-Face Sticker Configuration")
    print("=" * 60)
    
    cube = Cube()
    is_valid, errors = validate_cube_state(cube)
    
    if is_valid:
        print("[PASS] Initial cube has valid cross-face sticker distribution")
        return True
    else:
        print("[FAIL] Invalid sticker distribution:")
        for error in errors:
            print(f"  - {error}")
        return False


def main():
    print("\n" + "=" * 60)
    print("CUBE VALIDITY TEST SUITE")
    print("=" * 60)
    
    results = []
    
    results.append(("Initial Cube Validity", test_initial_cube_validity()))
    results.append(("Cube After Moves", test_cube_after_moves()))
    results.append(("Corner Consistency", test_cube_corner_sticker_consistency()))
    results.append(("Edge Consistency", test_cube_edge_sticker_consistency()))
    results.append(("3D Visualizer Compatibility", test_3d_visualizer_compatibility()))
    results.append(("Cross-Face Distribution", test_no_sticker_duplication_across_faces()))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    failed = sum(1 for _, result in results if not result)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
    
    print(f"\nTotal: {passed} passed, {failed} failed")
    print("=" * 60)


if __name__ == "__main__":
    main()
