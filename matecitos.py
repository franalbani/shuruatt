#!/usr/bin/env python3

import chess


def matecitos(depth=4):
    b = chess.Board()
    matecitos = []

    def _aux(b, level=0):
        if level == depth:
            if b.is_checkmate():
                print(b)
                matecitos.append(b.copy())
        else:
            for m in b.legal_moves:
                b.push(m)
                _aux(b, level=level+1)
                b.pop()
    _aux(b)
    return matecitos
