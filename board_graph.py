
from chess.svg import board as board2svg
from cairosvg import svg2png
from graphviz import Digraph
from pathlib import Path
import networkx as nx
from hashlib import md5
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
from contextlib import contextmanager
import chess
import requests
import requests_cache
import time

requests_cache.install_cache('lichess_cache')

LICHESS_API = 'https://explorer.lichess.ovh/'
LICHESS_RETRIES = 10

def lichess(fen, moves=0, topGames=0, cat='master'):
    # cat may be 'lichess'
    ratings = 'ratings[]=1600&ratings[]=1800&ratings[]=2000&ratings[]=2200&ratings[]=2500'
    speeds = 'speeds[]=blitz&speeds[]=rapid&speeds[]=classical'
    url = LICHESS_API + f'{cat}?variant=standard&{speeds}&{ratings}&moves={moves}&topGames={topGames}&recentGames=0&fen={fen}'
    try:
        good = False
        r = LICHESS_RETRIES
        while not good and r > 0:
            resp = requests.get(url)
            r -= 1
            if resp.status_code == 429:
                print(resp)
                print('waiting one minute...')
                time.sleep(61)
            else:
                good = True
    except:
        print(url)
        raise

    try:
        json = resp.json()
    except:
        print(resp)
        raise

    return json


class BoardGraph:
    def __init__(self, png_cache=Path('png_cache')):
        self.png_cache = png_cache
        self.png_cache.mkdir(exist_ok=True)
        self.board = chess.Board()
        self.dg = nx.DiGraph(bgcolor='bisque')
        self.depth = 0
        node_id = self.position_id()
        self.dg.add_node(node_id, title='Ajedrez Clásico', games=[])
        self.initial_position = self.dg.nodes[node_id]
        self.initial_position['year'] = '~6 AD'
        self.initial_position['comment'] = 'Al principio, la infinitud del juego<br/>'
        self.initial_position['comment'] += 'hace imposible imaginar todos los<br/>'
        self.initial_position['comment'] += 'futuros posibles.<br/>'
        self.initial_position['subtitles'] = []
        self.initial_position['fen'] = self.board.fen()
        self.save_png()

    def save_svg(self, path):
        A = to_agraph(self.dg)
        A.layout('dot') # 'twopi' 'circo' 'fdp'
        A.draw(str(path))

    def save_png(self):
        node_id = self.position_id()
        node = self.dg.nodes[node_id]
        png_path = self.png_cache.joinpath(node_id + '.png')
        if self.board.is_checkmate():
            if self.board.result() == '1-0':
                check_square = self.board.king(color=chess.BLACK)
                node['fillcolor'] = 'white'
                node['style'] = 'filled'
                node['fontcolor'] = 'black'
            else:
                check_square = self.board.king(color=chess.WHITE)
                node['fillcolor'] = 'black'
                node['style'] = 'filled'
                node['fontcolor'] = 'white'
        else:
            check_square = None

        svg = board2svg(self.board,
                        arrows=node.get('arrows', []),
                        check=check_square)
        svg2png(bytestring=svg, write_to=str(png_path))
        node['shape'] = 'none'
        title = node.get('title', '')
        year = node.get('year', '????')
        comment = node.get('comment', '')
        subtitles = node.get('subtitles', [])
        node['label'] = f'<<table cellspacing=\"0\" border=\"0\" cellborder=\"1\">' + \
                             f'<tr><td>{title}</td></tr>'

        if len(subtitles) % 2 != 0:
            subtitles.append('')

        for a, b in zip(subtitles[::2], subtitles[1::2]):
            node['label'] += f'<tr><td>{a}: {b}</td></tr>'

        print(f'hiting lichess for ' + ': '.join( [node["title"]] + node['subtitles']))
        resp = lichess(node['fen'])
        # print(resp)
        w = resp['white']
        b = resp['black']
        d = resp['draws']
        t = w + b + d
        if t > 0:
            node['label'] += f'<tr><td>Master Games: W: {100*w/t:3.0f}% B: {100*b/t:3.0f}% D: {100*d/t:3.0f}%</td></tr>'

        resp = lichess(node['fen'], cat='lichess')
        # print(resp)
        w = resp['white']
        b = resp['black']
        d = resp['draws']
        t = w + b + d
        if t > 0:
            node['label'] += f'<tr><td>Lichess Games: W: {100*w/t:3.0f}% B: {100*b/t:3.0f}% D: {100*d/t:3.0f}%</td></tr>'

        node['label'] += \
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

    def push(self, move_san, subtitle=None):
        current_id = self.position_id()
        current_node = self.dg.nodes[current_id]

        move = self.board.parse_san(move_san)
        try:
            self.board.push_san(move_san)
        except:
            print(self.board.move_stack)
            raise
        self.depth += 1
        new_id = self.position_id()
        self.dg.add_node(new_id, arrows=[(move.from_square, move.to_square)])
        self.dg.add_edge(current_id, new_id, label=' ' + move_san)
        node = self.dg.nodes[new_id]
        node['games'] = []
        node['title'] = current_node['title']
        node['subtitles'] = current_node['subtitles'].copy()
        node['fen'] = self.board.fen()

        if subtitle:
            node['subtitles'].append(subtitle)
        return node

    def pop(self):
        self.depth -= 1
        return self.board.pop()

    @contextmanager
    def pushed_to(self, move_san, subtitle=None):
        try:
            yield self.push(move_san, subtitle=subtitle)
            self.save_png()
        finally:
            self.pop()
