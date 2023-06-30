# Least Entropy Sudoku Space Search

This experment examines whether a minimum entropy guided depth first search has lesser operations on the stack (implying less searched states)
compared to a sequential order

(In progress)

## TODO

- [x] Solidify theory (partly done)
- [ ] Optimise Implementation
- [ ] Implement in C++
- [ ] Optimise Implementation
- [ ] Statistically Benchmark the appends and pop operation counts over a huge dataset
- [ ] Hypothesis testing

## Huge Update!

TLDR: 125x less Pops, Unoptimised code runs 3x faster

Upon noticing that pmap has negatives as well (for the purpose of restoring state easily)
I noticed that I was calaculating entropy from the pmap! meaning that if a cell has the maximal
amount of constraints to not equal a number (which is 3, one for row, col and quadrant)
then that cell is considered to have the least entropy! But this is incorrect! since the possible
values for that cell are still 8!

upon converting pmap to the bitmap by `(self.pmap > 0)` and summing it up to get the approximated entropy map
`(self.pmap > 0).sum(axis=2)` (if each number is equally likely then this is proportinal to informational entropy)

And, wouldn't you believe it, it ran in just 57 Appends and 4 Pops! Thats hardly any more states searched
furthermore this horribly written Python OOP code ran in just 0.017 seconds beating the plain DFS by little over **3x times in speed**
(which is not even the goal of this experiment) and beat plain DFS by **125x less pops!** (we dont compare appends, as there is a minimum value
required for appends without which the stack doesn't grow)

also a part of tdoku tests were ran, and only the least entropy sudoku solver could
solve them within time, with worst time being 17 seconds, 57316 pops
while DFS got stuck on the 9th test.

For the immediate goals, optimising the entropy calculation and making it more
accurate.

## More accurate entropy calculation
currently we treat all possibilities as having equal chance but that is not
true apart from the board state, the other information we have is the distribution
of the currently played digits, from which we can determine which possbility is
more likely and pick that first, however it should not have much improvement on a
9*9 board.

## Past Observations

<details>
<summary>Outdated Observations</summary>
(Warning: Unoptimised results) **OUTDATED**

Least Entropy DFS was 8.6 times **slower** than normal dfs on test_expert puzzle

The append and pop operations were 4 times greater on Least Entropy method.

This doesn't say the variant is bad. Since it's just one test run's results,
but it cant beat DFS in the thing it was supposed to be beat it in and hence
I am gonna procrastinate this as this doesn't seem very promising.
Perhaps I have an implementation or theoritical issue.

The normal DFS version unoptimised ran in 0.071 seconds which is a good time for python OOP
considering that Z3 took 0.05 seconds to solve the same puzzle (although Z3 isn't a specialised
sudoku solver, it sets a benchmark for now)
</details>

## Future Work

I will work on coupling entropy reduction and least entropy search
with existing optimisation algorithms to make more efficient (in terms of
time or energy) optimisation algorithms.

Since Entropy reduction seems to be a very effiecient way of doing things