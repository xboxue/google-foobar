'''
Distract the Guards
===================

The time for the mass escape has come, and you need to distract the guards so that the bunny prisoners can make it out! Unfortunately for you, they’re watching the bunnies closely. Fortunately, this means they haven’t realized yet that the space station is about to explode due to the destruction of the LAMBCHOP doomsday device. Also fortunately, all that time you spent working as first a minion and then a henchman means that you know the guards are fond of bananas. And gambling. And thumb wrestling.

The guards, being bored, readily accept your suggestion to play the Banana Games.

You will set up simultaneous thumb wrestling matches. In each match, two guards will pair off to thumb wrestle. The guard with fewer bananas will bet all their bananas, and the other guard will match the bet. The winner will receive all of the bet bananas. You don’t pair off guards with the same number of bananas (you will see why, shortly). You know enough guard psychology to know that the one who has more bananas always gets over-confident and loses. Once a match begins, the pair of guards will continue to thumb wrestle and exchange bananas, until both of them have the same number of bananas. Once that happens, both of them will lose interest and go back to guarding the prisoners, and you don’t want THAT to happen!

For example, if the two guards that were paired started with 3 and 5 bananas, after the first round of thumb wrestling they will have 6 and 2 (the one with 3 bananas wins and gets 3 bananas from the loser). After the second round, they will have 4 and 4 (the one with 6 bananas loses 2 bananas). At that point they stop and get back to guarding.

How is all this useful to distract the guards? Notice that if the guards had started with 1 and 4 bananas, then they keep thumb wrestling! 1, 4 -> 2, 3 -> 4, 1 -> 3, 2 -> 1, 4 and so on.

Now your plan is clear. You must pair up the guards in such a way that the maximum number of guards go into an infinite thumb wrestling loop!

Write a function solution(banana_list) which, given a list of positive integers depicting the amount of bananas the each guard starts with, returns the fewest possible number of guards that will be left to watch the prisoners. Element i of the list will be the number of bananas that guard i (counting from 0) starts with.

The number of guards will be at least 1 and not more than 100, and the number of bananas each guard starts with will be a positive integer no more than 1073741823 (i.e. 2^30 -1). Some of them stockpile a LOT of bananas.

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
(int list) banana_list = [1, 1]
Output:
(int) 2

Inputs:
(int list) banana_list = [1, 7, 3, 21, 13, 19]
Output:
(int) 0
'''

from collections import defaultdict


def solution(banana_list):
    graph = defaultdict(list)

    for i in range(len(banana_list)):
        for j in range(len(banana_list)):
            if i != j and hasLoop(banana_list[i], banana_list[j]):
                graph[i].append(j)

    return len(banana_list) - len(matching(graph))


def gcd(x, y):
    while y != 0:
        x, y = y, x % y
    return x


def hasLoop(x, y):
    a = (x + y) / gcd(x, y)
    return a & (a - 1) != 0


class unionFind:
    def __init__(self):
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        '''Find the root of the set that an object is in.
        Object must be hashable; previously unknown objects become new singleton sets.'''

        # check for previously unknown object
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    def union(self, *objects):
        '''Find the sets containing the given objects and merge them all.'''

        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r], r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest


def matching(G, initialMatching={}):
    '''Find a maximum cardinality matching in a graph G using Edmonds blossom-contraction algorithm.'''

    # Copy initial matching so we can use it nondestructively
    matching = {}
    for x in initialMatching:
        matching[x] = initialMatching[x]

    # Form greedy matching to avoid some iterations of augmentation
    for v in G:
        if v not in matching:
            for w in G[v]:
                if w not in matching:
                    matching[v] = w
                    matching[w] = v
                    break

    def augment():
        leader = unionFind()
        S = {}
        T = {}
        unexplored = []
        base = {}

        # Subroutines for augmenting path search.
        def blossom(v, w, a):
            '''Create a new blossom from edge v-w with common ancestor a.'''

            def findSide(v, w):
                path = [leader[v]]
                b = (v, w)   # new base for all T nodes found on the path
                while path[-1] != a:
                    tnode = S[path[-1]]
                    path.append(tnode)
                    base[tnode] = b
                    unexplored.append(tnode)
                    path.append(leader[T[tnode]])
                return path

            a = leader[a]   # sanity check
            path1, path2 = findSide(v, w), findSide(w, v)
            leader.union(*path1)
            leader.union(*path2)
            S[leader[a]] = S[a]  # update structure tree

        topless = object()  # should be unequal to any graph vertex

        def alternatingPath(start, goal=topless):
            '''Return sequence of vertices on alternating path from start to goal.
            Goal must be a T node along the path from the start to the root of the structure tree.
            If goal is omitted, we find an alternating path to the structure tree root.'''

            path = []
            while 1:
                while start in T:
                    v, w = base[start]
                    vs = alternatingPath(v, start)
                    vs.reverse()
                    path += vs
                    start = w
                path.append(start)
                if start not in matching:
                    return path     # reached top of structure tree, done!
                tnode = matching[start]
                path.append(tnode)
                if tnode == goal:
                    return path     # finished recursive subpath
                start = T[tnode]

        def pairs(L):
            '''Utility to partition list into pairs of items.
            If list has odd length, the final pair is omitted silently.'''
            i = 0
            while i < len(L) - 1:
                yield L[i], L[i+1]
                i += 2

        def alternate(v):
            '''Make v unmatched by alternating the path to the root of its structure tree.'''
            path = alternatingPath(v)
            path.reverse()
            for x, y in pairs(path):
                matching[x] = y
                matching[y] = x

        def addMatch(v, w):
            '''Here with an S-S edge vw connecting vertices in different structure trees.
            Find the corresponding augmenting path and use it to augment the matching.'''
            alternate(v)
            alternate(w)
            matching[v] = w
            matching[w] = v

        def ss(v, w):
            '''Handle detection of an S-S edge in augmenting path search.
            Like augment(), returns true iff the matching size was increased.'''

            if leader[v] == leader[w]:
                return False        # self-loop within blossom, ignore

            # parallel search up two branches of structure tree
            # until we find a common ancestor of v and w
            path1, head1 = {}, v
            path2, head2 = {}, w

            def step(path, head):
                head = leader[head]
                parent = leader[S[head]]
                if parent == head:
                    return head     # found root of structure tree
                path[head] = parent
                path[parent] = leader[T[parent]]
                return path[parent]

            while 1:
                head1 = step(path1, head1)
                head2 = step(path2, head2)

                if head1 == head2:
                    blossom(v, w, head1)
                    return False

                if leader[S[head1]] == head1 and leader[S[head2]] == head2:
                    addMatch(v, w)
                    return True

                if head1 in path2:
                    blossom(v, w, head1)
                    return False

                if head2 in path1:
                    blossom(v, w, head2)
                    return False

        # Start of main augmenting path search code.

        for v in G:
            if v not in matching:
                S[v] = v
                unexplored.append(v)

        current = 0     # index into unexplored, in FIFO order so we get short paths
        while current < len(unexplored):
            v = unexplored[current]
            current += 1

            for w in G[v]:
                if leader[w] in S:  # S-S edge: blossom or augmenting path
                    if ss(v, w):
                        return True

                elif w not in T:    # previously unexplored node, add as T-node
                    T[w] = v
                    u = matching[w]
                    if leader[u] not in S:
                        S[u] = w    # and add its match as an S-node
                        unexplored.append(u)

        return False    # ran out of graph without finding an augmenting path

    # augment the matching until it is maximum
    while augment():
        pass

    return matching
