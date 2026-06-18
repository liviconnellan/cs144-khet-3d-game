# lazer.py
# 2904691
# 2025-08-13
# Description: Laser propagation with vertical support
from cube import Cube
from piece import Piece, Sphinx, Pharaoh, Anubis


class Lazer:
    def __init__(self, cube: Cube, sphinx: Sphinx):
        self.cube = cube
        self.sphinx = sphinx
        self.owner = self.sphinx.owner
        self.position = (
            self.sphinx.get_k(),
            self.sphinx.get_m(),
            self.sphinx.get_n()
        )
        self.direction = self.sphinx.get_front()
        self.path = [self.position]
        self.terminated = False
        self.piece_hit = None

    def in_bounds(self, k, m, n):
        return (
            0 <= n < self.cube._n and
            0 <= m < self.cube._m and
            0 <= k < self.cube._k
        )

    def move_one_step(self):
        k, m, n = self.position
        if self.direction == 'N':
            m -= 1
        elif self.direction == 'S':
            m += 1
        elif self.direction == 'E':
            n += 1
        elif self.direction == 'W':
            n -= 1
        elif self.direction == 'UP':
            k += 1
        elif self.direction == 'DOWN':
            k -= 1
        return (k, m, n)

    def fire(self):
        tick = 0
        while not self.terminated:
            self.position = self.move_one_step()
            tick += 1
            k, m, n = self.position

            if not self.in_bounds(k, m, n):
                self.terminated = True
                break

            piece = self.cube.get_cell(k, m, n)

            if piece.symbol == ".":
                self.path.append(self.position)
                continue

            if isinstance(piece, Sphinx):
                self.terminated = True
                break

            if isinstance(piece, Pharaoh):
                outcome = piece.hit_by_lazer(self.direction)
                if outcome == "destroy":
                    piece.destroy_piece()
                    self.piece_hit = piece
                self.terminated = True
                break

            if isinstance(piece, Anubis):
                outcome = piece.hit_by_lazer(self.direction)
                if outcome == "immune":
                    self.terminated = True
                    break
                elif outcome == "destroy":
                    piece.destroy_piece()
                    self.piece_hit = piece
                    self.terminated = True
                    break
                self.terminated = True
                break

            if piece.is_mirror_piece():
                response = piece.hit_by_lazer(self.direction)

                if response == "reflect":
                    self.direction = piece.reflect_direction(self.direction)
                    self.path.append(self.position)
                    continue

                elif response == "reflect_up":
                    self.direction = 'UP'
                    self.path.append(self.position)
                    continue

                elif response == "reflect_down":
                    self.direction = 'DOWN'
                    self.path.append(self.position)
                    continue

                elif response == "exit_horizontal":
                    self.direction = piece.front
                    self.path.append(self.position)
                    continue

                elif response == "immune":
                    self.terminated = True
                    break

                elif response == "destroy":
                    piece.destroy_piece()
                    self.piece_hit = piece
                    self.terminated = True
                    break

                else:
                    self.terminated = True
                    break

            piece.destroy_piece()
            self.piece_hit = piece
            self.terminated = True
            break

        return self.piece_hit
