# cube.py
# 2904691
# 2025-08-13
# Description: Contains all piece classes for the Khet game

from piece import Piece, Pharaoh, Scarab, Sphinx


class Cube:
    def __init__(self, k, m, n):
        self._k = k
        self._m = m
        self._n = n

        self._cube = [[[None for x in range(n)]
                       for y in range(m)] for z in range(k)]

    def set_cell(self, k, m, n, value: Piece):
        if 0 <= k < self._k:
            self._cube[k][m][n] = value

    def remove_piece(self, piece: Piece):
        n = piece.get_n()
        m = piece.get_m()
        k = piece.get_k()
        empty = Piece(".", 'N', k, m, n)
        self.set_cell(k, m, n, empty)

    def get_player_sphinx(self, owner) -> Sphinx:
        for k in range(self._k):
            for m in range(self._m):
                for n in range(self._n):
                    piece = self.get_cell(k, m, n)
                    if isinstance(piece, Sphinx) and piece.owner == owner:
                        return piece
        return None

    def get_cell(self, k, m, n) -> Piece:
        if 0 <= k < self._k:
            return self._cube[k][m][n]

    def __str__(self):
        output = ''
        for k in range(self._k):
            output += f"Layer {k}:\n"
            for m in range(self._m):
                row_str = ''
                for n in range(self._n):
                    piece = self._cube[k][m][n]
                    row_str += str(piece) + ' ' if piece else '. '
                output += row_str.rstrip() + '\n'
            output += '\n'
        return output
