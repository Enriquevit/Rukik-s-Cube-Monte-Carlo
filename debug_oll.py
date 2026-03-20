"""Diagnostic: check cube3.py move geometry for known identities."""
from cube3 import Cube, SOLVED_CORNERS, SOLVED_EDGES

# Test 1: sexy move x6 = identity
print("=== sexy move (R U R' U') x 6 ===")
c = Cube()
for _ in range(6):
    c.apply_moves(["R", "U", "R'", "U'"])
print("is_solved:", c.is_solved())

# Test 2: F F' = identity
print("\n=== F F' ===")
c = Cube()
c.apply_moves(["F", "F'"])
print("is_solved:", c.is_solved())

# Test 3: F4 = identity
print("\n=== F4 ===")
c = Cube()
for _ in range(4):
    c.apply_move("F")
print("is_solved:", c.is_solved())

# Test 4: T-perm x2 = identity (known failing test)
print("\n=== T-perm x 2 ===")
c = Cube()
tperm = ["R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'", "U'", "R", "U", "R'", "F'"]
for _ in range(2):
    c.apply_moves(tperm)
print("is_solved:", c.is_solved())
if not c.is_solved():
    print("Checking which pieces wrong:")
    for i in range(8):
        if c.corners[i] != SOLVED_CORNERS[i]:
            print(f"  corner {i}: {c.corners[i]} != {SOLVED_CORNERS[i]}")
    for i in range(12):
        if c.edges[i] != SOLVED_EDGES[i]:
            print(f"  edge {i}: {c.edges[i]} != {SOLVED_EDGES[i]}")

# Test 5: single F from solved — check which pieces move
print("\n=== Single F from solved ===")
c = Cube()
c.apply_move("F")
for i in range(8):
    if c.corners[i] != SOLVED_CORNERS[i]:
        print(f"  corner {i} changed: {SOLVED_CORNERS[i]} -> {c.corners[i]}")
for i in range(12):
    if c.edges[i] != SOLVED_EDGES[i]:
        print(f"  edge {i} changed: {SOLVED_EDGES[i]} -> {c.edges[i]}")

# Test 6: Standard OLL 45 from solved, check D-layer / mid preservation 
print("\n=== F R U R' U' F' (OLL 45 standard) ===")
c = Cube()
c.apply_moves(["F", "R", "U", "R'", "U'", "F'"])
d_ok = all(c.corners[i] == SOLVED_CORNERS[i] for i in range(4,8))
mid_ok = all(c.edges[i] == SOLVED_EDGES[i] for i in range(8,12))
de_ok = all(c.edges[i] == SOLVED_EDGES[i] for i in range(4,8))
print(f"D corners: {'OK' if d_ok else 'FAIL'}")
print(f"D edges: {'OK' if de_ok else 'FAIL'}")
print(f"Mid edges: {'OK' if mid_ok else 'FAIL'}")
if not d_ok:
    for i in range(4,8):
        if c.corners[i] != SOLVED_CORNERS[i]:
            print(f"  corner {i}: {SOLVED_CORNERS[i]} -> {c.corners[i]}")
if not mid_ok:
    for i in range(8,12):
        if c.edges[i] != SOLVED_EDGES[i]:
            print(f"  edge {i}: {SOLVED_EDGES[i]} -> {c.edges[i]}")

# Test 7: Check FACE_CYCLES direction for F
# After CW F (looking at F from outside):
# URF→DFR means the URF piece should move to the DFR slot
print("\n=== Verify F direction ===")
c = Cube()
c.apply_move("F")
print(f"  Slot 4 (DFR): {c.corners[4]} (was at URF: {SOLVED_CORNERS[0]})")
print(f"  Slot 5 (DLF): {c.corners[5]} (was at DFR: {SOLVED_CORNERS[4]})")
print(f"  Slot 1 (UFL): {c.corners[1]} (was at DLF: {SOLVED_CORNERS[5]})")
print(f"  Slot 0 (URF): {c.corners[0]} (was at UFL: {SOLVED_CORNERS[1]})")
