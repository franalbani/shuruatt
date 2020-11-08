import chess
from chess.svg import board as board2svg
from cairosvg import svg2png
from graphviz import Digraph
from hashlib import md5
from pathlib import Path


CACHE = Path('.png_cache/')
CACHE.mkdir(exist_ok=True)


class BoardGraph:
    def __init__(self):
        self.board = chess.Board()
        self.dg = Digraph()
        self._add_node_from_position('Initial')

    def position_id(self):
        return md5(repr(self.board).encode('utf8')).hexdigest()

    def _add_node_from_position(self, name):
        node_id = self.position_id()
        png = CACHE.joinpath(node_id + '.png')
        self.save_png()
        self.dg.node(node_id, label='', image=str(png), shape='rect', xlabel=name)
        return node_id

    def save_png(self):
        svg = board2svg(self.board)
        node_id = self.position_id()
        png = CACHE.joinpath(node_id + '.png')
        svg2png(bytestring=svg, write_to=str(png))

    def push(self, move, name):
        assert move in self.board.legal_moves
        father_id = self.position_id()
        self.board.push(move)
        node_id = self._add_node_from_position(name)
        self.dg.edge(father_id, node_id, label=' ' + str(move))

    def pop(self):
        return self.board.pop()

from contextlib import contextmanager

@contextmanager
def line(bg, move, name):
    try:
        yield bg.push(chess.Move.from_uci(move), name)
    finally:
        bg.pop()

bg = BoardGraph()

with line(bg, 'e2e4', "King's Pawn"):
    with line(bg, 'e7e5', 'Open game'):
        with line(bg, 'g1f3', "King's Knight"):
            with line(bg, 'g8f6', "Petrov's Defense"):
                with line(bg, 'f3e5', '...'):
                    with line(bg, 'f6e4', 'Russian game: ¡¡Cuidado!!!'):
                        pass
            with line(bg, 'b8c6', "King's Knight: Normal variation"):
                with line(bg, 'f1c4', 'Italian game'):
                    with line(bg, 'f8c5', 'Italian game: Giuoco Piano'):
                        with line(bg, 'b2b4', "Italian game: Evan's Gambit"):
                            pass
                with line(bg, 'f1b5', 'Ruy Lopez'):
                    pass
                with line(bg, 'd2d4', 'Scotch Game'):
                    pass
            with line(bg, 'd7d6', "Philidor's Defense"):
                pass

with line(bg, 'd2d4', "Queen's Pawn"):
    with line(bg, 'd7d5', "Closed game"):
        with line(bg, 'c2c4', "Queen's Gambit"):
            with line(bg, 'd5c4', "Queen's Gambit accepted"):
                pass
