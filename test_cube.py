import unittest
from cube import Cube

class TestCube(unittest.TestCase):
    def setUp(self):
        self.cube = Cube()

    def test_rotate_U_clockwise(self):
        # Save initial state
        initial_U = [row[:] for row in self.cube.sides['U'].grid]
        initial_F = [row[:] for row in self.cube.sides['F'].grid]
        initial_R = [row[:] for row in self.cube.sides['R'].grid]
        initial_B = [row[:] for row in self.cube.sides['B'].grid]
        initial_L = [row[:] for row in self.cube.sides['L'].grid]

        self.cube.rotate_U(clockwise=True)

        # U face should be rotated clockwise
        expected_U = [list(row) for row in zip(*initial_U[::-1])]
        self.assertEqual(self.cube.sides['U'].grid, expected_U)

        # F top row should now be L's top row
        self.assertEqual(self.cube.sides['F'].grid[0], initial_L[0])
        # L top row should now be B's top row
        self.assertEqual(self.cube.sides['L'].grid[0], initial_B[0])
        # B top row should now be R's top row
        self.assertEqual(self.cube.sides['B'].grid[0], initial_R[0])
        # R top row should now be F's top row
        self.assertEqual(self.cube.sides['R'].grid[0], initial_F[0])

    def test_rotate_U_counterclockwise(self):
        # Save initial state
        initial_U = [row[:] for row in self.cube.sides['U'].grid]
        initial_F = [row[:] for row in self.cube.sides['F'].grid]
        initial_R = [row[:] for row in self.cube.sides['R'].grid]
        initial_B = [row[:] for row in self.cube.sides['B'].grid]
        initial_L = [row[:] for row in self.cube.sides['L'].grid]

        self.cube.rotate_U(clockwise=False)

        # U face should be rotated counterclockwise
        expected_U = [list(row) for row in zip(*initial_U)][::-1]
        self.assertEqual(self.cube.sides['U'].grid, expected_U)

        # F top row should now be R's top row
        self.assertEqual(self.cube.sides['F'].grid[0], initial_R[0])
        # R top row should now be B's top row
        self.assertEqual(self.cube.sides['R'].grid[0], initial_B[0])
        # B top row should now be L's top row
        self.assertEqual(self.cube.sides['B'].grid[0], initial_L[0])
        # L top row should now be F's top row
        self.assertEqual(self.cube.sides['L'].grid[0], initial_F[0])

    def test_rotate_D_clockwise(self):
        initial_D = [row[:] for row in self.cube.sides['D'].grid]
        initial_F = [row[:] for row in self.cube.sides['F'].grid]
        initial_R = [row[:] for row in self.cube.sides['R'].grid]
        initial_B = [row[:] for row in self.cube.sides['B'].grid]
        initial_L = [row[:] for row in self.cube.sides['L'].grid]
        if not hasattr(self.cube, 'rotate_D'):
            self.skipTest('rotate_D not implemented')
        self.cube.rotate_D(clockwise=True)
        expected_D = [list(row) for row in zip(*initial_D[::-1])]
        self.assertEqual(self.cube.sides['D'].grid, expected_D)

    def test_rotate_D_counterclockwise(self):
        initial_D = [row[:] for row in self.cube.sides['D'].grid]
        if not hasattr(self.cube, 'rotate_D'):
            self.skipTest('rotate_D not implemented')
        self.cube.rotate_D(clockwise=False)
        expected_D = [list(row) for row in zip(*initial_D)][::-1]
        self.assertEqual(self.cube.sides['D'].grid, expected_D)

    def test_rotate_F_clockwise(self):
        initial_F = [row[:] for row in self.cube.sides['F'].grid]
        if not hasattr(self.cube, 'rotate_F'):
            self.skipTest('rotate_F not implemented')
        self.cube.rotate_F(clockwise=True)
        expected_F = [list(row) for row in zip(*initial_F[::-1])]
        self.assertEqual(self.cube.sides['F'].grid, expected_F)

    def test_rotate_F_counterclockwise(self):
        initial_F = [row[:] for row in self.cube.sides['F'].grid]
        if not hasattr(self.cube, 'rotate_F'):
            self.skipTest('rotate_F not implemented')
        self.cube.rotate_F(clockwise=False)
        expected_F = [list(row) for row in zip(*initial_F)][::-1]
        self.assertEqual(self.cube.sides['F'].grid, expected_F)

    def test_rotate_B_clockwise(self):
        initial_B = [row[:] for row in self.cube.sides['B'].grid]
        if not hasattr(self.cube, 'rotate_B'):
            self.skipTest('rotate_B not implemented')
        self.cube.rotate_B(clockwise=True)
        expected_B = [list(row) for row in zip(*initial_B[::-1])]
        self.assertEqual(self.cube.sides['B'].grid, expected_B)

    def test_rotate_B_counterclockwise(self):
        initial_B = [row[:] for row in self.cube.sides['B'].grid]
        if not hasattr(self.cube, 'rotate_B'):
            self.skipTest('rotate_B not implemented')
        self.cube.rotate_B(clockwise=False)
        expected_B = [list(row) for row in zip(*initial_B)][::-1]
        self.assertEqual(self.cube.sides['B'].grid, expected_B)

    def test_rotate_L_clockwise(self):
        initial_L = [row[:] for row in self.cube.sides['L'].grid]
        if not hasattr(self.cube, 'rotate_L'):
            self.skipTest('rotate_L not implemented')
        self.cube.rotate_L(clockwise=True)
        expected_L = [list(row) for row in zip(*initial_L[::-1])]
        self.assertEqual(self.cube.sides['L'].grid, expected_L)

    def test_rotate_L_counterclockwise(self):
        initial_L = [row[:] for row in self.cube.sides['L'].grid]
        if not hasattr(self.cube, 'rotate_L'):
            self.skipTest('rotate_L not implemented')
        self.cube.rotate_L(clockwise=False)
        expected_L = [list(row) for row in zip(*initial_L)][::-1]
        self.assertEqual(self.cube.sides['L'].grid, expected_L)

    def test_rotate_R_clockwise(self):
        initial_R = [row[:] for row in self.cube.sides['R'].grid]
        if not hasattr(self.cube, 'rotate_R'):
            self.skipTest('rotate_R not implemented')
        self.cube.rotate_R(clockwise=True)
        expected_R = [list(row) for row in zip(*initial_R[::-1])]
        self.assertEqual(self.cube.sides['R'].grid, expected_R)

    def test_rotate_R_counterclockwise(self):
        initial_R = [row[:] for row in self.cube.sides['R'].grid]
        if not hasattr(self.cube, 'rotate_R'):
            self.skipTest('rotate_R not implemented')
        self.cube.rotate_R(clockwise=False)
        expected_R = [list(row) for row in zip(*initial_R)][::-1]
        self.assertEqual(self.cube.sides['R'].grid, expected_R)

    def test_rotate_M_clockwise(self):
        if not hasattr(self.cube, 'rotate_M'):
            self.skipTest('rotate_M not implemented')
        # Save the middle column of U, F, D, B before rotation
        initial_U = [row[1] for row in self.cube.sides['U'].grid]
        initial_F = [row[1] for row in self.cube.sides['F'].grid]
        initial_D = [row[1] for row in self.cube.sides['D'].grid]
        initial_B = [row[1] for row in self.cube.sides['B'].grid]
        self.cube.rotate_M(clockwise=True)
        # After M clockwise: U->F, F->D, D->B (reversed), B->U (reversed)
        self.assertEqual([row[1] for row in self.cube.sides['F'].grid], initial_U)
        self.assertEqual([row[1] for row in self.cube.sides['D'].grid], initial_F)
        self.assertEqual([row[1] for row in self.cube.sides['B'].grid][::-1], initial_D)
        self.assertEqual([row[1] for row in self.cube.sides['U'].grid][::-1], initial_B)

    def test_rotate_M_counterclockwise(self):
        if not hasattr(self.cube, 'rotate_M'):
            self.skipTest('rotate_M not implemented')
        initial_U = [row[1] for row in self.cube.sides['U'].grid]
        initial_F = [row[1] for row in self.cube.sides['F'].grid]
        initial_D = [row[1] for row in self.cube.sides['D'].grid]
        initial_B = [row[1] for row in self.cube.sides['B'].grid]
        self.cube.rotate_M(clockwise=False)
        # After M counterclockwise: U->B (reversed), B->D (reversed), D->F, F->U
        self.assertEqual([row[1] for row in self.cube.sides['B'].grid], initial_U[::-1])
        self.assertEqual([row[1] for row in self.cube.sides['D'].grid], initial_B[::-1])
        self.assertEqual([row[1] for row in self.cube.sides['F'].grid], initial_D)
        self.assertEqual([row[1] for row in self.cube.sides['U'].grid], initial_F)

if __name__ == '__main__':
    unittest.main()
