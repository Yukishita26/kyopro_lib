# 再帰深さ制限の設定
import sys
sys.setrecursionlimit(30000)
# メモ化再帰
# roopによるdpよりかなり遅いので注意
from functools import lru_cache
@lru_cache(maxsize=30000)
def hogehoge():
    pass

# 切り上げ割り算
def divup(a, b):
    return -(-a//b)
    
# 繰り返し2乗法
# ModIntなら組み込み pow(x, p, mod) で可能
def reppow(x, p, f):
    if p==1: return x
    r = reppow(x, p//2, f)
    if p%2==0:
        return f(r, r)
    else:
        return f(x, f(r, r))

# UnionFindTree
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

# めぐる式二分探索
# Callable[[int], bool], int, int -> int(index)
# left < x < right で func(x)=True となる最小のxを探索
def binsearch(func, left, right):
  while left+1<right:
    mid = left + (right - left)//2
    if func(mid):
      right = mid
    else:
      left = mid
  return right

# List[T], T -> int(昇順に挿入できるindex)
# 単にlistのサーチなら
"""
from bisect import bisect_left
i = bisect_left(lst, x)
"""
# の方が速い
def binsearch_list_left(lst, x):
    return binsearch(lambda i:lst[i]>=x, -1, len(lst))

import numpy as np
class Permutation:
    def __init__(self, arr):
        if len(arr) != len([a for a in arr if 0<=a<len(arr)]):
            raise ValueError("array could not be converted to permutation")
        self._arr = arr
    def size(self):
        return len(self._arr)
    def apply(self, x):
        if not(0 <= x < self.size()):
            raise IndexError()
        return self._arr[x]
    def order(self):
        Id = Permutation.Id(self.size())
        x = self
        for i in range(self.size() + 1):
            if x == Id:
                return i+1
            x *= self
        return -1
    def transposition_disassembly(self):
        pass
    def toMatrix(self):
        return np.array([[1 if i==self.apply(j) else 0 for j in range(self.size())] for i in range(self.size())])
    def sign(self):
        return int(np.linalg.det(self.toMatrix()))
    def __mul__(self, other):
        if self.size() != other.size():
            raise ValueError(f"operands could not be broadcast together with shapes ({self.size()},) ({other.size()},)")
        return Permutation([self.apply(other.apply(i)) for i in range(self.size())])
    def __pow__(self, n):
        r = Permutation.Id(self.size())
        x = self
        while n > 0:
            if n % 2 != 0:
                r *= x
            x *= x
            n >>= 1
        return r
    def __eq__(self, other):
        if type(other) != Permutation:
            return False
        return self._arr == other._arr
    def __str__(self):
        return  "(" + " ".join(str(self.apply(i)) for i in range(self.size())) + ")"
    @classmethod
    def Id(cls, n):
        return cls(list(range(n)))

# ModInt & combination
class ModInt:
    default_mod = 10**9 + 7
    class SubstitutionError(Exception):
        pass
    def __init__(self, n, mod=None):
        if mod is None:
            mod = self.default_mod
        self._mod = mod
        self._n = n.n if isinstance(n, ModInt) else n % mod
    
    @property
    def mod(self):
        return self._mod
    @mod.setter
    def mod(self, value):        
        raise self.SubstitutionError("cannot assign to ModInt property")
    
    @property
    def n(self):
        return self._n
    @n.setter
    def n(self, value):
        raise self.SubstitutionError("cannot assign to ModInt property")

    def __eq__(self, other):
        if not(isinstance(other, ModInt)):
            return False
        return self.mod == other.mod and self.n == other.n
    def __add__(self, other):
        if isinstance(other, ModInt): other=other.n
        return ModInt(self.n + other, self.mod)
    __radd__=__add__
    def __sub__(self, other):
        if isinstance(other, ModInt): other=other.n
        return ModInt(self.n - other, self.mod)
    def __rsub__(self, other):
        if isinstance(other, ModInt): other=other.n
        return ModInt(other - self.n, self.mod)
    def __mul__(self, other):
        if isinstance(other, ModInt): other=other.n
        return ModInt(self.n * other, self.mod)
    __rmul__=__mul__
    def __pow__(self, p: int):
        """
        if p==0:
            return ModInt(1, self.mod)
        m = self.__pow__(p//2)
        if p%2==0:
            return m * m
        else:
            return self * m * m
        """
        return ModInt(pow(self.n, p, mod=self.mod))
    def inv(self):
        return ModInt(pow(self.n, -1, mod=self.mod))
        #return self ** (self.mod - 2)
    def __truediv__(self, other):
        if isinstance(other, int): other=ModInt(other)
        return self * other.inv()
    def __rtruediv__(self, other):
        if isinstance(other, int): other=ModInt(other)
        return other * self.inv()
    def __str__(self):
        return str(self.n)
    def __repr__(self):
        return f"ModInt({self.n}, {self.mod})"
    @classmethod
    def comb(cls, n, k, mod=default_mod):
        if isinstance(k, cls):
            mod = k.mod
            k = k.n
        if isinstance(n, cls):
            mod = n.mod
            n = n.n
        k = min(k, n-k)
        nf = ModInt(1, mod)
        for i in range(n-k+1, n+1):
            nf *= i
        kf = ModInt(1, mod)
        for i in range(1,k+1):
            kf *= i
        return nf / kf


from collections import deque

# 強連結成分分解
class SCC:
  def __init__(self, graph):
    self.graph = graph
  def visit_dfs(self, top, depth):
    self.visited[top] = depth
    stack = [top]
    while stack:
      top = stack[-1]
      if self.quegraph[top]:
        nxt = self.quegraph[top].popleft()
        if self.visited[nxt]==-1:
          self.visited[nxt] = self.visited[top] + 1
          stack.append(nxt)
      else:
        self.orders += [top]
        stack.pop()
  def dfs_return_order(self):
    self.visited = [-1] * len(self.graph)
    self.orders = []
    self.quegraph = [deque(l) for l in self.graph]
    for i in range(1, len(self.graph)):
      if self.visited[i]==-1:
        self.visit_dfs(i, 0)
    return self.orders
  def revisit_dfs(self, top, section):
    self.revisited[top] = section
    stack = [top]
    while stack:
      top = stack.pop()
      for nxt in self.rev_graph[top]:
        if self.revisited[nxt]!=-1:continue
        self.revisited[nxt] = self.revisited[top]
        stack.append(nxt)
  # 強連結成分(行き帰りできる成分の組)のグループ
  # 代表元:同じグループの頂点 のdictで返す
  def scc(self):
    self.rev_graph = [[] for _ in range(len(self.graph))]
    for i in range(len(self.graph)):
      for v in self.graph[i]:
        self.rev_graph[v] += [i]
    self.dfs_return_order()
    self.revisited = [-1] * len(self.graph)
    for i in self.orders[::-1]:
      if self.revisited[i]==-1:
        self.revisit_dfs(i, i)
    scc = {}
    for i,v in enumerate(self.revisited):
      if v==-1:continue
      if v in scc:
        scc[v] += [i]
      else:
        scc[v] = [i]
    return scc
