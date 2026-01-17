import chess
import chess.pgn

import os
from state import State


def get_dataset(num_samples=None):
    X, Y = [], []
    gn = 0
    for fn in os.listdir('data'):
        pgn = open(os.path.join('data', fn))
        while 1:
            try:
                game = chess.pgn.read_game(pgn)
            except Exception:
                break

            print("parsing game %d, got examples %d" % (gn, len(X)))
            gn += 1
            value = {'1/2-1/2':0, '0-1':-1, '1-0':1}[game.headers['Result']]
            board = game.board()
            for i, move in enumerate(game.mainline_moves()):
                board.push(move)
                ser = State(board).serialize()[:, :, 0]
                X.append(ser)
                Y.append(value)
            if len(X) > 50000:
                return X, Y

if __name__ == '__main__':
    X, Y = get_dataset()