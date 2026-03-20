"""Quick F2L solver test."""
import random, time
from cube3 import Cube
from cross_solver import CrossSolver
from F2L_solver import F2LSolver

cs = CrossSolver()
fs = F2LSolver()

successes = 0
total_time = 0
N = 20

for trial in range(N):
    random.seed(trial)
    c = Cube()
    c.scramble(20)
    _, c2 = cs.solve_cross(c)
    if not cs.is_cross_complete(c2):
        print('Trial %d: CROSS FAILED' % trial)
        continue

    t0 = time.time()
    f2l_moves, c3 = fs.solve_f2l(c2)
    dt = time.time() - t0
    total_time += dt

    ok = fs.is_f2l_complete(c3) and cs.is_cross_complete(c3)
    if ok:
        successes += 1
    status = 'OK' if ok else 'FAIL'
    slots = sum(1 for i in range(4) if fs.is_slot_solved(c3, i))
    print('Trial %2d: %s | %2d moves | slots=%d | %.3fs' % (trial, status, len(f2l_moves), slots, dt))

print('\n%d/%d correct | avg time: %.3fs' % (successes, N, total_time / N))
