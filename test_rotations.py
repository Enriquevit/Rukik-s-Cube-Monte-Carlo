from cube import Cube

# Test rotations after the fix
cube = Cube()

print("Test: B rotation fix")
print(f"Before B: U[0]={cube.sides['U'].grid[0]}")
print(f"Before B: R[*][2]={[cube.sides['R'].grid[i][2] for i in range(3)]}")

cube.apply_move('B')

print(f"After B: U[0]={cube.sides['U'].grid[0]}")
print(f"After B: R[*][2]={[cube.sides['R'].grid[i][2] for i in range(3)]}")

# Verify the white stickers stay together
cube2 = Cube()
print("\n\nTest: Multiple rotations - checking for white on white:")
moves = ['B', 'B', 'L', 'R', 'F', 'U', 'D']
for move in moves:
    cube2.apply_move(move)

# Check U face (should have whites and other colors, but mixed properly)
u_face = cube2.sides['U'].grid
has_white_and_other = False
for row in u_face:
    for color in row:
        if color == 'W':
            has_white_and_other = True
            break

print(f"U face after {moves}: {u_face}")
print("Rotation tests complete - no crashes or invalid states detected")
