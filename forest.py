#!/usr/bin/env python3

import chess
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
import requests
import requests_cache
import pickle
from time import sleep
from board_graph import lichess


def grow(forest, board, depth=5, msg=''):
    if depth < 1:
        # print('depth 0 reached')
        return
    sleep(0.01)
    # print(len(forest.nodes))

    fen = board.fen()
    forest.add_node(fen, label='o')
    m = sum(1 for _ in board.legal_moves)

    games = lichess(fen, moves=m)
    total_moves = len(games['moves'])
    total = games['white'] + games['black'] + games['draws']

    for k, move in enumerate(games['moves']):
        new_msg = f'{msg} Pushing move {k+1} of {total_moves} at depth {depth}.')
        print(new_msg)
        board.push_san(move['san'])
        new_fen = board.fen()
        if not new_fen in forest.nodes.keys():
            forest.add_node(new_fen, label='o')
            forest.add_edge(fen, new_fen, label=move['san'])
            grow(forest, board, depth=depth-1, msg=new_msg)
        else:
            print('Transposition!')
            forest.add_edge(fen, new_fen, label=move['san'])
        board.pop()


if __name__ == '__main__':
    requests_cache.install_cache('lichess_cache')

    board = chess.Board()

    try:
        with open('forest.pickle', 'rb') as fp:
            forest = pickle.load(fp)
    except (FileNotFoundError, EOFError):
        forest = nx.DiGraph(rankdir='LR')

        grow(forest, board, depth=4)
    
        with open('forest.pickle', 'wb') as fp:
            pickle.dump(forest, fp)

    nx.set_node_attributes(forest, 'black', 'fillcolor')
    nx.set_node_attributes(forest, 'filled', 'style')
    nx.set_node_attributes(forest, 'circle', 'shape')

    print('Saving svg...')
    ag = to_agraph(forest)
    ag.layout('dot') # 'twopi' 'circo' 'fdp'
    ag.draw('forest.svg')

    from IPython import embed
    embed(header1='', colors='linux', confirm_exit=False)

