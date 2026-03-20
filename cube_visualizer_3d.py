"""Simple 3D-ish visualizer for the Cube using pygame and a software projection.

Controls:
  - Left mouse drag: rotate cube
  - SPACE: scramble (20 moves)
  - R: reset to solved
  - Q / ESC: quit

This avoids extra native-OpenGL dependencies by projecting 3D vertices to 2D
and drawing filled polygons with painter's sorting.
"""
import math
import random
import pygame
from cube3 import Cube


COLORS = {
    'W': (255, 255, 255),
    'Y': (255, 255, 0),
    'G': (0, 180, 0),
    'B': (0, 0, 200),
    'O': (255, 140, 0),
    'R': (200, 0, 0),
}


def rotate_point(pt, yaw, pitch):
    """Rotate a 3D point (x,y,z) by yaw (around y) and pitch (around x)."""
    x, y, z = pt
    # yaw (y axis)
    cosy = math.cos(yaw)
    siny = math.sin(yaw)
    x2 = x * cosy - z * siny
    z2 = x * siny + z * cosy
    # pitch (x axis)
    cosp = math.cos(pitch)
    sinp = math.sin(pitch)
    y3 = y * cosp - z2 * sinp
    z3 = y * sinp + z2 * cosp
    return (x2, y3, z3)


class Cube3DVisualizer:
    def __init__(self, cube: Cube, size=600):
        pygame.init()
        self.size = size
        self.screen = pygame.display.set_mode((size, size))
        pygame.display.set_caption('Rubik\'s Cube 3D Visualizer')
        self.clock = pygame.time.Clock()
        self.cube = cube

        # angles
        self.yaw = -0.6
        self.pitch = -0.4

        # mouse drag
        self.dragging = False
        self.last_mouse = (0, 0)

        # camera distance
        self.dist = 4.5

        # precompute sticker quads for a unit cube
        self.sticker_quads = []  # list of tuples (face_key, (r,c), [v0..v3])
        self._build_sticker_quads()

    def _face_axes(self, face):
        # returns (center, u_axis, v_axis) for face in local cube coords
        if face == 'F':
            return ((0, 0, 1), (1, 0, 0), (0, -1, 0))
        if face == 'B':
            return ((0, 0, -1), (-1, 0, 0), (0, -1, 0))
        if face == 'U':
            return ((0, 1, 0), (1, 0, 0), (0, 0, -1))
        if face == 'D':
            return ((0, -1, 0), (1, 0, 0), (0, 0, 1))
        if face == 'L':
            return ((-1, 0, 0), (0, 0, -1), (0, -1, 0))
        if face == 'R':
            return ((1, 0, 0), (0, 0, 1), (0, -1, 0))

    def _build_sticker_quads(self):
        # Each face spans from -1..1 in its local u/v coords. Stickers are 3x3.
        step = 2.0 / 3.0
        half = step / 2.0
        faces = ['U', 'D', 'F', 'B', 'L', 'R']
        for face in faces:
            center, u_axis, v_axis = self._face_axes(face)
            for r in range(3):
                for c in range(3):
                    # offset from face center to sticker center
                    u = (c - 1) * step
                    v = (r - 1) * step
                    # compute sticker center
                    cx = center[0] + u * u_axis[0] + v * v_axis[0]
                    cy = center[1] + u * u_axis[1] + v * v_axis[1]
                    cz = center[2] + u * u_axis[2] + v * v_axis[2]
                    # corners (in u/v local)
                    corners = []
                    for du in (-half, half):
                        for dv in (-half, half):
                            x = center[0] + (u + du) * u_axis[0] + (v + dv) * v_axis[0]
                            y = center[1] + (u + du) * u_axis[1] + (v + dv) * v_axis[1]
                            z = center[2] + (u + du) * u_axis[2] + (v + dv) * v_axis[2]
                            corners.append((x, y, z))
                    # order corners to make a quad (tl, tr, br, bl) in screen space after projection
                    # current corners order is [(-half,-half), (-half,half), (half,-half), (half,half)] due to loops; reorder
                    quad = [corners[0], corners[2], corners[3], corners[1]]
                    self.sticker_quads.append((face, (r, c), quad))

    def project(self, pt):
        x, y, z = pt
        # apply rotations
        xr, yr, zr = rotate_point((x, y, z), self.yaw, self.pitch)
        # perspective
        zc = zr + self.dist
        if zc == 0:
            zc = 0.0001
        f = 400 / zc
        sx = self.size / 2 + xr * f
        sy = self.size / 2 + yr * f
        return (sx, sy, zc)

    def draw(self):
        self.screen.fill((30, 30, 30))

        # build list of polygons with depth
        polygons = []
        for face, (r, c), quad in self.sticker_quads:
            proj = [self.project(rotate_point(p, 0, 0)) for p in quad]
            # compute average depth
            avg_z = sum(p[2] for p in proj) / 4.0
            # map face sticker color
            color = COLORS.get(self.cube.get_sticker(face, r, c), (128, 128, 128))
            points = [(p[0], p[1]) for p in proj]
            polygons.append((avg_z, points, color))

        # painter's sort: draw farthest first
        polygons.sort(key=lambda x: x[0], reverse=True)
        for depth, pts, color in polygons:
            pygame.draw.polygon(self.screen, color, pts)
            pygame.draw.polygon(self.screen, (10, 10, 10), pts, 1)

        # overlay text
        font = pygame.font.SysFont(None, 20)
        lines = ["U/D/R/L/F/B: moves  |  +Shift: inverse  |  SPACE: scramble  |  0: reset  |  Q/ESC: quit"]
        for i, ln in enumerate(lines):
            surf = font.render(ln, True, (220, 220, 220))
            self.screen.blit(surf, (10, 10 + i * 18))

        pygame.display.flip()

    def apply_move(self, mv: str):
        # Delegate to Cube.apply_move for correctness
        self.cube.apply_move(mv)

    def animate_scramble(self, moves=20, delay_ms=120):
        seq = self.cube.scramble(moves)
        for mv in seq:
            self.cube.apply_move(mv)
            self.cube.log_state()
            self.draw()
            pygame.time.delay(delay_ms)

    def run(self):
        running = True
        while running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    if ev.button == 1:
                        self.dragging = True
                        self.last_mouse = ev.pos
                elif ev.type == pygame.MOUSEBUTTONUP:
                    if ev.button == 1:
                        self.dragging = False
                elif ev.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        mx, my = ev.pos
                        lx, ly = self.last_mouse
                        dx = mx - lx
                        dy = my - ly
                        self.yaw += dx * 0.01
                        self.pitch += dy * 0.01
                        self.last_mouse = ev.pos
                elif ev.type == pygame.KEYDOWN:
                    shift = ev.mod & pygame.KMOD_SHIFT
                    # (no-shift move, shift move) — corrected for the
                    # z-axis flip between cube3 (+z=B) and visualizer (+z=F).
                    move_keys = {
                        pygame.K_u: ("U'", "U"),
                        pygame.K_d: ("D'", "D"),
                        pygame.K_r: ("R'", "R"),
                        pygame.K_l: ("L'", "L"),
                        pygame.K_f: ("B'", "B"),
                        pygame.K_b: ("F'", "F"),
                    }
                    if ev.key in move_keys:
                        normal, shifted = move_keys[ev.key]
                        self.cube.apply_move(shifted if shift else normal)
                        self.cube.log_state()
                    elif ev.key == pygame.K_SPACE:
                        self.animate_scramble(20, delay_ms=80)
                    elif ev.key == pygame.K_0:
                        self.cube = Cube()
                        self.cube.log_state()
                    elif ev.key == pygame.K_q or ev.key == pygame.K_ESCAPE:
                        running = False

            self.draw()
            self.clock.tick(30)

        pygame.quit()


def main():
    cube = Cube()
    try:
        viz = Cube3DVisualizer(cube, size=700)
    except Exception as e:
        print("Could not initialize visualizer (likely headless).", e)
        return
    viz.run()


if __name__ == '__main__':
    main()
