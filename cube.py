import random

# Represents a single face of the Rubik's Cube
class Side:
    def __init__(self, color):
        # 3x3 grid initialized with the same color
        self.grid = [[color for _ in range(3)] for _ in range(3)]

    def rotate_clockwise(self):
        # Rotates the face 90 degrees clockwise
        self.grid = [list(row) for row in zip(*self.grid[::-1])]

    def rotate_counterclockwise(self):
        # Rotates the face 90 degrees counterclockwise
        self.grid = [list(row) for row in zip(*self.grid)][::-1]

# Represents the entire Rubik's Cube
class Cube:
    def __init__(self):
        # U: Up, D: Down, F: Front, B: Back, L: Left, R: Right
        self.sides = {
            'U': Side('W'),  # White
            'D': Side('Y'),  # Yellow
            'F': Side('G'),  # Green
            'B': Side('B'),  # Blue
            'L': Side('O'),  # Orange
            'R': Side('R'),  # Red
        }

    def rotate_U(self, clockwise=True):
        # Rotate the Up face and adjust adjacent faces
        if clockwise:
            self.sides['U'].rotate_clockwise()
        else:
            self.sides['U'].rotate_counterclockwise()
        # Adjust the adjacent faces' top rows
        self._rotate_U_adjacent(clockwise)

    def _rotate_U_adjacent(self, clockwise):
        F, R, B, L = self.sides['F'], self.sides['R'], self.sides['B'], self.sides['L']
        if clockwise:
            temp = F.grid[0][:]
            F.grid[0] = L.grid[0][:]
            L.grid[0] = B.grid[0][:]
            B.grid[0] = R.grid[0][:]
            R.grid[0] = temp
        else:
            temp = F.grid[0][:]
            F.grid[0] = R.grid[0][:]
            R.grid[0] = B.grid[0][:]
            B.grid[0] = L.grid[0][:]
            L.grid[0] = temp

    def rotate_D(self, clockwise=True):
        if clockwise:
            self.sides['D'].rotate_clockwise()
        else:
            self.sides['D'].rotate_counterclockwise()
        self._rotate_D_adjacent(clockwise)

    def _rotate_D_adjacent(self, clockwise):
        F, R, B, L = self.sides['F'], self.sides['R'], self.sides['B'], self.sides['L']
        if clockwise:
            temp = F.grid[2][:]
            F.grid[2] = R.grid[2][:]
            R.grid[2] = B.grid[2][:]
            B.grid[2] = L.grid[2][:]
            L.grid[2] = temp
        else:
            temp = F.grid[2][:]
            F.grid[2] = L.grid[2][:]
            L.grid[2] = B.grid[2][:]
            B.grid[2] = R.grid[2][:]
            R.grid[2] = temp

    def rotate_F(self, clockwise=True):
        if clockwise:
            self.sides['F'].rotate_clockwise()
        else:
            self.sides['F'].rotate_counterclockwise()
        self._rotate_F_adjacent(clockwise)

    def _rotate_F_adjacent(self, clockwise):
        U, R, D, L = self.sides['U'], self.sides['R'], self.sides['D'], self.sides['L']
        if clockwise:
            temp = U.grid[2][:]
            U.grid[2] = [L.grid[i][2] for i in range(2, -1, -1)]
            for i in range(3):
                L.grid[i][2] = D.grid[0][i]
            D.grid[0] = [R.grid[i][0] for i in range(2, -1, -1)]
            for i in range(3):
                R.grid[i][0] = temp[i]
        else:
            temp = U.grid[2][:]
            U.grid[2] = [R.grid[i][0] for i in range(3)]
            for i in range(3):
                R.grid[i][0] = D.grid[0][2-i]
            D.grid[0] = [L.grid[i][2] for i in range(3)]
            for i in range(3):
                L.grid[i][2] = temp[2-i]

    def rotate_B(self, clockwise=True):
        if clockwise:
            self.sides['B'].rotate_clockwise()
        else:
            self.sides['B'].rotate_counterclockwise()
        self._rotate_B_adjacent(clockwise)

    def _rotate_B_adjacent(self, clockwise):
        U, R, D, L = self.sides['U'], self.sides['R'], self.sides['D'], self.sides['L']
        if clockwise:
            temp = U.grid[0][:]
            U.grid[0] = [R.grid[i][2] for i in range(3)]
            for i in range(3):
                R.grid[i][2] = D.grid[2][2-i]
            D.grid[2] = [L.grid[i][0] for i in range(3)]
            for i in range(3):
                L.grid[i][0] = temp[2-i]
        else:
            temp = U.grid[0][:]
            U.grid[0] = [L.grid[i][0] for i in range(2, -1, -1)]
            for i in range(3):
                L.grid[i][0] = D.grid[2][i]
            D.grid[2] = [R.grid[i][2] for i in range(2, -1, -1)]
            for i in range(3):
                R.grid[i][2] = temp[i]

    def rotate_L(self, clockwise=True):
        if clockwise:
            self.sides['L'].rotate_clockwise()
        else:
            self.sides['L'].rotate_counterclockwise()
        self._rotate_L_adjacent(clockwise)

    def _rotate_L_adjacent(self, clockwise):
        U, F, D, B = self.sides['U'], self.sides['F'], self.sides['D'], self.sides['B']
        if clockwise:
            temp = [U.grid[i][0] for i in range(3)]
            for i in range(3):
                U.grid[i][0] = B.grid[2-i][2]
                B.grid[2-i][2] = D.grid[i][0]
                D.grid[i][0] = F.grid[i][0]
                F.grid[i][0] = temp[i]
        else:
            temp = [U.grid[i][0] for i in range(3)]
            for i in range(3):
                U.grid[i][0] = F.grid[i][0]
                F.grid[i][0] = D.grid[i][0]
                D.grid[i][0] = B.grid[2-i][2]
                B.grid[2-i][2] = temp[i]

    def rotate_R(self, clockwise=True):
        if clockwise:
            self.sides['R'].rotate_clockwise()
        else:
            self.sides['R'].rotate_counterclockwise()
        self._rotate_R_adjacent(clockwise)

    def _rotate_R_adjacent(self, clockwise):
        U, F, D, B = self.sides['U'], self.sides['F'], self.sides['D'], self.sides['B']
        if clockwise:
            temp = [U.grid[i][2] for i in range(3)]
            for i in range(3):
                U.grid[i][2] = F.grid[i][2]
                F.grid[i][2] = D.grid[i][2]
                D.grid[i][2] = B.grid[2-i][0]
                B.grid[2-i][0] = temp[i]
        else:
            temp = [U.grid[i][2] for i in range(3)]
            for i in range(3):
                U.grid[i][2] = B.grid[2-i][0]
                B.grid[2-i][0] = D.grid[i][2]
                D.grid[i][2] = F.grid[i][2]
                F.grid[i][2] = temp[i]

    def rotate_M(self, clockwise=True):
        U, F, D, B = self.sides['U'], self.sides['F'], self.sides['D'], self.sides['B']
        if clockwise:
            temp = [U.grid[i][1] for i in range(3)]
            for i in range(3):
                U.grid[i][1] = B.grid[2-i][1]
                B.grid[2-i][1] = D.grid[i][1]
                D.grid[i][1] = F.grid[i][1]
                F.grid[i][1] = temp[i]
        else:
            temp = [U.grid[i][1] for i in range(3)]
            for i in range(3):
                U.grid[i][1] = F.grid[i][1]
                F.grid[i][1] = D.grid[i][1]
                D.grid[i][1] = B.grid[2-i][1]
                B.grid[2-i][1] = temp[i]

    def apply_move(self, mv: str):
        """Apply a single move in standard notation, e.g. "U", "U'", "F", "R'".

        This centralizes move application so external code can use the same
        legal-turn logic as the cube implementation.
        """
        prime = mv.endswith("'")
        face = mv[0]
        clockwise = not prime
        if face == 'U':
            self.rotate_U(clockwise=clockwise)
        elif face == 'D':
            self.rotate_D(clockwise=clockwise)
        elif face == 'F':
            self.rotate_F(clockwise=clockwise)
        elif face == 'B':
            self.rotate_B(clockwise=clockwise)
        elif face == 'L':
            self.rotate_L(clockwise=clockwise)
        elif face == 'R':
            self.rotate_R(clockwise=clockwise)
        elif face == 'M':
            # middle slice
            self.rotate_M(clockwise=clockwise)
        else:
            raise ValueError(f"Unknown move: {mv}")

    def generate_scramble(self, moves: int = 20):
        """Generate a scramble sequence of legal single-face quarter turns.

        Rules applied:
        - Moves are chosen from the six faces U,D,F,B,L,R with optional prime (') suffix.
        - Do not repeat the same face twice in a row (that's allowed on a real cube but
          usually avoided in scramble notation).
        Returns the list of move strings.
        """
        faces = ['U', 'D', 'F', 'B', 'L', 'R']
        suffixes = ['', "'"]
        seq = []
        prev_face = None
        for _ in range(moves):
            choice = random.choice(faces) if prev_face is None else random.choice([f for f in faces if f != prev_face])
            suf = random.choice(suffixes)
            mv = choice + suf
            seq.append(mv)
            prev_face = choice
        return seq

    def reset(self):
        """Reset the cube to the solved state."""
        # Reinitialize sides to their original colors
        self.__init__()

    def display(self):
        # Simple text-based visualization of the cube in a net layout
        U = self.sides['U'].grid
        D = self.sides['D'].grid
        F = self.sides['F'].grid
        B = self.sides['B'].grid
        L = self.sides['L'].grid
        R = self.sides['R'].grid
        def row_to_str(row):
            return ' '.join(row)
        print('      ' + row_to_str(U[0]))
        print('      ' + row_to_str(U[1]))
        print('      ' + row_to_str(U[2]))
        for i in range(3):
            print(row_to_str(L[i]) + ' ' + row_to_str(F[i]) + ' ' + row_to_str(R[i]) + ' ' + row_to_str(B[i]))
        print('      ' + row_to_str(D[0]))
        print('      ' + row_to_str(D[1]))
        print('      ' + row_to_str(D[2]))

if __name__ == "__main__":
    cube = Cube()
    print("Initial state:")
    cube.display()
    cube.rotate_U()
    print("\nAfter U rotation:")
    cube.display()
    cube.rotate_F(clockwise=False)
    print("\nAfter F' rotation:")
    cube.display()