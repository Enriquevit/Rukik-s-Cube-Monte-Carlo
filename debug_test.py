from cube2 import Cube

# Test L + L'
print("=== Testing L + L' ===")
cube = Cube()
print(f"Initial corner 1: {cube.corners[1]}")
print(f"Is solved: {cube.is_solved()}")

cube.apply_move('L')
print(f"After L, corner 1: {cube.corners[1]}")
print(f"After L, corner 2: {cube.corners[2]}")

cube.apply_move("L'")
print(f"After L + L', corner 1: {cube.corners[1]}")
print(f"After L + L', corner 2: {cube.corners[2]}")
print(f"Is solved: {cube.is_solved()}")

# Test R for comparison
print("\n=== Testing R + R' ===")
cube2 = Cube()
print(f"Initial corner 0: {cube2.corners[0]}")

cube2.apply_move('R')
print(f"After R, corner 0: {cube2.corners[0]}")

cube2.apply_move("R'")
print(f"After R + R', corner 0: {cube2.corners[0]}")
print(f"Is solved: {cube2.is_solved()}")
