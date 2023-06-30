# Least Entropy Sudoku Space Search

This experment examines whether a minimum entropy guided depth first search has lesser operations on the stack (implying less searched states)
compared to a sequential order

(In progress)

## TODO

- [ ] Solidify theory (Calculations have a lot of combinatronics and information theory, help wanted)
- [ ] Optimise Implementation
- [ ] Implement in C++
- [ ] Optimise Implementation
- [ ] Statistically Benchmark the appends and pop operation counts over a huge dataset
- [ ] Hypothesis testing

## Observations Till now

(Warning: Unoptimised results)

Least Entropy DFS was 8.6 times **slower** than normal dfs on test_expert puzzle

The append and pop operations were 4 times greater on Least Entropy method.

This doesn't say the variant is bad. Since it's just one test run's results,
but it cant beat DFS in the thing it was supposed to be beat it in and hence
I am gonna procrastinate this as this doesn't seem very promising.
Perhaps I have an implementation or theoritical issue.

The normal DFS version unoptimised ran in 0.071 seconds which is a good time for python OOP
considering that Z3 took 0.05 seconds to solve the same puzzle (although Z3 isn't a specialised
sudoku solver, it sets a benchmark for now)

## Future Work

If promising entropy reduction and least entropy search could be coupled existing optimisation
algorithms to make more efficient (in terms of time or energy) optimisation algorithms