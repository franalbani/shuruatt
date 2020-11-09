import chess
from chess.svg import board as board2svg
from cairosvg import svg2png
from graphviz import Digraph
from hashlib import md5
from pathlib import Path
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
from contextlib import contextmanager


CACHE = Path('.png_cache/')
CACHE.mkdir(exist_ok=True)


class BoardGraph:
    def __init__(self):
        self.board = chess.Board()
        self.dg = nx.DiGraph()

        node_id = self.position_id()
        self.dg.add_node(node_id, label='Initial')
        self.save_png()

    def save_svg(self, path):
        A = to_agraph(self.dg)
        A.layout('dot')
        A.draw(path)

    def save_png(self):
        node_id = self.position_id()
        node = self.dg.nodes[node_id]
        png_path = CACHE.joinpath(node_id + '.png')
        svg = board2svg(self.board, arrows=node.get('arrows', []))
        svg2png(bytestring=svg, write_to=str(png_path))
        node['image'] = str(png_path)
        node['shape'] = 'square'
        node['imagepos'] = 'c'
        node['labelloc'] = 't'
        node['height'] = 6
        
    def position_id(self):
        return md5(repr(self.board).encode('utf8')).hexdigest()

    @contextmanager
    def pushed_to(self, move_san, label=''):
        try:
            current_id = self.position_id()
            move = self.board.parse_san(move_san)
            self.board.push_san(move_san)
            new_id = self.position_id()
            self.dg.add_node(new_id, label=label, arrows=[(move.from_square, move.to_square)])
            self.dg.add_edge(current_id, new_id, label=' ' + move_san)
            yield self.dg.nodes[new_id]
            arrows = self.dg.nodes[new_id]['arrows']
            self.save_png()
        finally:
            self.board.pop()
 

bg = BoardGraph()

with bg.pushed_to('e4', "King's Pawn") as position:
    position['comment'] = 'Whites takes control of the center'
    position['arrows'].append(chess.svg.Arrow(chess.E4, chess.D5, color='red'))
    position['arrows'].append(chess.svg.Arrow(chess.E4, chess.F5, color='red'))

    with bg.pushed_to('e5', 'Open game') as position:
        with bg.pushed_to('Nf3', "King's Knight") as position:
            with bg.pushed_to('Nf6', "Petrov's Defense"):
                with bg.pushed_to('Nxe5', '...'):
                    with bg.pushed_to('Nxe4', 'Russian game: ¡¡Cuidado!!!'):
                        pass
            with bg.pushed_to('Nc6', "King's Knight: Normal variation"):
                with bg.pushed_to('Bc4', 'Italian game'):
                    with bg.pushed_to('Bc5', 'Italian game: Giuoco Piano'):
                        with bg.pushed_to('b4', "Italian game: Evan's Gambit"):
                            pass
                    with bg.pushed_to('Nf6', 'Italian game: Two Knights Defense'):
                        with bg.pushed_to('Ng5', 'Italian game: Two Knights Defense & Knight Attack'):
                            with bg.pushed_to('d5', 'Italian game: Two Knights Defense & Knight Attack: Normal variation'):
                                with bg.pushed_to('exd5', '...'):
                                    with bg.pushed_to('Nxd5', '...'):
                                        with bg.pushed_to('Nxf7', 'Italian game: Fried Liver attack'):
                                            pass
                with bg.pushed_to('Bb5', 'Ruy Lopez'):
                    pass
                with bg.pushed_to('d4', 'Scotch Game'):
                    pass
            with bg.pushed_to('d6', "Philidor's Defense"):
                pass

with bg.pushed_to('d4', "Queen's Pawn"):
    with bg.pushed_to('d5', "Closed game"):
        with bg.pushed_to('c4', "Queen's Gambit"):
            with bg.pushed_to('dxc4', "Queen's Gambit accepted"):
                pass
