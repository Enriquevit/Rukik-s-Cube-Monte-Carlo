import sys
import random
import time

import pygame

from cube3 import Cube


# Simple 2D net visualizer for the Cube class using pygame
# Controls:
#   SPACE - scramble (animated)
#   R     - reset cube to solved
#   M     - apply a single random move
#   Q/ESC - quit


COLORS = {
    'W': (255, 255, 255),
    'Y': (255, 255, 0),
    'G': (0, 180, 0),
    'B': (0, 0, 200),
    'O': (255, 140, 0),
    'R': (200, 0, 0),
}


class Visualizer:
    def __init__(self, cube: Cube, square=40, margin=10):
        self.cube = cube
        self.square = square
        self.margin = margin

        # net layout (face -> (grid_x, grid_y) in 3x3 face coordinates)
        # we'll draw a 12x9 grid where each face is 3x3
        self.face_positions = {
            'U': (3, 0),
            'L': (0, 3),
            'F': (3, 3),
            'R': (6, 3),
            'B': (9, 3),
            'D': (3, 6),
        }

        grid_w = 12 * self.square
        grid_h = 9 * self.square
        self.width = grid_w + self.margin * 2
        self.height = grid_h + self.margin * 2 + 40

        pygame.init()
        try:
            self.screen = pygame.display.set_mode((self.width, self.height))
        except pygame.error as e:
            print("Could not open a display for pygame. If you're running headless, try running locally with a GUI.")
            raise
        pygame.display.set_caption('Rubik\'s Cube Visualizer')
        self.font = pygame.font.SysFont(None, 20)

    def draw_face(self, face_grid, origin_x, origin_y):
        for r in range(3):
            for c in range(3):
                color_key = face_grid[r][c]
                color = COLORS.get(color_key, (128, 128, 128))
                x = origin_x + c * self.square
                y = origin_y + r * self.square
                rect = pygame.Rect(x, y, self.square, self.square)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

    def draw(self):
        self.screen.fill((40, 40, 40))
        # draw each face at its position
        for face, pos in self.face_positions.items():
            gx, gy = pos
            ox = self.margin + gx * self.square
            oy = self.margin + gy * self.square
            face_grid = [[self.cube.get_sticker(face, r, c) for c in range(3)] for r in range(3)]
            self.draw_face(face_grid, ox, oy)

        # draw instructions
        lines = [
            "SPACE: scramble (20 moves)",
            "M: single random move",
            "R: reset",
            "Q / ESC: quit",
        ]
        for i, line in enumerate(lines):
            surf = self.font.render(line, True, (230, 230, 230))
            self.screen.blit(surf, (self.margin, self.height - 30 + i * 12))

        pygame.display.flip()

    def animate_scramble(self, moves=20, delay=0.12):
        seq = self.cube.scramble(moves)
        for mv in seq:
            # use the cube's apply_move so the cube logic is authoritative
            self.cube.apply_move(mv)
            self.draw()
            pygame.time.delay(int(delay * 1000))

    def apply_move(self, mv: str):
        # Delegate to cube.apply_move to ensure consistent legal-turn logic
        self.cube.apply_move(mv)


def main():
    cube = Cube()
    viz = None
    try:
        viz = Visualizer(cube)
    except Exception:
        # Initialization failed (likely headless). Exit gracefully.
        print("Visualizer cannot run in this environment. The cube logic still works — try running this script on your machine with a GUI.")
        return

    clock = pygame.time.Clock()
    viz.draw()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    viz.animate_scramble(moves=20, delay=0.12)
                elif event.key == pygame.K_r:
                    cube = Cube()
                    viz.cube = cube
                    viz.draw()
                elif event.key == pygame.K_m:
                    mv = random.choice(['U', "U'", 'D', "D'", 'F', "F'", 'B', "B'", 'L', "L'", 'R', "R'"])
                    viz.apply_move(mv)
                    viz.draw()
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    main()
