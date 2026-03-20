"""
Tests for ll_algorithms.py — OLL / PLL database correctness.

For every algorithm we verify:
  1. Round-trip:  solved → inverse → forward  ==  solved
  2. F2L preservation:  solved → forward → cross + U-corners + mid-edges intact
  3. Orientation invariants: sum(corner_oris) % 3 == 0, sum(edge_oris) % 2 == 0
"""

import pytest
from cube3 import Cube, SOLVED_CORNERS, SOLVED_EDGES
from ll_algorithms import (
    OLL_ALGORITHMS, PLL_ALGORITHMS,
    ALL_OLL, ALL_PLL,
    to_d_layer, invert_alg, invert_move,
)


# ────────────────────────────────────────────────────────────
#  Helper
# ────────────────────────────────────────────────────────────

def _check_orientation_invariants(cube: Cube):
    """Assert mod-3 / mod-2 orientation sums."""
    corner_ori_sum = sum(cube.get_corner_orientation(i) for i in range(8))
    edge_ori_sum = sum(cube.get_edge_orientation(i) for i in range(12))
    assert corner_ori_sum % 3 == 0, f"corner orientation sum {corner_ori_sum} not ≡0 mod3"
    assert edge_ori_sum % 2 == 0, f"edge orientation sum {edge_ori_sum} not ≡0 mod2"


def _f2l_intact(cube: Cube):
    """Cross (U edges 0-3), U corners (0-3), mid edges (8-11) must be solved."""
    for i in range(4):
        assert cube.corners[i] == SOLVED_CORNERS[i], (
            f"U corner {i}: {cube.corners[i]} != {SOLVED_CORNERS[i]}"
        )
    for i in range(4):
        assert cube.edges[i] == SOLVED_EDGES[i], (
            f"U edge {i}: {cube.edges[i]} != {SOLVED_EDGES[i]}"
        )
    for i in range(8, 12):
        assert cube.edges[i] == SOLVED_EDGES[i], (
            f"mid edge {i}: {cube.edges[i]} != {SOLVED_EDGES[i]}"
        )


# ────────────────────────────────────────────────────────────
#  Converter / utility tests
# ────────────────────────────────────────────────────────────

class TestConverters:
    def test_to_d_layer_sune(self):
        result = to_d_layer("R U R' U R U2 R'")
        assert result == ["R", "D", "R'", "D", "R", "D2", "R'"]

    def test_to_d_layer_fb_swap(self):
        result = to_d_layer("F R U R' U' F'")
        assert result == ["B", "R", "D", "R'", "D'", "B'"]

    def test_invert_move_basic(self):
        assert invert_move("R") == "R'"
        assert invert_move("R'") == "R"
        assert invert_move("R2") == "R2"
        assert invert_move("D") == "D'"
        assert invert_move("D'") == "D"

    def test_invert_alg(self):
        alg = ["R", "U", "R'"]
        inv = invert_alg(alg)
        assert inv == ["R", "U'", "R'"]

    def test_invert_alg_sexy_move(self):
        # sexy = R U R' U';  inverse = U R U' R'
        alg = ["R", "D", "R'", "D'"]
        inv = invert_alg(alg)
        assert inv == ["D", "R", "D'", "R'"]


# ────────────────────────────────────────────────────────────
#  Coverage checks
# ────────────────────────────────────────────────────────────

class TestCoverage:
    def test_oll_count(self):
        assert len(OLL_ALGORITHMS) == 57, f"got {len(OLL_ALGORITHMS)} OLL algorithms"

    def test_pll_count(self):
        assert len(PLL_ALGORITHMS) == 21, f"got {len(PLL_ALGORITHMS)} PLL algorithms"

    def test_oll_numbers(self):
        expected = set(range(1, 58))
        actual = set(OLL_ALGORITHMS.keys())
        assert actual == expected, f"missing OLL: {expected - actual}, extra: {actual - expected}"

    def test_pll_names(self):
        expected = {"Ua", "Ub", "Z", "H",
                    "Aa", "Ab", "E",
                    "T", "F", "Ja", "Jb", "Ra", "Rb",
                    "V", "Y", "Na", "Nb",
                    "Ga", "Gb", "Gc", "Gd"}
        actual = set(PLL_ALGORITHMS.keys())
        assert actual == expected, f"missing PLL: {expected - actual}, extra: {actual - expected}"


# ────────────────────────────────────────────────────────────
#  Round-trip tests:  solved → inverse(alg) → alg → solved
# ────────────────────────────────────────────────────────────

class TestOLLRoundTrip:
    @pytest.mark.parametrize("num", sorted(OLL_ALGORITHMS.keys()))
    def test_oll_roundtrip(self, num):
        alg = OLL_ALGORITHMS[num]
        c = Cube()
        c.apply_moves(invert_alg(alg))
        c.apply_moves(alg)
        assert c.is_solved(), f"OLL {num} round-trip failed"


class TestPLLRoundTrip:
    @pytest.mark.parametrize("name", sorted(PLL_ALGORITHMS.keys()))
    def test_pll_roundtrip(self, name):
        alg = PLL_ALGORITHMS[name]
        c = Cube()
        c.apply_moves(invert_alg(alg))
        c.apply_moves(alg)
        assert c.is_solved(), f"PLL {name} round-trip failed"


# ────────────────────────────────────────────────────────────
#  F2L preservation:  solved → alg → F2L still intact
# ────────────────────────────────────────────────────────────

class TestOLLPreservesF2L:
    @pytest.mark.parametrize("num", sorted(OLL_ALGORITHMS.keys()))
    def test_oll_f2l_preserved(self, num):
        alg = OLL_ALGORITHMS[num]
        c = Cube()
        c.apply_moves(alg)
        _f2l_intact(c)
        _check_orientation_invariants(c)


class TestPLLPreservesF2L:
    @pytest.mark.parametrize("name", sorted(PLL_ALGORITHMS.keys()))
    def test_pll_f2l_preserved(self, name):
        alg = PLL_ALGORITHMS[name]
        c = Cube()
        c.apply_moves(alg)
        _f2l_intact(c)
        _check_orientation_invariants(c)


# ────────────────────────────────────────────────────────────
#  set_f2l_state integration test (no pygame needed)
# ────────────────────────────────────────────────────────────

class TestSetF2LState:
    """Simulate the visualizer's set_f2l_state logic without pygame."""

    def _set_f2l(self, seed):
        import random as _rng
        _rng.seed(seed)
        cube = Cube()
        pll = _rng.choice(ALL_PLL)
        cube.apply_moves(invert_alg(pll))
        auf = _rng.choice(['', 'D', "D'", 'D2'])
        if auf:
            cube.apply_move(auf)
        oll = _rng.choice(ALL_OLL)
        cube.apply_moves(invert_alg(oll))
        auf2 = _rng.choice(['', 'D', "D'", 'D2'])
        if auf2:
            cube.apply_move(auf2)
        return cube

    @pytest.mark.parametrize("seed", range(50))
    def test_f2l_intact_after_set(self, seed):
        cube = self._set_f2l(seed)
        _f2l_intact(cube)

    @pytest.mark.parametrize("seed", range(50))
    def test_orientation_invariants(self, seed):
        cube = self._set_f2l(seed)
        _check_orientation_invariants(cube)

    def test_produces_variety(self):
        """Different seeds should produce different D-layer states."""
        states = set()
        for seed in range(20):
            cube = self._set_f2l(seed)
            d_state = tuple(tuple(c) for c in cube.corners[4:8]) + \
                      tuple(tuple(e) for e in cube.edges[4:8])
            states.add(d_state)
        assert len(states) >= 10, f"only {len(states)} distinct states from 20 seeds"
