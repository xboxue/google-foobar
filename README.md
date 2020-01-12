# Google Foobar

Foobar is a hidden coding challenge from Google consisting of 8 challenges over 5 levels of increasing difficulty. Users are invited to participate after searching for certain programming terms on Google. I recieved an invite while researching dependency injection.

The problems in levels 1 and 2 are similar to interview questions. There is a substring problem, an array problem with many edge cases, and a sequence sum problem.

Solutions to level 3 are more involved, requiring dynamic programming and number theory.

Level 4 reformulates two problems in graph theory: maximum matching and maximum flow with multiple sources and multiple sinks. To solve the maximum flow problem, I convert it to a single-source and single-sink problem by introducing dummy source and sink nodes and then use the Edmonds-Karp algorithm. For the maximum matching problem, I use the blossom algorithm.

Level 5 uses a result from group theory known as the Polya enumeration theorem for counting distinct objects while taking symmetry into account. The theorem defines a relation between the number of distinct configurations of a set and the cycles in each permutation of that set, expressed as a polynomial known as the cycle index. In this problem, we look at permutations of rows and columns of an h × w matrix. Formally, the permutations of rows and columns are the symmetric groups S<sub>h</sub> and S<sub>w</sub>, and their combined permutations form the cartesian product S<sub>w</sub> × S<sub>h</sub>. By finding the cycle index for the permutation group S<sub>w</sub> × S<sub>h</sub> acting on an h × w matrix, we can then compute the number of distinct configurations of that matrix.
