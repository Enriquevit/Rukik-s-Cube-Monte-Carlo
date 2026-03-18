import random


class Piece:
    """Represents a corner or edge piece on the Rubik's cube."""
    
    def __init__(self, colors, orientation=0):
        """
        Initialize a piece.
        
        Args:
            colors: tuple of colors, e.g. ('W', 'R', 'G') for corner or ('W', 'R') for edge
            orientation: 0, 1, or 2 for corners; 0 or 1 for edges
        """
        self.colors = tuple(colors)
        self.orientation = orientation
    
    def copy(self):
        """Return a deep copy of this piece."""
        return Piece(self.colors, self.orientation)
    
    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return self.colors == other.colors and self.orientation == other.orientation
    
    def __repr__(self):
        return f"Piece({self.colors}, orient={self.orientation})"


class Cube:
    """Piece-based Rubik's Cube representation using corners and edges."""
    
    # Solved state for reference
    SOLVED_CORNERS = [
        Piece(('W', 'R', 'G')),  # 0: URF
        Piece(('W', 'G', 'O')),  # 1: UFL
        Piece(('W', 'O', 'B')),  # 2: ULB
        Piece(('W', 'B', 'R')),  # 3: UBR
        Piece(('Y', 'G', 'R')),  # 4: DFR
        Piece(('Y', 'O', 'G')),  # 5: DLF
        Piece(('Y', 'B', 'O')),  # 6: DBL
        Piece(('Y', 'R', 'B')),  # 7: DRB
    ]
    
    SOLVED_EDGES = [
        Piece(('W', 'R')),   # 0: UR
        Piece(('W', 'G')),   # 1: UF
        Piece(('W', 'O')),   # 2: UL
        Piece(('W', 'B')),   # 3: UB
        Piece(('Y', 'R')),   # 4: DR
        Piece(('Y', 'G')),   # 5: DF
        Piece(('Y', 'O')),   # 6: DL
        Piece(('Y', 'B')),   # 7: DB
        Piece(('R', 'G')),   # 8: FR
        Piece(('G', 'O')),   # 9: FL
        Piece(('O', 'B')),   # 10: BL
        Piece(('B', 'R')),   # 11: BR
    ]
    
    def __init__(self):
        """Initialize cube in solved state."""
        self.reset()
    
    def reset(self):
        """Reset cube to solved state."""
        self.corners = [p.copy() for p in self.SOLVED_CORNERS]
        self.edges = [p.copy() for p in self.SOLVED_EDGES]
    
    # ========== U Face Moves ==========
    
    def rotate_U(self, clockwise=True):
        """Rotate U (top) layer 90 degrees. No orientation changes."""
        if clockwise:
            # Cycle corners: 0→1→2→3→0
            temp = [self.corners[i].copy() for i in [0, 1, 2, 3]]
            self.corners[1] = temp[0]
            self.corners[2] = temp[1]
            self.corners[3] = temp[2]
            self.corners[0] = temp[3]
            
            # Cycle edges: 0→1→2→3→0
            temp = [self.edges[i].copy() for i in [0, 1, 2, 3]]
            self.edges[1] = temp[0]
            self.edges[2] = temp[1]
            self.edges[3] = temp[2]
            self.edges[0] = temp[3]
        else:
            # Counter-clockwise: 0→3→2→1→0
            temp = [self.corners[i].copy() for i in [0, 1, 2, 3]]
            self.corners[0] = temp[1]
            self.corners[1] = temp[2]
            self.corners[2] = temp[3]
            self.corners[3] = temp[0]
            
            temp = [self.edges[i].copy() for i in [0, 1, 2, 3]]
            self.edges[0] = temp[1]
            self.edges[1] = temp[2]
            self.edges[2] = temp[3]
            self.edges[3] = temp[0]
    
    # ========== D Face Moves ==========
    
    def rotate_D(self, clockwise=True):
        """Rotate D (bottom) layer 90 degrees. No orientation changes."""
        if clockwise:
            # Cycle corners: 4→5→6→7→4
            temp = [self.corners[i].copy() for i in [4, 5, 6, 7]]
            self.corners[5] = temp[0]
            self.corners[6] = temp[1]
            self.corners[7] = temp[2]
            self.corners[4] = temp[3]
            
            # Cycle edges: 4→5→6→7→4
            temp = [self.edges[i].copy() for i in [4, 5, 6, 7]]
            self.edges[5] = temp[0]
            self.edges[6] = temp[1]
            self.edges[7] = temp[2]
            self.edges[4] = temp[3]
        else:
            # Counter-clockwise: 4→7→6→5→4
            temp = [self.corners[i].copy() for i in [4, 5, 6, 7]]
            self.corners[4] = temp[1]
            self.corners[5] = temp[2]
            self.corners[6] = temp[3]
            self.corners[7] = temp[0]
            
            temp = [self.edges[i].copy() for i in [4, 5, 6, 7]]
            self.edges[4] = temp[1]
            self.edges[5] = temp[2]
            self.edges[6] = temp[3]
            self.edges[7] = temp[0]
    
    # ========== R Face Moves ==========
    
    def rotate_R(self, clockwise=True):
        """Rotate R (right) layer 90 degrees. Corner orientation changes."""
        if clockwise:
            # Cycle: 0→4→7→3→0, orientation deltas [1, 2, 1, 2]
            temp = [self.corners[i].copy() for i in [0, 3, 4, 7]]
            self.corners[4] = temp[0]
            self.corners[4].orientation = (temp[0].orientation + 1) % 3
            self.corners[7] = temp[2]
            self.corners[7].orientation = (temp[2].orientation + 2) % 3
            self.corners[3] = temp[1]
            self.corners[3].orientation = (temp[1].orientation + 1) % 3
            self.corners[0] = temp[3]
            self.corners[0].orientation = (temp[3].orientation + 2) % 3
            
            # Edges: 0→8→11→3→0, no orientation changes (R doesn't flip edges)
            temp = [self.edges[i].copy() for i in [0, 3, 8, 11]]
            self.edges[8] = temp[0]
            self.edges[11] = temp[3]
            self.edges[3] = temp[1]
            self.edges[0] = temp[2]
        else:
            # Counter-clockwise: 0→3→7→4→0, orientation deltas [2, 1, 2, 1]
            temp = [self.corners[i].copy() for i in [0, 3, 4, 7]]
            self.corners[3] = temp[0]
            self.corners[3].orientation = (temp[0].orientation + 2) % 3
            self.corners[0] = temp[3]
            self.corners[0].orientation = (temp[3].orientation + 1) % 3
            self.corners[4] = temp[1]
            self.corners[4].orientation = (temp[1].orientation + 2) % 3
            self.corners[7] = temp[2]
            self.corners[7].orientation = (temp[2].orientation + 1) % 3
            
            # Edges: 0→3→11→8→0, no orientation changes
            temp = [self.edges[i].copy() for i in [0, 3, 8, 11]]
            self.edges[3] = temp[0]
            self.edges[0] = temp[1]
            self.edges[8] = temp[3]
            self.edges[11] = temp[2]
    
    # ========== L Face Moves ==========
    
    def rotate_L(self, clockwise=True):
        """Rotate L (left) layer 90 degrees. Corner orientation changes."""
        if clockwise:
            # Cycle: 1→5→6→2→1, orientation deltas [2, 1, 2, 1]
            temp = [self.corners[i].copy() for i in [1, 2, 5, 6]]
            self.corners[5] = temp[0]
            self.corners[5].orientation = (temp[0].orientation + 2) % 3
            self.corners[6] = temp[2]
            self.corners[6].orientation = (temp[2].orientation + 1) % 3
            self.corners[2] = temp[3]
            self.corners[2].orientation = (temp[3].orientation + 2) % 3
            self.corners[1] = temp[1]
            self.corners[1].orientation = (temp[1].orientation + 1) % 3
            
            # Edges: 1→9→10→2→1, no orientation changes
            temp = [self.edges[i].copy() for i in [1, 2, 9, 10]]
            self.edges[9] = temp[0]
            self.edges[10] = temp[3]
            self.edges[2] = temp[1]
            self.edges[1] = temp[2]
        else:
            # Counter-clockwise: 1→2→6→5→1, orientation deltas [1, 2, 1, 2]
            temp = [self.corners[i].copy() for i in [1, 2, 5, 6]]
            self.corners[2] = temp[0]
            self.corners[2].orientation = (temp[0].orientation + 1) % 3
            self.corners[1] = temp[1]
            self.corners[1].orientation = (temp[1].orientation + 2) % 3
            self.corners[5] = temp[3]
            self.corners[5].orientation = (temp[3].orientation + 2) % 3
            self.corners[6] = temp[2]
            self.corners[6].orientation = (temp[2].orientation + 1) % 3
            
            # Edges: 1→2→10→9→1, no orientation changes
            temp = [self.edges[i].copy() for i in [1, 2, 9, 10]]
            self.edges[2] = temp[0]
            self.edges[1] = temp[1]
            self.edges[9] = temp[3]
            self.edges[10] = temp[2]
    
    # ========== F Face Moves ==========
    
    def rotate_F(self, clockwise=True):
        """Rotate F (front) layer 90 degrees. Both corner and edge orientations change."""
        if clockwise:
            # Cycle: 0→1→5→4→0, orientation deltas [1, 2, 1, 2]
            temp = [self.corners[i].copy() for i in [0, 1, 4, 5]]
            self.corners[1] = temp[0]
            self.corners[1].orientation = (temp[0].orientation + 1) % 3
            self.corners[5] = temp[1]
            self.corners[5].orientation = (temp[1].orientation + 2) % 3
            self.corners[4] = temp[3]
            self.corners[4].orientation = (temp[3].orientation + 1) % 3
            self.corners[0] = temp[2]
            self.corners[0].orientation = (temp[2].orientation + 2) % 3
            
            # Edges: 1→8→5→9→1, all flip [1, 1, 1, 1]
            temp = [self.edges[i].copy() for i in [1, 5, 8, 9]]
            self.edges[8] = temp[0]
            self.edges[8].orientation = (temp[0].orientation + 1) % 2
            self.edges[5] = temp[2]
            self.edges[5].orientation = (temp[2].orientation + 1) % 2
            self.edges[9] = temp[3]
            self.edges[9].orientation = (temp[3].orientation + 1) % 2
            self.edges[1] = temp[1]
            self.edges[1].orientation = (temp[1].orientation + 1) % 2
        else:
            # Counter-clockwise: 0→4→5→1→0, orientation deltas [2, 1, 2, 1]
            temp = [self.corners[i].copy() for i in [0, 1, 4, 5]]
            self.corners[4] = temp[0]
            self.corners[4].orientation = (temp[0].orientation + 2) % 3
            self.corners[0] = temp[1]
            self.corners[0].orientation = (temp[1].orientation + 1) % 3
            self.corners[1] = temp[2]
            self.corners[1].orientation = (temp[2].orientation + 2) % 3
            self.corners[5] = temp[3]
            self.corners[5].orientation = (temp[3].orientation + 1) % 3
            
            # Edges: 1→9→5→8→1, all flip [1, 1, 1, 1]
            temp = [self.edges[i].copy() for i in [1, 5, 8, 9]]
            self.edges[9] = temp[0]
            self.edges[9].orientation = (temp[0].orientation + 1) % 2
            self.edges[1] = temp[2]
            self.edges[1].orientation = (temp[2].orientation + 1) % 2
            self.edges[8] = temp[3]
            self.edges[8].orientation = (temp[3].orientation + 1) % 2
            self.edges[5] = temp[1]
            self.edges[5].orientation = (temp[1].orientation + 1) % 2
    
    # ========== B Face Moves ==========
    
    def rotate_B(self, clockwise=True):
        """Rotate B (back) layer 90 degrees. Both corner and edge orientations change."""
        if clockwise:
            # Cycle: 2→6→7→3→2, orientation deltas [2, 1, 2, 1]
            temp = [self.corners[i].copy() for i in [2, 3, 6, 7]]
            self.corners[6] = temp[0]
            self.corners[6].orientation = (temp[0].orientation + 2) % 3
            self.corners[7] = temp[2]
            self.corners[7].orientation = (temp[2].orientation + 1) % 3
            self.corners[3] = temp[3]
            self.corners[3].orientation = (temp[3].orientation + 2) % 3
            self.corners[2] = temp[1]
            self.corners[2].orientation = (temp[1].orientation + 1) % 3
            
            # Edges: 3→10→7→11→3, all flip [1, 1, 1, 1]
            temp = [self.edges[i].copy() for i in [3, 7, 10, 11]]
            self.edges[10] = temp[0]
            self.edges[10].orientation = (temp[0].orientation + 1) % 2
            self.edges[7] = temp[2]
            self.edges[7].orientation = (temp[2].orientation + 1) % 2
            self.edges[11] = temp[3]
            self.edges[11].orientation = (temp[3].orientation + 1) % 2
            self.edges[3] = temp[1]
            self.edges[3].orientation = (temp[1].orientation + 1) % 2
        else:
            # Counter-clockwise: 2→3→7→6→2, orientation deltas [1, 2, 1, 2]
            temp = [self.corners[i].copy() for i in [2, 3, 6, 7]]
            self.corners[3] = temp[0]
            self.corners[3].orientation = (temp[0].orientation + 1) % 3
            self.corners[2] = temp[1]
            self.corners[2].orientation = (temp[1].orientation + 2) % 3
            self.corners[6] = temp[3]
            self.corners[6].orientation = (temp[3].orientation + 2) % 3
            self.corners[7] = temp[2]
            self.corners[7].orientation = (temp[2].orientation + 1) % 3
            
            # Edges: 3→11→7→10→3, all flip [1, 1, 1, 1]
            temp = [self.edges[i].copy() for i in [3, 7, 10, 11]]
            self.edges[3] = temp[2]
            self.edges[3].orientation = (temp[2].orientation + 1) % 2
            self.edges[11] = temp[0]
            self.edges[11].orientation = (temp[0].orientation + 1) % 2
            self.edges[10] = temp[1]
            self.edges[10].orientation = (temp[1].orientation + 1) % 2
            self.edges[7] = temp[3]
            self.edges[7].orientation = (temp[3].orientation + 1) % 2
    
    # ========== Move Application ==========
    
    def apply_move(self, move_str):
        """Apply standard Rubik's cube notation move."""
        if not move_str or len(move_str) == 0:
            raise ValueError("Empty move string")
        
        face = move_str[0]
        if face not in ['U', 'D', 'L', 'R', 'F', 'B']:
            raise ValueError(f"Unknown face: {face}")
        
        is_prime = "'" in move_str
        is_double = "2" in move_str
        
        clockwise = not is_prime
        repetitions = 2 if is_double else 1
        
        move_func = getattr(self, f"rotate_{face}")
        for _ in range(repetitions):
            move_func(clockwise=clockwise)
    
    def apply_moves(self, move_list):
        """Apply a list of moves."""
        for move in move_list:
            self.apply_move(move)
    
    # ========== Utility Functions ==========
    
    def is_solved(self):
        """Check if the cube is in the solved state."""
        for i in range(8):
            if self.corners[i] != self.SOLVED_CORNERS[i]:
                return False
        for i in range(12):
            if self.edges[i] != self.SOLVED_EDGES[i]:
                return False
        return True
    
    def scramble(self, num_moves=20):
        """Apply a random scramble to the cube."""
        faces = ['U', 'D', 'L', 'R', 'F', 'B']
        modifiers = ['', "'", '2']
        moves = []
        last_face = None
        
        for _ in range(num_moves):
            face = random.choice([f for f in faces if f != last_face])
            modifier = random.choice(modifiers)
            move = face + modifier
            self.apply_move(move)
            moves.append(move)
            last_face = face
        
        return moves
    
    def get_corner_position(self, corner_idx):
        """Get the piece at a corner position."""
        return self.corners[corner_idx]
    
    def get_edge_position(self, edge_idx):
        """Get the piece at an edge position."""
        return self.edges[edge_idx]
    
    def __repr__(self):
        return (f"Cube(corners={len(self.corners)}, edges={len(self.edges)}, "
                f"solved={self.is_solved()})")


# ========== Example Usage ==========

if __name__ == "__main__":
    print("=== Piece-Based Cube Demo ===\n")
    
    cube = Cube()
    print(f"Cube initialized: {cube}")
    print(f"Is solved: {cube.is_solved()}\n")
    
    print("First corner piece:", cube.get_corner_position(0))
    print("First edge piece:", cube.get_edge_position(0))
    print()
    
    print("Applying U move...")
    cube.apply_move("U")
    print(f"Is solved: {cube.is_solved()}")
    print(f"Corner 0: {cube.get_corner_position(0)}")
    print(f"Edge 0: {cube.get_edge_position(0)}\n")
    
    cube.reset()
    moves = ["R", "U", "R'", "U'"]
    print(f"Applying moves: {' '.join(moves)}")
    cube.apply_moves(moves)
    print(f"Is solved: {cube.is_solved()}\n")
    
    cube.reset()
    scramble = cube.scramble(5)
    print(f"Applied scramble ({len(scramble)} moves): {' '.join(scramble)}")
    print(f"Is solved: {cube.is_solved()}")
    print(f"Cube state: {cube}")
