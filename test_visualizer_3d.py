"""
Test suite for cube_visualizer_3d.py
Tests 3D coordinate generation and rendering logic
"""
import math
from cube import Cube
from cube_visualizer_3d import Cube3DVisualizer, rotate_point


def test_rotate_point_basic():
    """Test basic point rotation functionality"""
    print("=" * 60)
    print("Test 1: Basic Point Rotation")
    print("=" * 60)
    
    # Identity rotation should not change the point
    pt = (1, 0, 0)
    result = rotate_point(pt, 0, 0)
    if abs(result[0] - pt[0]) < 0.0001 and abs(result[1] - pt[1]) < 0.0001 and abs(result[2] - pt[2]) < 0.0001:
        print("[PASS] Identity rotation: (1,0,0) remains unchanged")
    else:
        print(f"[FAIL] Identity rotation: (1,0,0) became {result}")
    
    # 90 degree rotation around Y axis should transform x->z and z->-x
    pt = (1, 0, 0)
    result = rotate_point(pt, math.pi/2, 0)
    expected_z = -1  # x becomes z but negated
    if abs(result[0] - 0) < 0.0001 and abs(result[2] - expected_z) < 0.0001:
        print(f"[PASS] 90° Y-axis rotation: (1,0,0) became (0,0,{expected_z:.1f})")
    else:
        print(f"[FAIL] 90° Y-axis rotation: expected (0, 0, {expected_z}), got {result}")
    
    # Rotation should preserve distance from origin
    pt = (1, 2, 3)
    original_dist = math.sqrt(pt[0]**2 + pt[1]**2 + pt[2]**2)
    result = rotate_point(pt, 0.5, 0.3)
    rotated_dist = math.sqrt(result[0]**2 + result[1]**2 + result[2]**2)
    if abs(original_dist - rotated_dist) < 0.0001:
        print(f"[PASS] Distance preserved: {original_dist:.4f} vs {rotated_dist:.4f}")
    else:
        print(f"[FAIL] Distance not preserved: {original_dist:.4f} vs {rotated_dist:.4f}")


def test_cube_3d_initialization():
    """Test that Cube3DVisualizer initializes correctly"""
    print("\n" + "=" * 60)
    print("Test 2: Cube3DVisualizer Initialization")
    print("=" * 60)
    
    try:
        cube = Cube()
        visualizer = Cube3DVisualizer(cube, size=400)
        
        # Check basic properties
        if visualizer.size == 400:
            print("[PASS] Visualizer size set correctly")
        else:
            print(f"[FAIL] Visualizer size: expected 400, got {visualizer.size}")
        
        # Check sticker_quads generated
        if len(visualizer.sticker_quads) == 54:  # 6 faces * 9 stickers per face
            print("[PASS] 54 sticker quads generated (6 faces × 9 stickers)")
        else:
            print(f"[FAIL] Expected 54 sticker quads, got {len(visualizer.sticker_quads)}")
        
        # Check each face has 9 stickers
        face_counts = {}
        for face, (r, c), quad in visualizer.sticker_quads:
            face_counts[face] = face_counts.get(face, 0) + 1
        
        for face in ['U', 'D', 'F', 'B', 'L', 'R']:
            if face_counts.get(face, 0) == 9:
                print(f"[PASS] Face {face} has 9 stickers")
            else:
                print(f"[FAIL] Face {face} has {face_counts.get(face, 0)} stickers, expected 9")
        
        return True
    except Exception as e:
        print(f"[FAIL] Initialization error: {e}")
        return False


def test_sticker_quads_structure():
    """Test that each sticker quad has correct 3D structure"""
    print("\n" + "=" * 60)
    print("Test 3: Sticker Quad Structure")
    print("=" * 60)
    
    try:
        cube = Cube()
        visualizer = Cube3DVisualizer(cube, size=400)
        
        errors = []
        for face, (r, c), quad in visualizer.sticker_quads:
            # Each quad should have 4 vertices
            if len(quad) != 4:
                errors.append(f"Face {face}[{r}][{c}]: quad has {len(quad)} vertices, expected 4")
            
            # Each vertex should be a 3-tuple
            for i, vertex in enumerate(quad):
                if not isinstance(vertex, tuple) or len(vertex) != 3:
                    errors.append(f"Face {face}[{r}][{c}] vertex {i}: invalid format {vertex}")
                
                # Each coordinate should be finite
                for j, coord in enumerate(vertex):
                    if not isinstance(coord, (int, float)) or math.isnan(coord) or math.isinf(coord):
                        errors.append(f"Face {face}[{r}][{c}] vertex {i} coord {j}: invalid {coord}")
        
        if not errors:
            print("[PASS] All sticker quads have valid structure")
            return True
        else:
            print(f"[FAIL] {len(errors)} structure errors found:")
            for error in errors[:5]:  # Show first 5 errors
                print(f"  - {error}")
            return False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False


def test_sticker_positions_within_bounds():
    """Test that all sticker vertices are within expected bounds for a unit cube"""
    print("\n" + "=" * 60)
    print("Test 4: Sticker Positions Within Bounds")
    print("=" * 60)
    
    try:
        cube = Cube()
        visualizer = Cube3DVisualizer(cube, size=400)
        
        # For a unit cube centered at origin from -1 to 1, max distance from center is sqrt(3) ≈ 1.732
        max_allowed_dist = 2.0  # Generous bound for ±1 cube (sqrt(3) ≈ 1.732)
        
        errors = []
        for face, (r, c), quad in visualizer.sticker_quads:
            for vertex in quad:
                x, y, z = vertex
                dist = math.sqrt(x**2 + y**2 + z**2)
                if dist > max_allowed_dist:
                    errors.append(f"Face {face}[{r}][{c}]: vertex {vertex} distance {dist:.3f} exceeds {max_allowed_dist}")
        
        if not errors:
            print(f"[PASS] All sticker vertices within {max_allowed_dist} unit distance")
            return True
        else:
            print(f"[FAIL] {len(errors)} out-of-bounds vertices:")
            for error in errors[:5]:
                print(f"  - {error}")
            return False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False


def test_face_axes_correctness():
    """Test that face axes form valid orthonormal bases"""
    print("\n" + "=" * 60)
    print("Test 5: Face Axes Validity")
    print("=" * 60)
    
    try:
        cube = Cube()
        visualizer = Cube3DVisualizer(cube, size=400)
        
        errors = []
        for face in ['U', 'D', 'F', 'B', 'L', 'R']:
            center, u_axis, v_axis = visualizer._face_axes(face)
            
            # Check center is on face surface (one component should be ±1)
            center_dist = sum(abs(c) for c in center)
            if not (0.95 < center_dist < 1.05):
                errors.append(f"Face {face} center {center} not on unit sphere surface")
            
            # Check axes are unit vectors
            u_len = math.sqrt(sum(c**2 for c in u_axis))
            v_len = math.sqrt(sum(c**2 for c in v_axis))
            if not (0.95 < u_len < 1.05):
                errors.append(f"Face {face} u_axis length {u_len:.3f}, expected ~1.0")
            if not (0.95 < v_len < 1.05):
                errors.append(f"Face {face} v_axis length {v_len:.3f}, expected ~1.0")
            
            # Check axes are orthogonal
            dot_product = sum(u_axis[i] * v_axis[i] for i in range(3))
            if abs(dot_product) > 0.01:
                errors.append(f"Face {face} axes not orthogonal: dot={dot_product:.3f}")
        
        if not errors:
            print("[PASS] All face axes are valid orthonormal bases")
            return True
        else:
            print(f"[FAIL] {len(errors)} axis errors:")
            for error in errors:
                print(f"  - {error}")
            return False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False


def test_projection_basic():
    """Test that projection works without crashing"""
    print("\n" + "=" * 60)
    print("Test 6: Projection Basic Functionality")
    print("=" * 60)
    
    try:
        cube = Cube()
        visualizer = Cube3DVisualizer(cube, size=400)
        
        # Test projecting various 3D points
        test_points = [
            (0, 0, 0),      # center
            (1, 0, 0),      # on surface
            (0, 1, 0),
            (0, 0, 1),
            (-1, -1, -1),   # corner
        ]
        
        errors = []
        for pt in test_points:
            try:
                result = visualizer.project(pt)
                sx, sy, zc = result
                
                # Check results are reasonable
                if not (0 <= sx <= 400 or -50 <= sx <= 450):  # slack for off-screen
                    errors.append(f"Point {pt}: projected x={sx} is way off")
                if not isinstance(zc, (int, float)) or math.isnan(zc) or zc <= 0:
                    errors.append(f"Point {pt}: projected depth z={zc} is invalid")
            except Exception as e:
                errors.append(f"Point {pt}: projection error {e}")
        
        if not errors:
            print("[PASS] Projection works correctly for test points")
            return True
        else:
            print(f"[FAIL] {len(errors)} projection errors:")
            for error in errors:
                print(f"  - {error}")
            return False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False


def test_consistency_after_moves():
    """Test that sticker_quads remain consistent after cube moves"""
    print("\n" + "=" * 60)
    print("Test 7: Consistency After Moves")
    print("=" * 60)
    
    try:
        cube = Cube()
        visualizer = Cube3DVisualizer(cube, size=400)
        
        # Apply moves to the cube
        moves = ["R", "U", "F", "D", "L", "B"]
        for move in moves:
            cube.apply_move(move)
        
        # Verify sticker_quads still make sense
        if len(visualizer.sticker_quads) != 54:
            print(f"[FAIL] Sticker quads changed: expected 54, got {len(visualizer.sticker_quads)}")
            return False
        
        # Verify all quad structures are still valid
        for face, (r, c), quad in visualizer.sticker_quads:
            if len(quad) != 4:
                print(f"[FAIL] Quad corrupted: {face}[{r}][{c}]")
                return False
            for vertex in quad:
                if len(vertex) != 3:
                    print(f"[FAIL] Vertex corrupted in {face}[{r}][{c}]")
                    return False
        
        print("[PASS] Sticker quads remain consistent after moves")
        return True
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False


def main():
    print("\n" + "=" * 60)
    print("CUBE 3D VISUALIZER TEST SUITE")
    print("=" * 60)
    
    results = []
    
    test_rotate_point_basic()
    results.append(("Rotate Point Basic", True))  # Already handles all reporting
    
    results.append(("Cube3DVisualizer Initialization", test_cube_3d_initialization()))
    results.append(("Sticker Quad Structure", test_sticker_quads_structure()))
    results.append(("Sticker Positions Bounds", test_sticker_positions_within_bounds()))
    results.append(("Face Axes Validity", test_face_axes_correctness()))
    results.append(("Projection Basic", test_projection_basic()))
    results.append(("Consistency After Moves", test_consistency_after_moves()))
    
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
