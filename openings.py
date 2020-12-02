import chess
from chess.pgn import read_game
from pathlib import Path
from board_graph import BoardGraph


bg = BoardGraph(png_cache=Path('png_cache'))


with bg.pushed_to('e4', "King's Pawn") as p:
    p['comment'] = 'Blancas toma control del centro<br/>y abre las diagonales para la Dama y el alfil f'
    # p['arrows'].append(chess.svg.Arrow(chess.E4, chess.D5, color='red'))
    # p['arrows'].append(chess.svg.Arrow(chess.E4, chess.F5, color='red'))

    with bg.pushed_to('e5', 'Open game') as p:
        p['comment'] = 'Negras reclama su parte del centro<br/>y también abre las diagonales'

        with bg.pushed_to('Qf3', "Napoleon's opening") as p:
            pass

        with bg.pushed_to('Qh5', "Parham's opening") as p:
            pass

        with bg.pushed_to('Bc4', "Bishop's opening") as p:
            p['comment'] = 'Blancas ataca al peón débil en f7.<br/>Esta apertura es útil para llegar<br/>al Italian Game sin permitir Petrov'
            p['arrows'].append(chess.svg.Arrow(chess.C4, chess.F7, color='red'))

            with bg.pushed_to('Nc6') as p:
                p['comment'] = 'Negras ignora la amenaza y defiende e5,<br/>que no está atacado aún.'
                p['arrows'].append(chess.svg.Arrow(chess.C6, chess.E5, color='yellow'))

                with bg.pushed_to('Qh5') as p:
                    p['comment'] = 'Blancas aprovecha y prepara un mate en 1 en f7'
                    p['arrows'].append(chess.svg.Arrow(chess.H5, chess.F7, color='red'))
                    p['arrows'].append(chess.svg.Arrow(chess.C4, chess.F7, color='red'))

                    with bg.pushed_to('Nf6') as p:
                        p['comment'] = 'Negras ataca a la dama.'
                        p['arrows'].append(chess.svg.Arrow(chess.F6, chess.H5, color='red'))

                        with bg.pushed_to('Qxf7', "Scholar's mate / Mate del pastor") as p:
                            p['comment'] = 'Jaque mate. Gana Blancas'

            with bg.pushed_to('Nf6', 'Berlin Defense') as p:
                p['comment'] = 'Negras ignora la amenaza, evita Qh5,<br/> bloquea Qf3 y ataca a e5,<br/>que no está defendido aún.'
                p['arrows'].append(chess.svg.Arrow(chess.F6, chess.E4, color='red'))
                p['arrows'].append(chess.svg.Arrow(chess.F6, chess.H5, color='yellow'))
                with bg.pushed_to('d4', 'Ponziani Gambit') as p:
                    p['comment'] = 'Blancas no descansa y ofrece un peón<br/>a cambio de...'

        with bg.pushed_to('Nf3', "King's Knight") as p:
            p['comment'] = 'Blancas amenaza el peón e5'
            p['arrows'].append(chess.svg.Arrow(chess.F3, chess.E5, color='red'))
            with bg.pushed_to('Nf6', "Petrov's Defense") as p:
                p['comment'] = 'Contrariamente a su nombre,<br/>negras contrataca e4 sin defender e5'
                p['arrows'].append(chess.svg.Arrow(chess.F6, chess.E4, color='red'))
                with bg.pushed_to('Nxe5', "Clasical variation") as p:
                    p['comment'] = 'Blancas aprovecha la ventaja de tempo.<br/>'
                    with bg.pushed_to('Nxe4', 'Russian game: Damiano variation') as p:
                        p['fillcolor'] = 'yellow'
                        p['style'] = 'filled'
                        with bg.pushed_to('Qe2') as p:
                            p['comment'] = 'Blancas finge un ataque al caballo'
                            p['arrows'].append(chess.svg.Arrow(chess.E2, chess.E4, color='red'))
                            with bg.pushed_to('Nf6') as p:
                                p['comment'] = 'Habiendo saciado su sed,<br/>Negras regresa el caballo.'
                                #p['arrows'].append(chess.svg.Arrow(chess.E2, chess.E4, color='red'))
                                with bg.pushed_to('Nc6', 'Copycat trap') as p:
                                    p['comment'] = 'Jaque descubierto. Cualquier respuesta de Negras<br/> pierde la dama.'
                                    p['arrows'].append(chess.svg.Arrow(chess.C6, chess.D8, color='red'))
                                    p['arrows'].append(chess.svg.Arrow(chess.E2, chess.E8, color='red'))
                                    p['fillcolor'] = 'red'
                                    p['style'] = 'filled'
                    with bg.pushed_to('d6') as p:
                        p['comment'] = 'Negras no cede ante la tentación Nxe4 y echa al caballo'
                        p['arrows'].append(chess.svg.Arrow(chess.D6, chess.E5, color='red'))
                        with bg.pushed_to('Nxf7', 'Cochrane Gambit') as p:
                            p['comment'] = 'Blancas no tiene marcha atrás'
                            with bg.pushed_to('Kxf7') as p:
                                p['comment'] = 'Negras no tiene alternativa que salvar a la torre<br/>renunciando al derecho de enrrocarse.'
                                with bg.pushed_to('d4', 'Center variation') as p:
                                    p['comment'] = 'Blancas aprovecha que negras tiene mucho en su plato<br/>e incluso le tienta a Nxe4.'
                                    with bg.pushed_to('Nxe4') as p:
                                        p['fillcolor'] = 'red'
                                        p['style'] = 'filled'
                                        p['comment'] = 'Negras cae en la trampa.'
                                        with bg.pushed_to('Qh5') as p:
                                            p['comment'] = 'Blancas dará una serie de jaques que<br/> irremediablemente terminan en Qxe4.'
                    with bg.pushed_to('Nc6', 'Stafford Gambit') as p:
                        with bg.pushed_to('Nxc6', 'Stafford Gambit Accepted') as p:
                            with bg.pushed_to('dxc6') as p:
                                p['comment'] = 'A partir de aquí se posibilitan varias trampas,<br/>dependiendo de la respuesta Blancas.'
                                with bg.pushed_to('d3') as p:
                                    with bg.pushed_to('Bc5') as p:
                                        with bg.pushed_to('Bg5') as p:
                                            with bg.pushed_to('Nxe4') as p:
                                                p['comment'] = 'Negras ofrece la dama.'
                                                with bg.pushed_to('Bxd8') as p:
                                                    p['comment'] = 'Blancas no lo piensa dos veces.<br/>El mate en 2 es inevitable.'
                                                    with bg.pushed_to('Bxf2') as p:
                                                        with bg.pushed_to('Ke2') as p:
                                                            with bg.pushed_to('Bg4') as p:
                                                                pass
                                                with bg.pushed_to('Be3') as p:
                                                    p['comment'] = 'Blancas vio el horror;<br/>regresa.'
                                                    with bg.pushed_to('Bxe3') as p:
                                                        with bg.pushed_to('fxe3') as p:
                                                            with bg.pushed_to('Qh4') as p:
                                                                with bg.pushed_to('g3') as p:
                                                                    with bg.pushed_to('Nxg3') as p:
                                                                        with bg.pushed_to('hxg3') as p:
                                                                            with bg.pushed_to('Qxh1') as p:
                                                                                pass
                                                with bg.pushed_to('Qe2') as p:
                                                    with bg.pushed_to('Qxg5') as p:
                                                        with bg.pushed_to('Qxe4') as p:
                                                            with bg.pushed_to('Kd8') as p:
                                                                p['comment'] = 'Negras sale del jaque dejando lugar<br/>para que la torre fije la dama al rey.'
                                                                with bg.pushed_to('Be2') as p:
                                                                    p['comment'] = 'Blancas intenta neutralizar Re8...'
                                                                    with bg.pushed_to('Qc1') as p:
                                                                        with bg.pushed_to('Bd1') as p:
                                                                            with bg.pushed_to('Re8') as p:
                                                                                p['comment'] = 'Blancas pierde la dama.'
                                        with bg.pushed_to('Nc3') as p:
                                            pass
                                        with bg.pushed_to('h3') as p:
                                            with bg.pushed_to('Bxf2') as p:
                                                with bg.pushed_to('Kxf2') as p:
                                                    with bg.pushed_to('Nxe4') as p:
                                                        with bg.pushed_to('Kg1') as p:
                                                            with bg.pushed_to('Qd4') as p:
                                                                p['comment'] = 'Blancas puede forzar tablas.'

                                with bg.pushed_to('e5') as p:
                                    with bg.pushed_to('Ne4') as p:
                                        with bg.pushed_to('d3') as p:
                                            with bg.pushed_to('Bc5') as p:
                                                with bg.pushed_to('dxe4') as p:
                                                    with bg.pushed_to('Bxf2') as p:
                                                        with bg.pushed_to('Kxf2') as p:
                                                            with bg.pushed_to('Qxd1') as p:
                                                                pass
                                                        with bg.pushed_to('Ke2') as p:
                                                            with bg.pushed_to('Bg4') as p:
                                                                p['comment'] = 'Blancas pierde la dama.'
                                        with bg.pushed_to('d4') as p:
                                            with bg.pushed_to('Qh4') as p:
                                                with bg.pushed_to('g3') as p:
                                                    with bg.pushed_to('Nxg3') as p:
                                                        with bg.pushed_to('fxg3') as p:
                                                            with bg.pushed_to('Qe4') as p:
                                                                p['comment'] = 'Blancas pierde la torre.'
                                                                p['arrows'].append(chess.svg.Arrow(chess.E4, chess.H1, color='red'))
                                with bg.pushed_to('Nc3') as p:
                                    with bg.pushed_to('Bc5') as p:
                                        with bg.pushed_to('d3') as p:
                                            with bg.pushed_to('Ng4') as p:
                                                with bg.pushed_to('Be3') as p:
                                                    with bg.pushed_to('Nxe3') as p:
                                                        with bg.pushed_to('fxe3') as p:
                                                            with bg.pushed_to('Bxe3') as p:
                                                                p['comment'] = 'El alfil domina.'
                                                                p['arrows'].append(chess.svg.Arrow(chess.E3, chess.G1, color='green'))
                                                                p['arrows'].append(chess.svg.Arrow(chess.E3, chess.C1, color='green'))
                                        with bg.pushed_to('Bc4') as p:
                                            with bg.pushed_to('Ng4') as p:
                                                with bg.pushed_to('O-O') as p:
                                                    with bg.pushed_to('Qh4') as p:
                                                        with bg.pushed_to('h3') as p:
                                                            with bg.pushed_to('Nxf2') as p:
                                                                with bg.pushed_to('Qf3') as p:
                                                                    with bg.pushed_to('Nxh3') as p:
                                                                        p['comment'] = 'Doble jaque.'
                                                                        with bg.pushed_to('Kh2') as p:
                                                                            with bg.pushed_to('Nf2') as p:
                                                                                pass
                                                                                # SyntaxError: too many statically nested blocks
                                                                                #   with bg.pushed_to('Kg1') as p:
                                                                                #       with bg.pushed_to('Qh1') as p:
                                                                                #           pass
                                                                        with bg.pushed_to('Kh1') as p:
                                                                            with bg.pushed_to('Nf2') as p:
                                                                                pass
                                                                                # SyntaxError: too many statically nested blocks
                                                                                #   with bg.pushed_to('Kg1') as p:
                                                                                #       with bg.pushed_to('Qh1') as p:
                                                                                #           pass
                                                with bg.pushed_to('Qf3') as p:
                                                    with bg.pushed_to('Nxf2') as p:
                                                        with bg.pushed_to('Qxf7') as p:
                                                            pass
                                                    with bg.pushed_to('Ne5') as p:
                                                        p['comment'] = 'Fork dama y alfil'
                                                        p['arrows'].append(chess.svg.Arrow(chess.E5, chess.F3, color='red'))
                                                        p['arrows'].append(chess.svg.Arrow(chess.E5, chess.C4, color='red'))
                                                        with bg.pushed_to('Qe2') as p:
                                                            with bg.pushed_to('Qh4') as p:
                                                                p['comment'] = 'Negras amenaza ganar una pieza con<br/>Bxf2+, Qxf2, Qxf2, Kxf2, Nxc4.<br/>El peón f está clavado al rey,<br/>permitiendo Bg4.'
                                                                with bg.pushed_to('g3') as p:
                                                                    with bg.pushed_to('Qh3') as p:
                                                                        pass
                                        with bg.pushed_to('Be2') as p:
                                            with bg.pushed_to('h5') as p:
                                                with bg.pushed_to('h3') as p:
                                                    with bg.pushed_to('Qd4') as p:
                                                        with bg.pushed_to('O-O') as p:
                                                            with bg.pushed_to('Ng4') as p:
                                                                with bg.pushed_to('hxg4') as p:
                                                                    with bg.pushed_to('hxg4') as p:
                                                                        p['comment'] = 'Negras amenaza Qe5.'
            with bg.pushed_to('Nc6', "Normal variation") as p:
                p['comment'] = 'Negras defiende el peón e5'
                p['arrows'].append(chess.svg.Arrow(chess.C6, chess.E5, color='yellow'))
                with bg.pushed_to('Bc4', 'Italian game') as p:
                    p['comment'] = 'Blancas ataca al peón débil en f7'
                    p['arrows'].append(chess.svg.Arrow(chess.C4, chess.F7, color='red'))

                    ### GIUOCO PIANO
                    with bg.pushed_to('Bc5', 'Giuoco Piano'):
                        with bg.pushed_to('b4', "Evan's Gambit") as p:
                            p['url'] = 'https://en.wikipedia.org/wiki/Evans_Gambit'
                            p['year'] = 1827
                            p['games'] += [(1852, 'Evergreen game')]
                            p['games'] += [(1995, 'Kasparov vs. Anand')]
                            p['comment'] = 'Blancas ofrece un peón para atraer al alfil.'
                            with bg.pushed_to('Nxb4') as p:
                                p['comment'] = 'Negras deja desprotegido e5.'
                                p['style'] = 'filled'
                                p['fillcolor'] = 'yellow'
                            with bg.pushed_to('Bxb4', "Evan's Gambit accepted") as p:
                                p['comment'] = 'La mejor opción de Negras es aceptar el peón.'
                                with bg.pushed_to('c3') as p:
                                    p['comment'] = 'Blancas sacrifió un peón a cambio de un tempo<br/>y control del centro.'
                                    with bg.pushed_to('a5') as p:
                                        with bg.pushed_to('d4') as p:
                                            p['comment'] = 'Con c3 defendido por el caballo<br/>Blancas ataca en el centro.'
                                            with bg.pushed_to('exd4') as p:
                                                p['comment'] = 'Negras aprovecha que c3 está clavado.'
                                                with bg.pushed_to('O-O') as p:
                                                    p['comment'] = 'Blancas gana ventaja en desarrollo<br/>y amenaza cxd4.'

                    ### TWO KNIGHTS DEFENSE
                    with bg.pushed_to('Nf6', 'Two Knights Defense'):
                        with bg.pushed_to('Ng5', 'Knight Attack'):
                            with bg.pushed_to('d5', 'Normal variation') as p:
                                p['comment'] = "Negras quiere evitar el fork de Nxf7.<br/>Razona: bloqueo al alfil y tengo dos defensores de la casilla d5"
                                p['arrows'].append(chess.svg.Arrow(chess.D8, chess.D5, color='yellow'))
                                p['arrows'].append(chess.svg.Arrow(chess.F6, chess.D5, color='yellow'))
                                with bg.pushed_to('exd5') as p:
                                    p['comment'] = "A Blancas a no le importa, pues no tiene<br/>planeado finalizar el intercambio con el alfil"
                                    with bg.pushed_to('Nxd5') as p:
                                        p['comment']  = "Negras continua el intercambio de piezas"
                                        with bg.pushed_to('Nxf7', 'Fried Liver attack') as p:
                                            p['comment'] = 'Blancas sorprende sacrificando un caballo por un peón<br/>a cambio de exponer al rey.'
                                            p['games'] += [(1610, 'Polerio vs. Domenico')]
                                            p['year'] = 1610
                                            with bg.pushed_to('Kxf7') as p:
                                                p['comment'] = 'Negras acepta el reto'
                                                with bg.pushed_to('Qf3') as p:
                                                    p['comment'] = "Blancas muestra sus cartas"
                                                    with bg.pushed_to('Kg8') as p:
                                                        p['comment'] = "El miedo le costó caro a Negras.<br/>El mate en 3 es inevitable"
                                                        p['fillcolor'] = 'white'
                                                        p['style'] = 'filled'
                                                    with bg.pushed_to('Ke6') as p:
                                                        p['comment'] = "La mejor defensa de Negras"
                                                        p['games'] += [(1850, 'Paul Morphy vs. Alonzo Morphy')]
                                                        with bg.pushed_to('Nc3') as p:
                                                            p['comment'] = 'Blancas suma presión al caballo en d5<br/>inmovilizado por el alfil de c4.'
                                                            with bg.pushed_to('Nd4') as p:
                                                                p['comment'] = 'Negras amenaza a la reina y un jaquefork en c2.'
                                                                with bg.pushed_to('Bxd5') as p:
                                                                    p['comment'] = 'Blancas toma el caballo.'
                                                                    with bg.pushed_to('Ke7') as p:
                                                                        p['comment'] = 'Grave error de negras<br/>El mate en 2 es inevitable.'
                                                                        p['fillcolor'] = 'white'
                                                                        p['style'] = 'filled'
                                                    with bg.pushed_to('Qf6') as p:
                                                        p['comment'] = "Negras ofrece un intercambio de reinas"
                                                        with bg.pushed_to('Bxd5') as p:
                                                            p['comment'] = "Blancas no lo acepta porque todavía<br/>puede capturar cosas."
                                                            with bg.pushed_to('Be6') as p:
                                                                with bg.pushed_to('Bxe6') as p:
                                                                    with bg.pushed_to('Kxe6') as p:
                                                                        with bg.pushed_to('Qb3') as p:
                                                                            p['comment'] = "Haga lo que haga Negras, Blancas tomará b7."
                            with bg.pushed_to('Bc5', 'Traxler counter-attack') as p:
                                p['comment'] = "Negras prepara una sorpresa a Nxf7"
                                p['arrows'].append(chess.svg.Arrow(chess.C5, chess.F2, color='red'))
                                with bg.pushed_to('Nxf7') as p:
                                    with bg.pushed_to('Bxf2') as p:
                                        with bg.pushed_to('Kxf2') as p:
                                            with bg.pushed_to('Nxe4') as p:
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
                pass

#   for pgn in Path('./games').glob('*.pgn'):
#       print(f'Reading {pgn}...')
#       with open(pgn) as pgn_data:
#           game = read_game(pgn_data)
#   
#       for k, v in game.headers.items():
#           print(f'{k}:\t{v}')
#   
#       bg.board.reset()
#       # p = bg.initial_position
#       for m in game.mainline_moves():
#           san = bg.board.san(m)
#           # print(f'{m}: {san}')
#           p = bg.push(san)
#   
#       termination = game.headers['Termination']
#       if bg.board.is_checkmate() or 'resignation' in termination:
#           p['title'] = game.headers['White'] + 'vs.' + game.headers['Black']
#           p['year'] = game.headers['Date']
#           p['comment'] = termination
#           p['fillcolor'] = 'white' if game.headers['White'] in termination else 'black'
#           p['style'] = 'filled'
#           print(p)
#           bg.save_png()
#   
#   from chess import H8, H5, C6, A6, Piece, WHITE, BLACK, KING, PAWN
#   
#   bg.board.clear()
#   bg.board.set_piece_at(H8, Piece(KING, WHITE))
#   bg.board.set_piece_at(A6, Piece(KING, BLACK))
#   bg.board.set_piece_at(C6, Piece(PAWN, WHITE))
#   bg.board.set_piece_at(H5, Piece(PAWN, BLACK))
#   with bg.position() as p:
#       p['Title'] = 'Estudio de Reti'
#       p['Depth'] = 0
#       p['year'] = 0
