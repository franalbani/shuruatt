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

    def _add_node_from_position(self, name, arrow=None):
        node_id = self.position_id()
        png = CACHE.joinpath(node_id + '.png')
        self.save_png(arrow)
        self.dg.node(node_id, label=name, image=str(png), shape='square', imagepos='c', labelloc='t', height='6')
        return node_id

    def save_png(self, arrow=None):
        svg = board2svg(self.board, arrows=[arrow] if arrow else [])
        node_id = self.position_id()
        png = CACHE.joinpath(node_id + '.png')
        svg2png(bytestring=svg, write_to=str(png))

    def push(self, move, name):
        san_move = bg.board.parse_san(move)
        assert san_move in self.board.legal_moves
        father_id = self.position_id()
        self.board.push_san(move)
        node_id = self._add_node_from_position(name, arrow=chess.svg.Arrow(san_move.from_square, san_move.to_square))
        self.dg.edge(father_id, node_id, label=' ' + move)

    def pop(self):
        return self.board.pop()

from contextlib import contextmanager

@contextmanager
def line(bg, move, name):
    try:
        yield bg.push(move, name)
    finally:
        bg.pop()

bg = BoardGraph()

with line(bg, 'e4', "King's Pawn") as l:
    
    with line(bg, 'e5', 'Open game'):
        with line(bg, 'Nf3', "King's Knight"):
            with line(bg, 'Nf6', "Petrov's Defense"):
                with line(bg, 'Nxe5', '...'):
                    with line(bg, 'Nxe4', 'Russian game: ¡¡Cuidado!!!'):
                        pass
            with line(bg, 'Nc6', "King's Knight: Normal variation"):
                with line(bg, 'Bc4', 'Italian game'):
                    with line(bg, 'Bc5', 'Italian game: Giuoco Piano'):
                        with line(bg, 'b4', "Italian game: Evan's Gambit"):
                            pass
                    with line(bg, 'Nf6', 'Italian game: Two Knights Defense'):
                        with line(bg, 'Ng5', 'Italian game: Two Knights Defense & Knight Attack'):
                            with line(bg, 'd5', 'Italian game: Two Knights Defense & Knight Attack: Normal variation'):
                                with line(bg, 'exd5', '...'):
                                    with line(bg, 'Nxd5', '...'):
                                        with line(bg, 'Nxf7', 'Italian game: Fried Liver attack'):
                                            pass
                with line(bg, 'Bb5', 'Ruy Lopez'):
                    pass
                with line(bg, 'd4', 'Scotch Game'):
                    pass
            with line(bg, 'd6', "Philidor's Defense"):
                pass

with line(bg, 'd4', "Queen's Pawn"):
    with line(bg, 'd5', "Closed game"):
        with line(bg, 'c4', "Queen's Gambit"):
            with line(bg, 'dxc4', "Queen's Gambit accepted"):
                pass
