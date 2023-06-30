import lentdoku
from time import perf_counter
import numpy as np

# with open("test_expert.txt", "r") as fp:
#     for r in range(9):
#         for c, i in enumerate(fp.readline()[:-1]):
#             if i != '.': board._play_move(int(i), r, c)

with open("test.txt", "r") as fp:
    k = 0
    while (w:=fp.readline()):
        board = lentdoku.Board()
        for c, i in enumerate(w.split(":")[0]):
            if i != '.': board._play_move(int(i), *np.unravel_index(c, (9, 9))) #type: ignore

        n = perf_counter()
        r = lentdoku.solver(board)
        print(perf_counter() - n)
        k += 1
        print(r[0], "Appends |", r[1], "Pops")
        print(r[2].board)
        print(k)
# print(2)