# knapsack-solver
Here is a simple evolutionary knapsack problem solver using DEAP. It's a little
raw but it does give a fairly straightforward example of how to use DEAP to
tackle a certain class of problem in combinatorial optimization. `solver.py`
will run as long as numpy and DEAP are installed. It requires two input files
in the same directory, `items.json` and `capacity.json`. The former contains
an array filled with objects having the keys `weight` and `profit` for each
item that could possibly go into the knapsack. In my example, the values for
those keys are all integers, but they could just as well be floating point and
it'd make no difference. The latter JSON file literally only contains one
number representing the capacity of the knapsack. Again, an integer is used
here but floating point is also fine.

The genome is simple, as many bits as there are items, with appropriate
operators. The evaluator function operates on two criteria, the first and most
important being overload, that is, how much the combined weight of the items in
the knapsack exceeds capacity. If there is no overload, this is zero. Positive
values cannot be permitted at all. The second is the combined profit of the set
of items that do in fact fit in the knapsack. Something I ought to mention at
this juncture is that, because multi-criteria optimization in DEAP uses
lexicographic ordering, getting the order of the criteria right is
**extremely** important. You can't just chuck in the criteria in any order and
expect the right outcome.

When it runs, it'll chug for a little while depending on the size of the
problem and the parameters for the algorithm. In my instance, it was very
reasonable in the time it took and I imagine that a good deal of bigger
problems could be tackled without any need to rewrite in C++ or something more
low-level like that, taking maybe a few minutes to run through to completion.
When all is said and done, you'll get a neatly formatted report that shows
which items were chosen, their total weight, the capacity and the profit.

The instance I used comes from here (P08):

https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html

It says that the optimal profit is 13549094. When I ran my solver, I got a
solution with a profit of 13524340, about 99.8% of this optimum. This amounts
to a simple but compelling demonstration of the power of evolution. It's not
perfect, but it can be clever.
