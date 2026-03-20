"""Diagnose why F2L algorithm candidates fail."""
import random
from cube3 import Cube
from cross_solver import CrossSolver
from F2L_solver import F2LSolver, F2L_TARGETS, F2L_SLOTS, _find_corner, _find_edge

cs = CrossSolver()
fs = F2LSolver()

random.seed(0)
c = Cube()
c.scramble(20)
_, c2 = cs.solve_cross(c)

print("Cross solved:", cs.is_cross_complete(c2))
print()

for si in range(4):
    target = F2L_TARGETS[si]
    c_colors = frozenset(target['corner'])
    e_colors = frozenset(target['edge'])
    c_pos = _find_corner(c2, c_colors)
    e_pos = _find_edge(c2, e_colors)

    cs_slot, es_slot = F2L_SLOTS[si][0], F2L_SLOTS[si][1]
    print("Slot %d: corner target=%s at pos %d, edge target=%s at pos %d" % (
        si, target['corner'], c_pos, target['edge'], e_pos))
    print("  Corner stickers at pos %d: %s" % (c_pos, c2.corners[c_pos]))
    print("  Edge stickers at pos %d: %s" % (e_pos, c2.edges[e_pos]))
    print("  Slot %d corner: %s (want %s)" % (cs_slot, c2.corners[cs_slot], target['corner']))
    print("  Slot %d edge: %s (want %s)" % (es_slot, c2.edges[es_slot], target['edge']))
    print("  Solved:", fs.is_slot_solved(c2, si))

    # Count candidates
    candidates = fs._generate_candidates(c2, si, [])
    print("  Total candidates: %d" % len(candidates))

    # Try algorithms without BFS
    result = fs._solve_slot.__wrapped__(fs, c2, si, []) if hasattr(fs._solve_slot, '__wrapped__') else None

    # Just try the candidates directly (skip BFS)
    from F2L_solver import _fast_copy
    found = None
    for seq in candidates:
        test = _fast_copy(c2)
        test.apply_moves(seq)
        if fs._is_goal(test, si, []):
            found = seq
            break
    if found:
        print("  FOUND: %s (%d moves)" % (' '.join(found), len(found)))
    else:
        print("  NO MATCH from any candidate!")
    print()
