import chess
from chess.pgn import read_game
from chess.svg import board as board2svg
from cairosvg import svg2png
from graphviz import Digraph
from hashlib import md5
from pathlib import Path
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
from contextlib import contextmanager

CACHE = Path('.png_cache')
CACHE.mkdir(exist_ok=True)


class BoardGraph:
    def __init__(self):
        self.board = chess.Board()
        self.dg = nx.DiGraph(bgcolor='bisque')
        self.depth = 0
        node_id = self.position_id()
        self.dg.add_node(node_id, title='Initial', games=[])
        self.initial_position = self.dg.nodes[node_id]
        self.initial_position['year'] = '~6 AD'
        self.initial_position['comment'] = 'Al principio, la infinitud del juego<br/>'
        self.initial_position['comment'] += 'hace imposible imaginar todos los<br/>'
        self.initial_position['comment'] += 'futuros posibles.<br/>'
        self.save_png()

    def save_svg(self, path):
        A = to_agraph(self.dg)
        A.layout('dot')
        A.draw(str(path))

    def save_png(self):
        node_id = self.position_id()
        node = self.dg.nodes[node_id]
        png_path = CACHE.joinpath(node_id + '.png')
        svg = board2svg(self.board, arrows=node.get('arrows', []))
        svg2png(bytestring=svg, write_to=str(png_path))
        node['shape'] = 'none'
        title = node.get('title', '')
        year = node.get('year', '????')
        comment = node.get('comment', '')
        node['label'] = f'<<table cellspacing=\"0\" border=\"0\" cellborder=\"1\">' + \
                             f'<tr><td>{title}</td></tr>' + \
                             f'<tr><td>Depth: {self.depth}</td></tr>' + \
                             f'<tr><td>Año: {year}</td></tr>' + \
                             f'<tr><td><img src=\"{png_path}\" /></td></tr>' + \
                             f'<tr><td>{comment}</td></tr>'
        url= node.get('url', None)
        if url:
            node['label'] += f'<tr><td href="{url}">Wikipedia</td></tr>'

        games = node['games']
        if games:
            node['label'] += f'<tr><td>Juegos notables:</td></tr>'
            for y, g in games:
                node['label'] += f'<tr><td>{y}: {g}</td></tr>'
        node['label'] += '</table>>'
        
    def position_id(self):
        return md5(repr(self.board).encode('utf8')).hexdigest()

    @contextmanager
    def position(self):
        try:
            current_id = self.position_id()
            self.dg.add_node(current_id)
            node = self.dg.nodes[current_id]
            node['games'] = []
            yield node
        finally:
            self.save_png()

    def push(self, move_san, title=None):
        current_id = self.position_id()
        move = self.board.parse_san(move_san)
        self.board.push_san(move_san)
        self.depth += 1
        new_id = self.position_id()
        self.dg.add_node(new_id, arrows=[(move.from_square, move.to_square)])
        self.dg.add_edge(current_id, new_id, label=' ' + move_san)
        node = self.dg.nodes[new_id]
        node['games'] = []
        self.save_png()
        if title:
            node['title'] = title
        return node

    def pop(self):
        self.depth -= 1
        return self.board.pop()

    @contextmanager
    def pushed_to(self, move_san, title=''):
        try:
            yield self.push(move_san, title=title)
        finally:
            self.pop()


bg = BoardGraph()


with bg.pushed_to('e4', "King's Pawn") as p:
    p['comment'] = 'Blancas toma control del centro<br/>y abre las diagonales para la Dama y el alfil f'
    # p['arrows'].append(chess.svg.Arrow(chess.E4, chess.D5, color='red'))
    # p['arrows'].append(chess.svg.Arrow(chess.E4, chess.F5, color='red'))

    with bg.pushed_to('e5', 'Open game') as p:
        p['comment'] = 'Negras reclama su parte del centro<br/>y también abre las diagonales'

        with bg.pushed_to('Bc4', "Bishop's opening") as p:
            p['comment'] = 'Blancas ataca al peón débil en f7'
            p['arrows'].append(chess.svg.Arrow(chess.C4, chess.F7, color='red'))

            with bg.pushed_to('Nc6', "...") as p:
                p['comment'] = 'Negras ignora la amenaza y defiende e5,<br/>que no está atacado aún'
                p['arrows'].append(chess.svg.Arrow(chess.C6, chess.E5, color='yellow'))

                with bg.pushed_to('Qh5', "...") as p:
                    p['comment'] = 'Blancas aprovecha y prepara un mate en 1 en f7'
                    p['arrows'].append(chess.svg.Arrow(chess.H5, chess.F7, color='red'))
                    p['arrows'].append(chess.svg.Arrow(chess.C4, chess.F7, color='red'))

                    with bg.pushed_to('Nf6', "...") as p:
                        p['comment'] = 'Negras ataca a la dama.'
                        p['arrows'].append(chess.svg.Arrow(chess.F6, chess.H5, color='red'))

                        with bg.pushed_to('Qxf7', "Scholar's mate / Mate del pastor") as p:
                            p['comment'] = 'Jaque mate. Gana Blancas'
                            p['fillcolor'] = 'white'
                            p['style'] = 'filled'

        with bg.pushed_to('Nf3', "King's Knight") as p:
            p['comment'] = 'Blancas amenaza el peón e5'
            p['arrows'].append(chess.svg.Arrow(chess.F3, chess.E5, color='red'))
            with bg.pushed_to('Nf6', "Petrov's Defense") as p:
                p['comment'] = 'Contrariamente a su nombre,<br/>negras contrataca e4 sin defender e5'
                p['arrows'].append(chess.svg.Arrow(chess.F6, chess.E4, color='red'))
                with bg.pushed_to('Nxe5', "Petrov's Defense: Clasical variation") as p:
                    p['comment'] = 'Blancas aprovecha la ventaja de tempo.<br/>'
                    with bg.pushed_to('Nxe4', 'Russian game: Damiano variation') as p:
                        p['fillcolor'] = 'yellow'
                        p['style'] = 'filled'
                        with bg.pushed_to('Qe2', '...') as p:
                            p['comment'] = 'Blancas finge un ataque al caballo'
                            p['arrows'].append(chess.svg.Arrow(chess.E2, chess.E4, color='red'))
                            with bg.pushed_to('Nf6', '...') as p:
                                p['comment'] = 'Habiendo saciado su sed,<br/>Negras regresa el caballo.'
                                #p['arrows'].append(chess.svg.Arrow(chess.E2, chess.E4, color='red'))
                                with bg.pushed_to('Nc6', 'Copycat trap') as p:
                                    p['comment'] = 'Jaque descubierto. Cualquier respuesta de Negras<br/> pierde la dama.'
                                    p['arrows'].append(chess.svg.Arrow(chess.C6, chess.D8, color='red'))
                                    p['arrows'].append(chess.svg.Arrow(chess.E2, chess.E8, color='red'))
                                    p['fillcolor'] = 'red'
                                    p['style'] = 'filled'
                    with bg.pushed_to('d6', '...') as p:
                        p['comment'] = 'Negras no cede ante la tentación Nxe4 y echa al caballo'
                        p['arrows'].append(chess.svg.Arrow(chess.D6, chess.E5, color='red'))
                        with bg.pushed_to('Nxf7', 'Cochrane Gambit') as p:
                            p['comment'] = 'Blancas no tiene marcha atrás'
                            with bg.pushed_to('Kxf7', '...') as p:
                                p['comment'] = 'Negras no tiene alternativa que salvar a la torre<br/>renunciando al derecho de enrrocarse.'
                                with bg.pushed_to('d4', 'Cochrane Gambit: center variation') as p:
                                    p['comment'] = 'Blancas aprovecha que negras tiene mucho en su plato<br/>e incluso le tienta a Nxe4.'
                                    with bg.pushed_to('Nxe4', '...') as p:
                                        p['fillcolor'] = 'red'
                                        p['style'] = 'filled'
                                        p['comment'] = 'Negras cae en la trampa.'
                                        with bg.pushed_to('Qh5', '...') as p:
                                            p['comment'] = 'Blancas dará una serie de jaques que<br/> irremediablemente terminan en Qxe4.'
                            
            with bg.pushed_to('Nc6', "King's Knight: Normal variation") as p:
                p['comment'] = 'Negras defiende el peón e5'
                p['arrows'].append(chess.svg.Arrow(chess.C6, chess.E5, color='yellow'))
                with bg.pushed_to('Bc4', 'Italian game') as p:
                    p['comment'] = 'Blancas ataca al peón débil en f7'
                    p['arrows'].append(chess.svg.Arrow(chess.C4, chess.F7, color='red'))
                    with bg.pushed_to('Bc5', 'Italian game: Giuoco Piano'):
                        with bg.pushed_to('b4', "Italian game: Evan's Gambit") as p:
                            p['url'] = 'https://en.wikipedia.org/wiki/Evans_Gambit'
                            p['year'] = 1827
                            p['games'] += [(1852, 'Evergreen game')]
                            p['games'] += [(1995, 'Kasparov vs. Anand')]
                            p['comment'] = 'Blancas ofrece un peón para atraer al alfil.'
                            with bg.pushed_to('Bxb4', "Italian game: Evan's Gambit accepted") as p:
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
            with bg.pushed_to('d6', "Philidor's Defense") as p:
                p['arrows'].append(chess.svg.Arrow(chess.D6, chess.E5, color='yellow'))

with bg.pushed_to('d4', "Queen's Pawn") as p:
    p['comment'] = 'Blancas toma control del centro<br/>pero sólo le abre paso al alfil c'
    with bg.pushed_to('d5', "Closed game") as p:
        with bg.pushed_to('c4', "Queen's Gambit"):
            with bg.pushed_to('dxc4', "Queen's Gambit accepted"):
                pass

with bg.pushed_to('f3', "f3") as p:
    with bg.pushed_to('e6', "e6") as p:
        with bg.pushed_to('g4', "g4") as p:
            with bg.pushed_to('Qh4', "Fool's mate") as p:
                p['fillcolor'] = 'black'
                p['style'] = 'filled'
                p['fontcolor'] = 'white'


for pgn in Path('./games').glob('*.pgn'):
    print(f'Reading {pgn}...')
    with open(pgn) as pgn_data:
        game = read_game(pgn_data)

    for k, v in game.headers.items():
        print(f'{k}:\t{v}')

    bg.board.reset()
    # p = bg.initial_position
    for m in game.mainline_moves():
        san = bg.board.san(m)
        # print(f'{m}: {san}')
        p = bg.push(san)

    termination = game.headers['Termination']
    if bg.board.is_checkmate() or 'resignation' in termination:
        p['title'] = game.headers['White'] + 'vs.' + game.headers['Black']
        p['year'] = game.headers['Date']
        p['comment'] = termination
        p['fillcolor'] = 'white' if game.headers['White'] in termination else 'black'
        p['style'] = 'filled'
        print(p)
        bg.save_png()

from chess import H8, H5, C6, A6, Piece, WHITE, BLACK, KING, PAWN

bg.board.clear()
bg.board.set_piece_at(H8, Piece(KING, WHITE))
bg.board.set_piece_at(A6, Piece(KING, BLACK))
bg.board.set_piece_at(C6, Piece(PAWN, WHITE))
bg.board.set_piece_at(H5, Piece(PAWN, BLACK))
with bg.position() as p:
    p['Title'] = 'Estudio de Reti'
    p['Depth'] = 0
    p['year'] = 0
