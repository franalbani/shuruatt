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
        father_id = self.position_id()
        self.board.push(move)
        node_id = self._add_node_from_position(name)
        self.dg.edge(father_id, node_id, label=' ' + str(move))

    def pop(self):
        return self.board.pop()


bg = BoardGraph()

bg.push(chess.Move.from_uci('e2e4'), "King's Pawn")

_m = bg.pop()
bg.push(chess.Move.from_uci('d2d4'), "Queen's Pawn")

bg.pop()

bg.board.push(_m)

bg.push(chess.Move.from_uci('e7e5'), 'Open game')
bg.push(chess.Move.from_uci('g1f3'), "King's Knight")
bg.push(chess.Move.from_uci('g8f6'), "Petrov's Defense")
bg.push(chess.Move.from_uci('f3e5'), '...')
bg.push(chess.Move.from_uci('f6e4'), 'Russian game: ¡¡Cuidado!!!')
bg.pop()
bg.pop()
bg.pop()

bg.push(chess.Move.from_uci('b8c6'), "King's Knight: Normal variation")
bg.push(chess.Move.from_uci('f1c4'), 'Italian game')
bg.push(chess.Move.from_uci('f8c5'), 'Italian game: Giuoco Piano')
bg.push(chess.Move.from_uci('b2b4'), "Italian game: Evan's Gambit")
#   # Scotch Game
#   g.e4.s.e5.s.Nf3.s.Nc3.s.d4.f.ScotchGame(shape='rectangle')
#   
#   # Philidor Defense
#   g.e4.s.e5.s.Nf3.s.d6.f.PhilidorDefense(shape='rectangle')
#   
#   # Ruy López
#   g.e4.s.e5.s.Nf3.s.Nf6.s.Bb5.f.RuyLopez(shape='rectangle')
#   
#   
