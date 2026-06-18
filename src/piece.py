# piece.py
# 2904691
# 2025-08-13
# Description: Piece classes for the Khet game.


class Piece:
    def __init__(self, symbol, owner, k, m, n):
        self.symbol = symbol
        self.owner = owner
        self.k = k
        self.m = m
        self.n = n
        self.is_alive = True
        self.front = None

    def get_front(self):
        pass

    def get_k(self):
        return self.k

    def get_m(self):
        return self.m

    def get_n(self):
        return self.n

    def set_coords(self, k, m, n):
        self.k = k
        self.m = m
        self.n = n

    def can_move(self, k, m, n):
        return False

    def rotate(self, direction):
        pass

    def is_mirror_piece(self):
        return False

    def destroy_piece(self):
        self.is_alive = False

    def hit_by_lazer(self, incoming_direction):
        return "continue"

    def reflect_direction(self, incoming_direction):
        return None

    def get_incoming_face(self, direction):
        opposite = {
            'N': 'S',
            'S': 'N',
            'E': 'W',
            'W': 'E',
            'UP': 'DOWN',
            'DOWN': 'UP',
        }
        return opposite.get(direction, None)

    def __str__(self):
        return f"({self.symbol},{self.owner})"


class Pharaoh(Piece):
    def __init__(self, symbol, owner, k, m, n):
        super().__init__(symbol, owner, k, m, n)

    def can_move(self, k, m, n):
        if k != self.k:
            return False
        check_y = m == self.m or m == self.m - 1 or m == self.m + 1
        check_x = n == self.n or n == self.n + 1 or n == self.n - 1
        not_new_pos = self.n == n and self.m == m and self.k == k

        if check_x and check_y and not not_new_pos:
            return True
        else:
            return False

    def hit_by_lazer(self, incoming_direction):
        if incoming_direction == 'UP':
            return "immune"
        self.is_alive = False
        return "destroy"


class Sphinx(Piece):
    def __init__(self, symbol, owner, k, m, n):
        super().__init__(symbol, owner, k, m, n)
        self.front = self.set_front(symbol)

    def get_front(self):
        return self.front

    def set_front(self, symb):
        if symb == '▲':
            return 'N'
        elif symb == '▼':
            return 'S'
        elif symb == '◀':
            return 'W'
        elif symb == '▶':
            return 'E'
        else:
            return None

    def rotate(self, direction):
        rotate_cw = {'▲': '▶', '▶': '▼',  '▼': '◀', '◀': '▲'}
        rotate_ac = {'▲': '◀', '◀': '▼',  '▼': '▶', '▶': '▲'}

        if direction == 'C':
            self.symbol = rotate_cw[self.symbol]
        if direction == 'A':
            self.symbol = rotate_ac[self.symbol]
        self.front = self.set_front(self.symbol)

    def hit_by_lazer(self, incoming_direction):
        return "immune"


class Anubis(Piece):
    def __init__(self, symbol, owner, k, m, n):
        super().__init__(symbol, owner, k, m, n)
        self.front = self.set_front(symbol)

    def set_front(self, symbol_anubis):
        if symbol_anubis == '△':
            return 'N'
        elif symbol_anubis == '▽':
            return 'S'
        elif symbol_anubis == '◁':
            return 'W'
        elif symbol_anubis == '▷':
            return 'E'
        else:
            return None

    def rotate(self, direction):
        rotate_cw = {"△": "▷", "▷": "▽", "▽": "◁", "◁": "△"}
        rotate_ac = {"△": "◁", "▷": "△", "▽": "▷", "◁": "▽"}

        if direction == 'C':
            self.symbol = rotate_cw[self.symbol]
        if direction == 'A':
            self.symbol = rotate_ac[self.symbol]
        self.front = self.set_front(self.symbol)

    def can_move(self, k, m, n):
        check_y = m == self.m or m == self.m - 1 or m == self.m + 1
        check_x = n == self.n or n == self.n + 1 or n == self.n - 1
        check_z = k == self.k or k == self.k + 1 or k == self.k - 1
        not_new_pos = self.n == n and self.m == m and self.k == k

        if check_x and check_y and check_z and not not_new_pos:
            return True
        else:
            return False

    def hit_by_lazer(self, incoming_direction):
        incoming_face = self.get_incoming_face(incoming_direction)
        if incoming_face == self.front or incoming_face == 'DOWN':
            return "immune"
        else:
            self.is_alive = False
            return "destroy"


class Pyramid(Piece):
    def __init__(self, symbol, owner, k, m, n):
        super().__init__(symbol, owner, k, m, n)

    def is_mirror_piece(self):
        return True

    def rotate(self, direction):
        rotate_cw = {'┐': '┘', '┘': '└', '└': '┌', '┌': '┐'}
        rotate_ac = {'┐': '┌', '┌': '└', '└': '┘', '┘': '┐'}

        if direction == 'C':
            self.symbol = rotate_cw[self.symbol]

        if direction == 'A':
            self.symbol = rotate_ac[self.symbol]

    def can_move(self, k, m, n):
        check_y = m == self.m or m == self.m - 1 or m == self.m + 1
        check_x = n == self.n or n == self.n + 1 or n == self.n - 1
        check_z = k == self.k or k == self.k + 1 or k == self.k - 1
        not_new_pos = self.n == n and self.m == m and self.k == k

        if check_x and check_y and check_z and not not_new_pos:
            return True
        else:
            return False

    reflection_map = {
        '┌': {'S': 'E', 'E': 'S'},
        '┐': {'S': 'W', 'W': 'S'},
        '└': {'N': 'E', 'E': 'N'},
        '┘': {'N': 'W', 'W': 'N'},
    }

    def hit_by_lazer(self, incoming_direction):
        if incoming_direction in ('UP', 'DOWN'):
            self.is_alive = False
            return "destroy"

        incoming_face = self.get_incoming_face(incoming_direction)
        if incoming_face in Pyramid.reflection_map.get(self.symbol, {}):
            return "reflect"

        self.is_alive = False
        return "destroy"

    def reflect_direction(self, incoming_direction):
        incoming_face = self.get_incoming_face(incoming_direction)
        return str(Pyramid.reflection_map[self.symbol][incoming_face])


class Scarab(Piece):
    def __init__(self, symbol, owner, k, m, n):
        super().__init__(symbol, owner, k, m, n)

    def is_mirror_piece(self):
        return True

    def rotate(self, direction):
        rotate_cw = {'╃': '╄', '╄': '╆', '╆': '╅', '╅': '╃'}
        rotate_ac = {'╃': '╅', '╅': '╆', '╆': '╄', '╄': '╃'}

        if direction == 'C':
            self.symbol = rotate_cw[self.symbol]
        if direction == 'A':
            self.symbol = rotate_ac[self.symbol]

    def can_move(self, k, m, n):
        check_y = m == self.m or m == self.m - 1 or m == self.m + 1
        check_x = n == self.n or n == self.n + 1 or n == self.n - 1
        check_z = k == self.k or k == self.k + 1 or k == self.k - 1
        not_new_pos = self.n == n and self.m == m and self.k == k

        if check_x and check_y and check_z and not not_new_pos:
            return True
        else:
            return False

    reflection_map = {
        '╃': {'N': 'W', 'S': 'E', 'E': 'S', 'W': 'N'},
        '╄': {'N': 'E', 'S': 'W', 'E': 'N', 'W': 'S'},
        '╅': {'N': 'E', 'S': 'W', 'E': 'N', 'W': 'S'},
        '╆': {'N': 'W', 'S': 'E', 'E': 'S', 'W': 'N'}
    }

    def hit_by_lazer(self, incoming_direction):
        if incoming_direction in ('UP', 'DOWN'):
                self.is_alive = False
                return "destroy"
        return "reflect"

    def reflect_direction(self, incoming_direction):
        incoming_face = self.get_incoming_face(incoming_direction)
        return Scarab.reflection_map[self.symbol][incoming_face]


class VerticalMirrorUp(Piece):
    def __init__(self, symbol, owner, k, m, n):
        super().__init__(symbol, owner, k, m, n)
        self.front = self.set_front(symbol)

    def is_mirror_piece(self):
        return True

    def set_front(self, symbol_up_mirror):
        if symbol_up_mirror == '⬅':
            return 'W'
        elif symbol_up_mirror == '➡':
            return 'E'
        elif symbol_up_mirror == '⬆':
            return 'N'
        elif symbol_up_mirror == '⬇':
            return 'S'
        else:
            return None

    def rotate(self, direction):
        rotate_cw = {'⬅': '⬆', '⬆': '➡', '➡': '⬇', '⬇': '⬅'}
        rotate_ac = {'⬆': '⬅', '⬅': '⬇', '⬇': '➡', '➡': '⬆'}

        if direction == 'C':
            self.symbol = rotate_cw[self.symbol]
        if direction == 'A':
            self.symbol = rotate_ac[self.symbol]
        self.front = self.set_front(self.symbol)

    def can_move(self, k, m, n):
        check_y = m == self.m or m == self.m - 1 or m == self.m + 1
        check_x = n == self.n or n == self.n + 1 or n == self.n - 1
        check_z = k == self.k or k == self.k + 1 or k == self.k - 1
        not_new_pos = self.n == n and self.m == m and self.k == k

        if check_x and check_y and check_z and not not_new_pos:
            return True
        else:
            return False

    def hit_by_lazer(self, incoming_direction):
        incoming_face = self.get_incoming_face(incoming_direction)

        if incoming_direction in ('N', 'S', 'E', 'W'):
            if incoming_face == self.front:
                return "reflect_up"
            self.is_alive = False
            return "destroy"

        if incoming_direction == "DOWN":
            return "exit_horizontal"

        if incoming_direction == 'UP':
            self.is_alive = False
            return "destroy"

        self.is_alive = False
        return "destroy"


class VerticalMirrorDown(Piece):
    def __init__(self, symbol, owner, k, m, n):
        super().__init__(symbol, owner, k, m, n)
        self.front = self.set_front(symbol)

    def is_mirror_piece(self):
        return True

    def set_front(self, symbol_down_mirror):
        if symbol_down_mirror == '⇦':
            return 'W'
        elif symbol_down_mirror == '⇨':
            return 'E'
        elif symbol_down_mirror == '⇧':
            return 'N'
        elif symbol_down_mirror == '⇩':
            return 'S'
        else:
            return None

    def rotate(self, direction):
        rotate_cw = {'⇦': '⇧', '⇧': '⇨', '⇨': '⇩', '⇩': '⇦'}
        rotate_ac = {'⇧': '⇦', '⇦': '⇩', '⇩': '⇨', '⇨': '⇧'}

        if direction == 'C':
            self.symbol = rotate_cw[self.symbol]
        if direction == 'A':
            self.symbol = rotate_ac[self.symbol]
        self.front = self.set_front(self.symbol)

    def can_move(self, k, m, n):
        check_y = m == self.m or m == self.m - 1 or m == self.m + 1
        check_x = n == self.n or n == self.n + 1 or n == self.n - 1
        check_z = k == self.k or k == self.k + 1 or k == self.k - 1
        not_new_pos = self.n == n and self.m == m and self.k == k

        if check_x and check_y and check_z and not not_new_pos:
            return True
        else:
            return False

    def hit_by_lazer(self, incoming_direction):
        incoming_face = self.get_incoming_face(incoming_direction)

        if incoming_direction in ('N', 'S', 'E', 'W'):
            if incoming_face == self.front:
                return "reflect_down"
            self.is_alive = False
            return "destroy"

        if incoming_direction == "UP":
            return "exit_horizontal"

        if incoming_direction == 'DOWN':
            self.is_alive = False
            return "destroy"

        self.is_alive = False
        return "destroy"
