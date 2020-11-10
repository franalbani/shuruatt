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
        self.dg = nx.DiGraph(bgcolor='bisque')

        node_id = self.position_id()
        self.dg.add_node(node_id, title='Initial', comment='Infinitos caminos se abren...')
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
        node['shape'] = 'rect'
        title = node['title']
        comment = node.get('comment', '')
        node['label'] = f'<<table cellspacing=\"0\" border=\"0\" cellborder=\"1\">' + \
                             f'<tr><td>{title}</td></tr>' + \
                             f'<tr><td><img src=\"{png_path}\" /></td></tr>' + \
                             f'<tr><td>{comment}</td></tr>' + \
                         '</table>>'
        
    def position_id(self):
        return md5(repr(self.board).encode('utf8')).hexdigest()

    @contextmanager
    def pushed_to(self, move_san, title=''):
        try:
            current_id = self.position_id()
            move = self.board.parse_san(move_san)
            self.board.push_san(move_san)
            new_id = self.position_id()
            self.dg.add_node(new_id, title=title, arrows=[(move.from_square, move.to_square)])
            self.dg.add_edge(current_id, new_id, label=' ' + move_san)
            node = self.dg.nodes[new_id]
            yield node
            self.save_png()
        finally:
            self.board.pop()
 

bg = BoardGraph()

with bg.pushed_to('e4', "King's Pawn") as position:
    position['comment'] = 'Blancas toma control del centro<br/>y abre las diagonales para la Dama y el alfil f'
    # position['arrows'].append(chess.svg.Arrow(chess.E4, chess.D5, color='red'))
    # position['arrows'].append(chess.svg.Arrow(chess.E4, chess.F5, color='red'))

    with bg.pushed_to('e5', 'Open game') as position:
        position['comment'] = 'Negras reclama su parte del centro<br/>y también abre las diagonales'

        with bg.pushed_to('Bc4', "Bishop's opening") as position:
            position['comment'] = 'Blancas ataca al peón débil en f7'
            position['arrows'].append(chess.svg.Arrow(chess.C4, chess.F7, color='red'))

            with bg.pushed_to('Nf6', "...") as position:
                position['comment'] = 'Negras ignora la amenaza y ataca e4'
                position['arrows'].append(chess.svg.Arrow(chess.F6, chess.E4, color='red'))
                position['fillcolor'] = 'yellow'
                position['style'] = 'filled'

                with bg.pushed_to('Qh5', "...") as position:
                    position['comment'] = 'Blancas aprovecha y prepara un mate en 1 en f7'
                    position['arrows'].append(chess.svg.Arrow(chess.H5, chess.F7, color='red'))
                    position['arrows'].append(chess.svg.Arrow(chess.C4, chess.F7, color='red'))

                    with bg.pushed_to('Nxe4', "...") as position:
                        position['comment'] = 'Negras no se dan por aludidas'

                        with bg.pushed_to('Qxf7', "Scholar's mate / Mate del pastor") as position:
                            position['comment'] = 'Jaque mate. Gana Blancas'
                            position['fillcolor'] = 'white'
                            position['style'] = 'filled'

        with bg.pushed_to('Nf3', "King's Knight") as position:
            position['comment'] = 'Whites attacks e5 pawn'
            position['arrows'].append(chess.svg.Arrow(chess.F3, chess.E5, color='red'))
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
                        with bg.pushed_to('Ng5', 'Italian game: Two Knights Defense &amp; Knight Attack'):
                            with bg.pushed_to('d5', 'Italian game: Two Knights Defense &amp; Knight Attack: Normal variation'):
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
