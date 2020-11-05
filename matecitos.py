#!/usr/bin/env python3

import chess

def matecitos(depth=4):
    b = chess.Board()
    matecitos = []
    n = 0

    def _aux(b, level=0):
        nonlocal n
        if level == depth:
            n += 1
            if b.is_checkmate():
                print(b)
                matecitos.append(b.copy())
        else:
            for m in b.legal_moves:
                b.push(m)
                _aux(b, level=level+1)
                b.pop()
    _aux(b)
    return matecitos, n


def forest(board, depth=2, copy=False):
    '''
    Generator over all board configurations.
    '''
    for move in board.legal_moves:
        board.push(move)
        if depth == 1:
            yield board.copy() if copy else board
        else:
            yield from forest(board, depth=depth-1, copy=copy)
        board.pop()

#   def forest2(board, depth=2):
#       if depth == 0:
#           yield board.copy()
#       else:
#           for move in board.legal_moves:
#               board.push(move)
#               yield from forest2(board, depth=depth-1)
#               board.pop
#   # AssertionError: push() expects move to be pseudo-legal
