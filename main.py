import lentdoku
from time import perf_counter

board = lentdoku.Board()

with open("test_expert.txt", "r") as fp:
    for r in range(9):
        for c, i in enumerate(fp.readline()[:-1]):
            if i != '.': board._play_move(int(i), r, c)

n = perf_counter()
r = lentdoku.solver(board)
print(perf_counter() - n)
print(r[0], "Appends |", r[1], "Pops")
print(r[2].board)
# print(2)