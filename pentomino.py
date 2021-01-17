from matplotlib import pyplot as plt
import numpy as np
import time

Pentomino = {
    'F': [(-1, 1), (-1, 0), (0, 0), (0, -1), (1, 0)],
    'I': [(2, 0), (1, 0), (0, 0), (-1, 0), (-2, 0)],
    'L': [(-3, 0), (-2, 0), (-1, 0), (0, 0), (0, 1)],
    'N': [(-1, 1), (0, 1), (0, 0), (1, 0), (2, 0)],
    'P': [(-1, 1), (-1, 0), (0, 1), (0, 0), (1, 0)],
    'T': [(-1, -1), (-1, 0), (-1, 1), (0, 0), (1, 0)],
    'U': [(-1, -1), (0, -1), (0, 0), (0, 1), (-1, 1)],
    'V': [(-2, 0), (-1, 0), (0, 0), (0, 1), (0, 2)],
    'W': [(-1, -1), (0, -1), (0, 0), (1, 0), (1, 1)],
    'X': [(1, 0), (0, 0), (-1, 0), (0, 1), (0, -1)],
    'Y': [(-1, 0), (0, 0), (0, -1), (1, 0), (2, 0)],
    'Z': [(-1, -1), (-1, 0), (0, 0), (1, 0), (1, 1)]
}


Symmetries = {
    'F': (True, 4),
    'I': (False, 2),
    'L': (True, 4),
    'N': (True, 4),
    'P': (True, 4),
    'T': (False, 4),
    'U': (False, 4),
    'V': (False, 4),
    'W': (False, 4),
    'X': (False, 1),
    'Y': (True, 4),
    'Z': (True, 2)
}


def put_on_board(board, figure, trans, v):
    shift = np.array(trans)
    for c in figure:
        s = np.array(c) + shift
        board[tuple(s)] = v


def generate_symmetries(figure):
    fig = Pentomino[figure][:]
    res = []
    rot = np.array([[0, -1], [1, 0]])
    sym = np.array([[-1, 0], [0, 1]])
    need_mirror, rots = Symmetries[figure]
    for i in range(rots):
        fig = [rot @ p for p in fig]
        res.append(fig)
    if need_mirror:
        sym_fig = [sym @ p for p in fig]
        res.append(sym_fig)
        for i in range(rots - 1):
            sym_fig = [rot @ p for p in sym_fig]
            res.append(sym_fig)
    return res


def fits_board(board, figure, pos):
    sh = board.shape
    for p in figure:
        s = p+pos
        if s[0] < 0 or s[1] < 0 or s[0] >= sh[0] or s[1] >= sh[1]:
            return False
        if board[tuple(p + pos)] != 0:
            return False
    return True


def find_tiling_rec(board, remaining_figures, placed):
    if len(remaining_figures) == 0 or placed*5 == board.shape[0] * board.shape[1]:
        plt.matshow(board)
        plt.show()
        return

    bs = board.shape
    fs = generate_symmetries(remaining_figures[0])
    rem = remaining_figures[1:]
    for f in fs:
        for i in range(bs[0]):
            for j in range(bs[1]):
                if board[i, j] != 0:
                    continue
                if fits_board(board, f, np.array((i, j))):
                    put_on_board(board, f, (i, j), len(remaining_figures))
                    find_tiling_rec(board, rem, placed+1)
                    put_on_board(board, f, (i, j), 0)


def find_tiling(board_size, figures):
    if board_size[0]*board_size[1] > len(figures)*5:
        return []

    board = np.zeros(board_size, dtype='int')
    find_tiling_rec(board, figures, 0)
    return board


def main():
    board_size = (5, 5)
    t = time.time()
    board = find_tiling(board_size, ['L', 'Y', 'T', 'P', 'W', 'Z', 'V', 'N'])
    t = time.time() - t
    print('Elapsed time:', t)
    plt.matshow(board)
    plt.show()
    '''    
    board_size = (12, 5)
    t = time.time()
    board = find_tiling(board_size, ['F', 'I', 'L', 'N', 'P', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
    t = time.time() - t
    print('Elapsed time:', t)
    plt.matshow(board)
    plt.show()
    '''

if __name__ == '__main__':
    main()
