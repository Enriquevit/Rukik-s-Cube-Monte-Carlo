"""Smoke test F2L solver."""
import random, time
from cube3 import Cube
from cross_solver import CrossSolver, CROSS_EDGE_TARGETS
from F2L_solver import (
    F2L_ALGORITHMS, is_slot_solved, is_f2l_complete,
    solve_f2l, SLOT_ORDER
)

cs = CrossSolver()

for slot in SLOT_ORDER:
    print("Table[%s]: %d cases" % (slot, len(F2L_ALGORITHMS[slot])))

N = 20
ok = 0
fails = []
total_time = 0

for seed in range(N):
    random.seed(seed)
    c = Cube()
    c.scramble(20)
    _, c2 = cs.solve_cross(c)
    if not cs.is_cross_complete(c2):
        print("seed %d: cross failed" % seed)
        continue

    t0 = time.time()
    moves, result = solve_f2l(c2)
    dt = time.time() - t0
    total_time += dt

    cross_ok = all(result.edges[s] == CROSS_EDGE_TARGETS[s] for s in range(4))
    f2l_ok = is_f2l_complete(result)
    slots_solved = sum(1 for s in SLOT_ORDER if is_slot_solved(result, s))

    status = "OK" if (f2l_ok and cross_ok) else "FAIL"
    print("seed=%2d  %s  moves=%2d  slots=%d  cross=%s  %.1fs" % (
        seed, status, len(moves), slots_solved, cross_ok, dt))

    if f2l_ok and cross_ok:
        ok += 1
    else:
        fails.append(seed)

print("\n%d / %d solved  (%.1fs total, %.1fs avg)" % (ok, N, total_time, total_time/max(N,1)))
if fails:
    print("Failed seeds:", fails)
