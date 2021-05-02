class UnionFindTree:
    def __init__(self, n):
        self._tree = [i for i in range(n)]
        self._rank = [1] * n
    def root(self, a):
        if self._tree[a] == a:return a
        self._tree[a] = self.root(self._tree[a])
        return self._tree[a]
    def is_same_set(self, a, b):
        return self.root(a) == self.root(b)
    def unite(self, a, b):
        ra = self.root(a)
        rb = self.root(b)
        if ra == rb: return
        if self._rank[ra] < self._rank[rb]:
            self._tree[ra] = rb
        else:
            self._tree[rb] = ra
            if self._rank[ra] == self._rank[rb]:
                self._rank[ra] += 1

from collections import deque
# graph(隣接リスト), 起点node -> deepest node, depth
def bfs_depth(graph, start: int): 
    dist = [-1] * (len(graph))
    dist[start] = 0
    deepest_node = start
    depth = 0
    q = deque()
    q.append(start)
    while q:
        top = q.popleft()
        for next_node in graph[top]:
            if dist[next_node] != -1:
                continue
            dist[next_node] = dist[top] + 1
            deepest_node = next_node
            depth = dist[next_node]
            q.append(next_node)
    # return dist
    return deepest_node, depth

# graph(隣接グラフ) -> 木の直径
def tree_diameter(graph):
    nodel, _ = bfs_depth(graph, 1)
    _node, r = bfs_depth(graph, nodel)
    return r
