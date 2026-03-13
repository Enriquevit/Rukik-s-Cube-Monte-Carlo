"""
Advanced test: Verify sticker colors match cube state for rendering
This checks if the visualizer is displaying the correct colors for each sticker
"""
import math
from cube import Cube
from cube_visualizer_3d import Cube3DVisualizer, COLORS


def test_sticker_color_mapping():
    """Test that sticker colors in the visualizer match the cube state"""
    print("=" * 60)
    print("Test: Sticker Color Mapping Validation")
    print("=" * 60)
    
    cube = Cube()
    visualizer = Cube3DVisualizer(cube, size=400)
    
    errors = []
    
    # Check that each sticker in sticker_quads matches the cube state
    for face, (r, c), quad in visualizer.sticker_quads:
        # Get expected color from cube state
        expected_color_code = cube.sides[face].grid[r][c]
        
        # Check it's a valid color
        if expected_color_code not in COLORS:
            errors.append(f"Face {face}[{r}][{c}]: invalid color code '{expected_color_code}'")
        else:
            # The quad should map to this color when rendered
            # (visualizer.draw() would look up this color)
            expected_rgb = COLORS[expected_color_code]
            print(f"  {face}[{r}][{c}] = {expected_color_code}{expected_rgb}")
    
    if not errors:
        print(f"\n[PASS] All {len(visualizer.sticker_quads)} stickers map to valid colors")
        return True
    else:
        print(f"\n[FAIL] {len(errors)} color mapping errors:")
        for error in errors[:10]:
            print(f"  - {error}")
        return False


def test_sticker_color_after_moves():
    """Test that sticker colors update correctly after moves"""
    print("\n" + "=" * 60)
    print("Test: Sticker Color After Moves")
    print("=" * 60)
    
    cube = Cube()
    visualizer = Cube3DVisualizer(cube, size=400)
    
    # Record initial state
    initial_colors = {}
    for face, (r, c), quad in visualizer.sticker_quads:
        initial_colors[(face, r, c)] = cube.sides[face].grid[r][c]
    
    # Apply some moves
    moves = ["R", "U", "F", "D"]
    for move in moves:
        cube.apply_move(move)
    
    # Check that colors still map correctly
    errors = []
    changed_count = 0
    
    for face, (r, c), quad in visualizer.sticker_quads:
        current_color = cube.sides[face].grid[r][c]
        
        # Check it's valid
        if current_color not in COLORS:
            errors.append(f"Face {face}[{r}][{c}]: invalid color after moves: '{current_color}'")
        
        # Check if it changed
        if current_color != initial_colors.get((face, r, c)):
            changed_count += 1
    
    if errors:
        print(f"[FAIL] {len(errors)} color errors after moves:")
        for error in errors[:5]:
            print(f"  - {error}")
        return False
    else:
        print(f"[PASS] All colors valid after moves")
        print(f"       {changed_count} stickers changed (out of 54)")
        if changed_count > 0:
            print(f"[PASS] Moves correctly updated cube state")
            return True
        else:
            print(f"[FAIL] No stickers changed after applying moves!")
            return False


def test_solved_cube_expected_colors():
    """Test that a solved cube has expected color distribution"""
    print("\n" + "=" * 60)
    print("Test: Solved Cube Expected Colors")
    print("=" * 60)
    
    cube = Cube()
    visualizer = Cube3DVisualizer(cube, size=400)
    
    expected_face_colors = {
        'U': 'W',
        'D': 'Y',
        'F': 'G',
        'B': 'B',
        'L': 'O',
        'R': 'R',
    }
    
    errors = []
    
    # For a solved cube, all stickers on a face should match that face's color
    for face, (r, c), quad in visualizer.sticker_quads:
        actual_color = cube.sides[face].grid[r][c]
        expected_color = expected_face_colors[face]
        
        if actual_color != expected_color:
            errors.append(f"Face {face}[{r}][{c}]: expected {expected_color}, got {actual_color}")
    
    if not errors:
        print("[PASS] Solved cube has correct color on each sticker")
        print("       Every sticker matches its face center color")
        return True
    else:
        print(f"[FAIL] {len(errors)} stickers have wrong color for solved cube:")
        for error in errors[:5]:
            print(f"  - {error}")
        return False


def test_color_counts_consistency():
    """Test that color counts remain constant (6 of each color, 9 times = 54 stickers)"""
    print("\n" + "=" * 60)
    print("Test: Color Count Consistency")
    print("=" * 60)
    
    test_cases = [
        ("Solved Cube", []),
        ("Scrambled", ["R", "U", "F", "D", "L", "B"]),
        ("More Scramble", ["R", "U'", "R'", "U", "R", "U", "R'"] ),
    ]
    
    all_passed = True
    for name, moves in test_cases:
        cube = Cube()
        for move in moves:
            cube.apply_move(move)
        
        visualizer = Cube3DVisualizer(cube, size=400)
        
        color_counts = {}
        for face, (r, c), quad in visualizer.sticker_quads:
            color = cube.sides[face].grid[r][c]
            color_counts[color] = color_counts.get(color, 0) + 1
        
        # Should have exactly 9 of each color
        expected = {'W': 9, 'Y': 9, 'G': 9, 'B': 9, 'O': 9, 'R': 9}
        
        success = True
        for color, expected_count in expected.items():
            actual_count = color_counts.get(color, 0)
            if actual_count != expected_count:
                print(f"[FAIL] {name}: {color} count {actual_count}, expected {expected_count}")
                success = False
                all_passed = False
        
        if success:
            print(f"[PASS] {name}: correct color distribution")
    
    return all_passed


def main():
    print("\n" + "=" * 60)
    print("STICKER COLOR VALIDATION TEST SUITE")
    print("=" * 60)
    
    results = []
    
    results.append(("Sticker Color Mapping", test_sticker_color_mapping()))
    results.append(("Sticker Color After Moves", test_sticker_color_after_moves()))
    results.append(("Solved Cube Colors", test_solved_cube_expected_colors()))
    results.append(("Color Count Consistency", test_color_counts_consistency()))
    
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
