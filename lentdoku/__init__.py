from collections import namedtuple

import numpy as np


LU = np.arange(1, 10, dtype=np.uint8)

def possibilites(pmap):
    return LU[pmap]

def calc_quadrant(row: int, col: int):
    return (slice(row // 3 * 3, row // 3 * 3 + 3), slice(col // 3 * 3, col // 3 * 3 + 3))

Move = namedtuple("Move", "poss poss_idx row col")

class Board:
    __slots__ = ("pmap", "poss", "board")

    def __init__(self):
        self.board = np.zeros((9,9), dtype=np.uint8)
        self.pmap = np.ones((9, 9, 9), dtype=np.int8) # (9 * 9 grid of 9 ints) max is 1, min is -2

    def _play_move(self, num: int,  row: int, col: int):
        rq, cq = calc_quadrant(row, col)

        self.pmap[:, col, num - 1] -= 1
        self.pmap[row, :, num - 1] -= 1

        self.pmap[row, cq, num - 1] += 1
        self.pmap[rq, col, num - 1] += 1
        self.pmap[rq, cq, num - 1] -= 1

        self.board[row, col] = num

    def play_move(self, move: Move):
        if move.poss_idx >= len(move.poss):
            return None

        self._play_move(move.poss[move.poss_idx], move.row, move.col)
        return move._replace(poss_idx=move.poss_idx + 1)

    def least_entropy_pos(self):
        # Assuming Equal Probabilities (We can not do better, I think)
        # The entropy is log2(possibilities) bits
        # and log is proportional to possibilities
        m = None
        mi = 10
        for i, b, y in zip((self.pmap > 0).sum(axis=2), self.board, range(9)):
            for j, c, x in zip(i, b, range(9)):
                if c != 0: continue
                if mi > j:
                    m = y, x
                    mi = j
        return m
        # a = np.where(self.board == 0, pos)
        # return np.unravel_index(np.argmin(pos), pos.shape)

    def get_possible(self, row, col):
        if (w := self.board[row, col]) == 0:
            return LU[self.pmap[row, col] > 0]
        else:
            return [w]

    def get_best_move(self):
        k = self.least_entropy_pos()
        if k is None:
            return None
        w = self.get_possible(k[0], k[1])
        return Move(w, 0, *k)

    def undo_last(self, row: int, col: int): # Unsafe impl
        rq, cq = calc_quadrant(row, col)
        num = self.board[row, col]

        self.pmap[:, col, num - 1] += 1
        self.pmap[row, :, num - 1] += 1

        self.pmap[row, cq, num - 1] -= 1
        self.pmap[rq, col, num - 1] -= 1
        self.pmap[rq, cq, num - 1] += 1

        self.board[row, col] = 0

def solver(board: Board): # Least Entropy DFS solver
    stack = []

    state = board.get_best_move()
    stack.append(board.play_move(state)) # type: ignore
    ne = None
    pops = 0
    apps = 1
    while (board.board == 0).any():
        if len(stack) == 0 and ((ne and ne.poss_idx >= len(ne.poss)) or ne is None): break

        if ne: # if next specified then
            r = board.play_move(ne)
            if r == None:
                ne = stack.pop()
                pops += 1
                board.undo_last(ne.row, ne.col)
                continue
            stack.append(r)
            apps += 1
            ne = None
            continue

        idx = board.least_entropy_pos()
        if idx is None:
            ne = stack.pop()
            pops += 1
            board.undo_last(ne.row, ne.col)
            continue

        a = board.get_possible(idx[0], idx[1])
        state = board.play_move(Move(a, 0, *idx))

        # assert state != None, f"{idx}\n{board.board}\n{board.poss}"
        if state == None:
            ne = stack.pop()
            pops += 1
            board.undo_last(ne.row, ne.col)
            continue

        stack.append(state)
        apps += 1
    return apps, pops, board

def get_first_unoccupied_pos(board: np.ndarray):
    for idx, i in enumerate(board.ravel()):
        if i == 0: return np.unravel_index(idx, board.shape)
    return None

def solver_dfs(board: Board):
    stack = []
    app = stack.append
    pop = stack.pop
    apps = 1
    pops = 0
    b = board.board
    k = get_first_unoccupied_pos(b)
    if k is None:
        return apps, pops, board
    w = board.get_possible(*k)
    app(board.play_move(Move(w, 0, *k)))

    ne = None
    while 1:
        if ne is None:
            k = get_first_unoccupied_pos(b)
            if not k:
                return apps, pops, board
            w = board.get_possible(*k)
            g = board.play_move(Move(w, 0, *k))
            if g is None:
                ne = pop()
                pops += 1
                board.undo_last(ne.row, ne.col)
                continue
            app(g)
            apps += 1
        else:
            g = board.play_move(ne)
            if g is None:
                ne = pop()
                pops += 1
                board.undo_last(ne.row, ne.col)
                continue
            app(g)
            apps += 1
            ne = None
    return apps, pops, board
