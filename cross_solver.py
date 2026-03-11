"""
cross_solver.py

CrossSolver class for Rubik's Cube cross solving (beginner, intermediate, advanced).
Includes edge recognition and utilities for advanced cross planning.
"""

from typing import List, Tuple, Dict, Any
from cube import Cube

class CrossSolver:
    def __init__(self, cross_color: str = 'W'):
        self.cross_color = cross_color  # e.g., 'W' for white

    def is_cross_complete(self, cube: Cube) -> bool:
        """
        Check if the white cross is complete on the top (U) face.
        The cross is complete when:
        1. All four edge stickers on U face are white
        2. Each adjacent edge sticker matches its face's center color
        Returns True if cross is complete, False otherwise.
        """
        U = cube.sides['U'].grid
        F = cube.sides['F'].grid
        B = cube.sides['B'].grid
        L = cube.sides['L'].grid
        R = cube.sides['R'].grid

        # Get the center colors of each face
        center_colors = {
            'F': F[1][1],  # Front center is green
            'B': B[1][1],  # Back center is blue
            'L': L[1][1],  # Left center is orange
            'R': R[1][1],  # Right center is red
        }

        # Check if all four edge stickers on U face are white
        edges_on_u = [U[0][1], U[1][0], U[1][2], U[2][1]]
        if not all(e == 'W' for e in edges_on_u):
            return False

        # Check if adjacent edge stickers match their face colors
        # Front-up edge: U[0][1] (W) and F[0][1] (should match F center)
        if F[0][1] != center_colors['F']:
            return False
        
        # Left-up edge: U[1][0] (W) and L[0][1] (should match L center)
        if L[0][1] != center_colors['L']:
            return False
        
        # Right-up edge: U[1][2] (W) and R[0][1] (should match R center)
        if R[0][1] != center_colors['R']:
            return False
        
        # Back-up edge: U[2][1] (W) and B[0][1] (should match B center)
        if B[0][1] != center_colors['B']:
            return False

        return True

    def recognize_cross_edges(self, cube: Cube) -> Dict[str, Any]:
        """
        Recognize the positions and orientations of cross edges for the given cross color.
        Returns a mapping of edge positions and their status.
        
        Returns a dict with edge info:
        {
            'F': {'on_U': bool, 'on_side': bool, 'correct': bool},
            'L': {'on_U': bool, 'on_side': bool, 'correct': bool},
            'R': {'on_U': bool, 'on_side': bool, 'correct': bool},
            'B': {'on_U': bool, 'on_side': bool, 'correct': bool},
        }
        """
        U = cube.sides['U'].grid
        F = cube.sides['F'].grid
        B = cube.sides['B'].grid
        L = cube.sides['L'].grid
        R = cube.sides['R'].grid
        D = cube.sides['D'].grid

        # Center colors
        centers = {
            'F': F[1][1],
            'B': B[1][1],
            'L': L[1][1],
            'R': R[1][1],
        }

        edge_map = {}

        # Check Front edge (should be at U[0][1] and F[0][1])
        edge_map['F'] = {
            'on_U': U[0][1] == 'W' and F[0][1] == centers['F'],
            'on_side': False,
            'correct': U[0][1] == 'W' and F[0][1] == centers['F'],
            'positions': [('U', 0, 1), ('F', 0, 1)]
        }

        # Check Left edge (should be at U[1][0] and L[0][1])
        edge_map['L'] = {
            'on_U': U[1][0] == 'W' and L[0][1] == centers['L'],
            'on_side': False,
            'correct': U[1][0] == 'W' and L[0][1] == centers['L'],
            'positions': [('U', 1, 0), ('L', 0, 1)]
        }

        # Check Right edge (should be at U[1][2] and R[0][1])
        edge_map['R'] = {
            'on_U': U[1][2] == 'W' and R[0][1] == centers['R'],
            'on_side': False,
            'correct': U[1][2] == 'W' and R[0][1] == centers['R'],
            'positions': [('U', 1, 2), ('R', 0, 1)]
        }

        # Check Back edge (should be at U[2][1] and B[0][1])
        edge_map['B'] = {
            'on_U': U[2][1] == 'W' and B[0][1] == centers['B'],
            'on_side': False,
            'correct': U[2][1] == 'W' and B[0][1] == centers['B'],
            'positions': [('U', 2, 1), ('B', 0, 1)]
        }

        return edge_map

    def advanced_cross_map(self, cube: Cube) -> Dict[str, Any]:
        """
        Utility for advanced cross: map all possible cross edge moves and their costs.
        Returns a structure for use in optimal cross search.
        """
        # TODO: Implement advanced cross mapping
        cross_map = {}
        # ... placeholder ...
        return cross_map

    def solve_cross(self, cube: Cube, skill: str = 'beginner') -> Tuple[List[str], Cube]:
        """
        Solve the cross using the specified skill level.
        skill: 'beginner', 'intermediate', 'advanced'
        Returns: (move_sequence, updated_cube)
        """
        if skill == 'beginner':
            return self.solve_cross_beginner(cube)
        elif skill == 'intermediate':
            return self.solve_cross_intermediate(cube)
        elif skill == 'advanced':
            return self.solve_cross_advanced(cube)
        else:
            raise ValueError(f"Unknown skill level: {skill}")

    def solve_cross_beginner(self, cube: Cube) -> Tuple[List[str], Cube]:
        """
        Solve the white cross using basic moves.
        Brings white edges from D layer to U layer one by one.
        """
        moves = []
        cube_copy = Cube()
        # Deep copy the cube state
        for face in cube.sides:
            cube_copy.sides[face].grid = [row[:] for row in cube.sides[face].grid]

        # Get center colors
        centers = {
            'F': cube_copy.sides['F'].grid[1][1],
            'B': cube_copy.sides['B'].grid[1][1],
            'L': cube_copy.sides['L'].grid[1][1],
            'R': cube_copy.sides['R'].grid[1][1],
        }

        # Solve the cross by bring each white edge piece to the top
        for _ in range(20):  # Maximum iterations
            if self.is_cross_complete(cube_copy):
                break

            # Try to solve one edge at a time
            for side in ['F', 'L', 'B', 'R']:
                if self._solve_one_edge_basic(cube_copy, moves, side, centers):
                    break

        return moves, cube_copy

    def _solve_one_edge_basic(self, cube: Cube, moves: List[str], target_side: str, centers: Dict) -> bool:
        """
        Try to solve one white edge for the target side.
        Returns True if a move was made, False otherwise.
        """
        # Check if already solved
        u_pos = {'F': (0, 1), 'L': (1, 0), 'R': (1, 2), 'B': (2, 1)}[target_side]
        if (cube.sides['U'].grid[u_pos[0]][u_pos[1]] == 'W' and
            cube.sides[target_side].grid[0][1] == centers[target_side]):
            return False

        # Scan D layer for the white piece that matches target_side
        d_edges = {
            'F': (0, 1),
            'L': (1, 0),
            'B': (2, 1),
            'R': (1, 2)
        }

        for check_side, (d_row, d_col) in d_edges.items():
            if (cube.sides['D'].grid[d_row][d_col] == 'W' and
                cube.sides[check_side].grid[2][1] == centers[target_side]):
                # Found the white edge on D layer for target_side
                # Align D so it's under target_side
                face_order = ['F', 'R', 'B', 'L']
                rotations_needed = (face_order.index(target_side) - face_order.index(check_side)) % 4
                for _ in range(rotations_needed):
                    moves.append('D')
                    cube.apply_move('D')

                # Flip the edge up (execute double face turn)
                face_moves = {'F': 'F', 'B': 'B', 'L': 'L', 'R': 'R'}[target_side]
                moves.extend([face_moves, face_moves])
                cube.apply_move(face_moves)
                cube.apply_move(face_moves)
                return True

        # If white edge is on a side face top, bring it down first
        for side in ['F', 'B', 'L', 'R']:
            if cube.sides[side].grid[0][1] == 'W':
                u_pos_for_side = {'F': (0, 1), 'B': (2, 1), 'L': (1, 0), 'R': (1, 2)}[side]
                neighbor = cube.sides['U'].grid[u_pos_for_side[0]][u_pos_for_side[1]]
                if neighbor == centers[target_side]:
                    # This is the edge we're looking for, but on top - bring it down
                    move_map = {'F': 'F', 'B': "B'", 'L': "L'", 'R': 'R'}
                    moves.append(move_map[side])
                    cube.apply_move(move_map[side])
                    return True
      
        return False

    def solve_cross_intermediate(self, cube: Cube) -> Tuple[List[str], Cube]:
        """
        Place two cross edges at a time (simple strategy).
        Uses basically the same algorithm as beginner for now, but could be optimized.
        """
        # For now, just use the beginner algorithm
        # TODO: Implement more sophisticated intermediate algorithm
        return self.solve_cross_beginner(cube)

    def solve_cross_advanced(self, cube: Cube) -> Tuple[List[str], Cube]:
        """
        Find optimal cross solution (≤8 moves, search/pruning).
        For now, uses the same logic as intermediate.
        """
        # TODO: Implement advanced cross logic with optimal search
        return self.solve_cross_intermediate(cube)
