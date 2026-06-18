# manager.py
# 2904691
# 2025-08-13
# Description: Manager for Khet game: I/O, rules, moves, draw tracking.

from pathlib import Path
import re

from cube import Cube
from piece import (
    Piece,
    Pharaoh,
    Sphinx,
    Anubis,
    Pyramid,
    Scarab,
    VerticalMirrorDown,
    VerticalMirrorUp,
)
from outstream import OutStream
from instream import InStream
from error import *
from lazer import Lazer


MOVE_PATTERN = (
    r"^\((\d{1,2}),(\d{1,2}),(\d{1,2})\)"
    r"(C|A|M\((\d{1,2}),(\d{1,2}),(\d{1,2})\))F?$|^q$"
)


class Manager:
    def __init__(self, filename):
        self._file = filename
        self._n = None
        self._m = None
        self._k = None
        self.cube = None
        self.game_over = False
        self.winner = None

        self.enable_draw = False
        self.draw_indices = None
        self.state_index = 0
        self.state_counts = {}
        self.state_occurrences = {}


    def _clone_cube(self):
        c = Cube(self._k, self._m, self._n)
        for k in range(self._k):
            for m in range(self._m):
                for n in range(self._n):
                    s = str(self.cube.get_cell(k, m, n))
                    p = self.parse_piece(s, k, m, n)
                    c.set_cell(k, m, n, p)
        return c

    def _apply_move_on(self, cube, move):
        m = re.match(MOVE_PATTERN, move)
        x1, y1, z1 = map(int, m.group(1, 2, 3))
        action = m.group(4)
        p1 = cube.get_cell(z1, y1, x1)

        if action in ("C", "A"):
            p1.rotate(action)
            cube.set_cell(z1, y1, x1, p1)
            return

        x2, y2, z2 = map(int, m.group(5, 6, 7))
        p2 = cube.get_cell(z2, y2, x2)

        k1, m1, n1 = p1.get_k(), p1.get_m(), p1.get_n()
        k2, m2, n2 = z2, y2, x2

        if isinstance(p1, Scarab) and (
            isinstance(p2, Anubis) or p2.is_mirror_piece()
        ):
            cube.set_cell(k2, m2, n2, p1)
            cube.set_cell(k1, m1, n1, p2)
            p1.set_coords(k2, m2, n2)
            p2.set_coords(k1, m1, n1)
        else:
            cube.set_cell(k1, m1, n1, p2)
            cube.set_cell(k2, m2, n2, p1)
            p1.set_coords(k2, m2, n2)
            p2.set_coords(k1, m1, n1)



    def find_forced_win_depth1(self) -> bool:
        owner = 'A'
        pattern_rot = ("C", "A")

        for k in range(self._k):
            for m in range(self._m):
                for n in range(self._n):
                    p = self.cube.get_cell(k, m, n)
                    if getattr(p, "owner", None) == owner and p.symbol != '.':
                        src = f"({n},{m},{k})"
                        for r in pattern_rot:
                            mv = f"{src}{r}F"
                            if self.check_move(mv, owner, emit_errors=False):
                                cube2 = self._clone_cube()
                                self._apply_move_on(cube2, mv)
                                sph = cube2.get_player_sphinx(owner)
                                laser = Lazer(cube2, sph)
                                hit = laser.fire()
                                if (
                                    hit and isinstance(hit, Pharaoh) and
                                    hit.owner == 'B'
                                ):
                                    return True
        for k in range(self._k):
            for m in range(self._m):
                for n in range(self._n):
                    p = self.cube.get_cell(k, m, n)
                    if getattr(p, "owner", None) == owner and p.symbol != '.':
                        src = f"({n},{m},{k})"
                        for dk in (-1, 0, 1):
                            for dm in (-1, 0, 1):
                                for dn in (-1, 0, 1):
                                    if dk == dm == dn == 0:
                                        continue
                                    k2 = k + dk
                                    m2 = m + dm
                                    n2 = n + dn
                                    if (
                                        0 <= k2 < self._k and
                                        0 <= m2 < self._m and
                                        0 <= n2 < self._n
                                    ):
                                        dst = f"({n2},{m2},{k2})"
                                        mv = f"{src}M{dst}F"
                                        if self.check_move(
                                            mv, owner, emit_errors=False
                                        ):
                                            cube2 = self._clone_cube()
                                            self._apply_move_on(cube2, mv)
                                            sph = cube2.get_player_sphinx(
                                                owner
                                            )
                                            laser = Lazer(cube2, sph)
                                            hit = laser.fire()
                                            if (
                                                hit and
                                                isinstance(hit, Pharaoh) and
                                                hit.owner == 'B'
                                            ):
                                                return True
        return False

    def set_enable_draw(self, bbool):
        self.enable_draw = bbool

    def _state_string(self) -> str:
        return self.generate_initial_state_string()

    def get_draw_result(self):
        if self.draw_indices is None:
            return None
        i, j, k = self.draw_indices
        return (
            "Game ended in draw due to repetition of game state "
            f"{i}, {j}, {k}"
        )

    def _record_state(self, state_str: str) -> None:
        if state_str in self.state_counts:
            self.state_counts[state_str] += 1
        else:
            self.state_counts[state_str] = 1
        if state_str in self.state_occurrences:
            self.state_occurrences[state_str].append(self.state_index)
        else:
            self.state_occurrences[state_str] = [self.state_index]


    def readFile(self):
        file_path = Path(self._file).resolve()
        if not file_path.exists():
            self.write_error_to_outfile(
                self._file,
                NO_CONFIG_FILE.format(config_file_path=self._file),
                True,
            )

        instream = InStream(str(file_path))

        line1 = instream.readLine()
        cells = line1.strip().split(',')
        if len(cells) != 3:
            self.write_error_to_outfile(
                self._file,
                INVALID_DIMENSIONS,
                True,
            )
        else:
            self._n = int(cells[0])
            self._m = int(cells[1])
            self._k = int(cells[2])

        line2 = instream.readLine()
        if line2 != "":
            self.write_error_to_outfile(
                self._file,
                NO_EMPTY_LINE,
                True,
            )

        file = instream.readAll()
        lines = file.splitlines()
        num_lines = len(lines) + 3
        expected_lines = (self._m + 2) * self._k + 2

        if num_lines != expected_lines:
            self.write_error_to_outfile(
                self._file,
                INVALID_LINE_COUNT.format(
                    expectedLineCount=expected_lines,
                    trueLineCount=num_lines,
                ),
                True,
            )

        self.cube = Cube(self._k, self._m, self._n)
        track = 0
        for k in range(self._k):
            layer_header = lines[track]
            if layer_header != f"Layer {k}:":
                self.write_error_to_outfile(
                    self._file,
                    INVALID_LAYER_HEADER.format(
                        lineNumber=track + 3, layerIndex=k
                    ),
                    True,
                )
            track += 1

            for m in range(self._m):
                current_row = lines[track]
                cells = current_row.strip().split(' ')

                if len(cells) != self._n:
                    self.write_error_to_outfile(
                        self._file,
                        INVALID_ROW_FORMAT.format(
                            layerIndex=k, rowIndex=m
                        ),
                        True,
                    )
                else:
                    for n in range(self._n):
                        s = cells[n]
                        if (
                            s[0] != "(" or
                            s[len(s) - 1] != ")" or
                            s[2] != ","
                        ):
                            self.write_error_to_outfile(
                                self._file,
                                INVALID_ROW_FORMAT.format(
                                    layerIndex=k, rowIndex=m
                                ),
                                True,
                            )
                        else:
                            piece1 = self.parse_piece(s, k, m, n)
                            self.cube.set_cell(k, m, n, piece1)
                track += 1

            track += 1

        player_A_sphinx = 0
        player_B_sphinx = 0
        for l in range(self._k):
            for r in range(self._m):
                for c in range(self._n):
                    cell = str(self.cube.get_cell(l, r, c))
                    cell1 = cell[1]
                    cell2 = cell[3]

                    if cell1 in ("▲", "▼", "◀", "▶"):
                        if l != 0:
                            self.write_error_to_outfile(
                                self._file,
                                INVALID_SPHINX_LAYER.format(layerIndex=l),
                                True,
                            )
                        else:
                            if cell2 == 'A':
                                player_A_sphinx += 1
                            if cell2 == 'B':
                                player_B_sphinx += 1

        if player_A_sphinx != 1 or player_B_sphinx != 1:
            self.write_error_to_outfile(
                self._file,
                INVALID_SPHINX_COUNT,
                True,
            )

        pharaoh1 = 0
        pharaoh2 = 0
        for l in range(self._k):
            for r in range(self._m):
                for c in range(self._n):
                    cell = str(self.cube.get_cell(l, r, c))
                    cell1 = cell[1]

                    if cell1 == "♚":
                        pharaoh1 += 1
                        if l != (self._k - 1):
                            self.write_error_to_outfile(
                                self._file,
                                INVALID_PHARAOH_LAYER.format(layerIndex=l),
                                True,
                            )

                    if cell1 == '♔':
                        pharaoh2 += 1
                        if l != (self._k - 1):
                            self.write_error_to_outfile(
                                self._file,
                                INVALID_PHARAOH_LAYER.format(layerIndex=l),
                                True,
                            )

        if pharaoh1 != 1 or pharaoh2 != 1:
            self.write_error_to_outfile(
                self._file,
                INVALID_PHARAOH_COUNT,
                True,
            )

        state0 = self._state_string()
        self._record_state(state0)


    def check_move(self, move, owner, emit_errors=True) -> bool:
        match = re.match(MOVE_PATTERN, move)
        if not match:
            if emit_errors:
                self.write_error_to_outfile(
                    self._file, INVALID_PATTERN, False
                )
            return False

        x1, y1, z1 = map(int, match.group(1, 2, 3))
        ok_x1 = 0 <= x1 <= self._n - 1
        ok_y1 = 0 <= y1 <= self._m - 1
        ok_z1 = 0 <= z1 <= self._k - 1
        if not (ok_x1 and ok_y1 and ok_z1):
            if emit_errors:
                self.write_error_to_outfile(
                    self._file,
                    OUT_OF_BOUNDS_SRC.format(encodedMove=move),
                    False,
                )
            return False

        cell_src = self.cube.get_cell(z1, y1, x1)
        cell_src_form = f"({x1},{y1},{z1})"

        if cell_src.symbol == '.':
            if emit_errors:
                self.write_error_to_outfile(
                    self._file,
                    EMPTY_CELL.format(cell=cell_src_form),
                    False,
                )
            return False

        if cell_src.owner != owner:
            owner_num = 1 if owner == 'A' else 2
            if emit_errors:
                self.write_error_to_outfile(
                    self._file,
                    OWNERSHIP_ERROR.format(
                        x=owner_num, cell=cell_src_form
                    ),
                    False,
                )
            return False

        action = match.group(4)
        if action.startswith('M'):
            x2, y2, z2 = map(int, match.group(5, 6, 7))
            ok_x2 = 0 <= x2 <= self._n - 1
            ok_y2 = 0 <= y2 <= self._m - 1
            ok_z2 = 0 <= z2 <= self._k - 1
            if not (ok_x2 and ok_y2 and ok_z2):
                if emit_errors:
                    self.write_error_to_outfile(
                        self._file,
                        OUT_OF_BOUNDS_DST.format(encodedMove=move),
                        False,
                    )
                return False

            cell_dst = self.cube.get_cell(z2, y2, x2)
            cell_dst_form = f"({x2},{y2},{z2})"

            if isinstance(cell_src, Sphinx):
                if emit_errors:
                    self.write_error_to_outfile(
                        self._file,
                        ILLEGAL_MOVEMENT.format(piece=cell_src_form),
                        False,
                    )
                return False

            if isinstance(cell_src, Pharaoh) and not cell_src.can_move(
                z2, y2, x2
            ):
                if emit_errors:
                    self.write_error_to_outfile(
                        self._file,
                        INVALID_PHARAOH_MOVE,
                        False,
                    )
                return False

            if not cell_src.can_move(z2, y2, x2):
                if emit_errors:
                    self.write_error_to_outfile(
                        self._file,
                        NOT_ADJACENT.format(
                            cell1=cell_src_form, cell2=cell_dst_form
                        ),
                        False,
                    )
                return False

            if isinstance(cell_src, Scarab):
                if isinstance(cell_dst, Anubis) or cell_dst.is_mirror_piece():
                    pass
                elif cell_dst.symbol != '.':
                    if emit_errors:
                        self.write_error_to_outfile(
                            self._file,
                            INVALID_SCARAB_SWAP.format(
                                cell1=cell_src_form, cell2=cell_dst_form
                            ),
                            False,
                        )
                    return False
            else:
                if cell_dst.symbol != '.':
                    if emit_errors:
                        self.write_error_to_outfile(
                            self._file,
                            DST_OCCUPIED.format(
                                cell1=cell_src_form, cell2=cell_dst_form
                            ),
                            False,
                        )
                    return False

        return True

    def get_move_type(self, move):
        match = re.match(MOVE_PATTERN, move)
        if move == "q":
            return "Q"
        action = match.group(4)
        lazer = move.endswith("F")
        if action.startswith("M"):
            return "MF" if lazer else "M"
        return "RF" if lazer else "R"

    def get_move_p1(self, move) -> Piece:
        match = re.match(MOVE_PATTERN, move)
        x1, y1, z1 = map(int, match.group(1, 2, 3))
        return self.cube.get_cell(z1, y1, x1)

    def get_move_p2(self, move) -> Piece:
        match = re.match(MOVE_PATTERN, move)
        x2, y2, z2 = map(int, match.group(5, 6, 7))
        return self.cube.get_cell(z2, y2, x2)

    def get_move_direction(self, move):
        match = re.match(MOVE_PATTERN, move)
        return match.group(4)


    def apply_move(self, move, owner):
        if not self.check_move(move, owner):
            return

        mv_type = self.get_move_type(move)

        if mv_type in ("R", "RF"):
            piece = self.get_move_p1(move)
            direction = self.get_move_direction(move)

            piece.rotate(direction)
            n = piece.get_n()
            m = piece.get_m()
            k = piece.get_k()
            self.cube.set_cell(k, m, n, piece)

            if len(mv_type) == 2:
                owner_sphinx = piece.owner
                sphinx_piece = self.cube.get_player_sphinx(owner_sphinx)
                lazer = Lazer(self.cube, sphinx_piece)
                piece_hit = lazer.fire()

                if piece_hit and isinstance(piece_hit, Pharaoh):
                    self.game_over = True
                    self.winner = 2 if piece_hit.owner == 'A' else 1
                elif piece_hit:
                    self.cube.remove_piece(piece_hit)

        if mv_type in ("M", "MF"):
            piece1 = self.get_move_p1(move)
            piece2 = self.get_move_p2(move)

            k1, m1, n1 = piece1.get_k(), piece1.get_m(), piece1.get_n()
            k2, m2, n2 = piece2.get_k(), piece2.get_m(), piece2.get_n()

            if (
                (piece2.is_mirror_piece() or isinstance(piece2, Anubis)) and
                isinstance(piece1, Scarab)
            ):
                self.cube.set_cell(k2, m2, n2, piece1)
                self.cube.set_cell(k1, m1, n1, piece2)
                piece1.set_coords(k2, m2, n2)
                piece2.set_coords(k1, m1, n1)

            elif piece2.symbol == '.':
                self.cube.set_cell(k1, m1, n1, piece2)
                self.cube.set_cell(k2, m2, n2, piece1)
                piece1.set_coords(k2, m2, n2)
                piece2.set_coords(k1, m1, n1)

            if len(mv_type) == 2:
                owner_sphinx = piece1.owner
                sphinx_piece = self.cube.get_player_sphinx(owner_sphinx)
                lazer = Lazer(self.cube, sphinx_piece)
                piece_hit = lazer.fire()

                if piece_hit and isinstance(piece_hit, Pharaoh):
                    self.game_over = True
                    self.winner = 2 if piece_hit.owner == 'A' else 1
                elif piece_hit:
                    self.cube.remove_piece(piece_hit)

        # record / draw detection
        self.state_index += 1
        cur_state = self._state_string()
        self._record_state(cur_state)

        if self.enable_draw and not self.game_over:
            if self.state_counts[cur_state] == 3:
                occ = self.state_occurrences[cur_state]
                i, j, k = occ[0], occ[1], occ[2]
                self.game_over = True
                self.winner = None
                self.draw_indices = (i, j, k)


    def parse_piece(self, value, k, m, n) -> Piece:
        symbol = value[1]
        owner = value[3]

        if symbol in ("♚", "♔"):
            p = Pharaoh(symbol, owner, k, m, n)
        elif symbol in ('▲', '▼', '◀', '▶'):
            p = Sphinx(symbol, owner, k, m, n)
        elif symbol in ('△', '▽', '◁', '▷'):
            p = Anubis(symbol, owner, k, m, n)
        elif symbol in ('┌', '┐', '└', '┘'):
            p = Pyramid(symbol, owner, k, m, n)
        elif symbol in ('╃', '╄', '╅', '╆'):
            p = Scarab(symbol, owner, k, m, n)
        elif symbol in ('⬅', '➡', '⬆', '⬇'):
            p = VerticalMirrorUp(symbol, owner, k, m, n)
        elif symbol in ('⇦', '⇧', '⇩', '⇨'):
            p = VerticalMirrorDown(symbol, owner, k, m, n)
        else:
            p = Piece(symbol, owner, k, m, n)
        return p


    def write_error_to_outfile(self, config_path, message, exitt: bool):
        out_directory = Path(__file__).parent.parent / "out"
        out_directory.mkdir(parents=True, exist_ok=True)

        config_file = Path(config_path)
        if config_file.exists():
            out_file = out_directory / (config_file.stem + ".out")
        else:
            out_file = out_directory / "noConfig.out"

        mode = "a" if out_file.exists() else "w"
        with open(out_file, mode, encoding="utf-8") as outstream:
            outstream.write(message.rstrip("\n") + "\n")

        if exitt is True:
            exit(0)

    def _prepare_outfile(self, config_path):
        out_directory = Path(__file__).parent.parent / "out"
        out_directory.mkdir(parents=True, exist_ok=True)

        config_file = Path(config_path)
        if config_file.exists():
            out_file = out_directory / (config_file.stem + ".out")
        else:
            out_file = out_directory / "noConfig.out"

        with open(out_file, "w", encoding="utf-8"):
            pass
        return out_file

    def generate_initial_state_string(self):
        output_string = ''
        c = self.cube
        for l in range(c._k):
            output_string += f"Layer {l}:\n"
            for r in range(c._m):
                for col in range(c._n):
                    piece = c.get_cell(l, r, col)
                    output_string += str(piece) + " "
                output_string = output_string.rstrip() + '\n'
            output_string += '\n'
        return output_string

    def write_initial_state_to_outfile(self, config_path, output_str):
        out_directory = Path(__file__).parent.parent / "out"
        config_file = Path(config_path)

        if config_file.exists():
            out_file = out_directory / (config_file.stem + ".out")
        else:
            out_file = out_directory / "noConfig.out"

        outstream = OutStream(str(out_file))
        outstream.write(output_str.rstrip() + '\n')
