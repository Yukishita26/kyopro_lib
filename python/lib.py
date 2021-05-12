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

class HashableIntSet:
    class SubstitutionError(Exception):
        pass
    def __init__(self, s):
        if type(s)==set:
            sm = 0
            for i in s:
                if type(i)!=int:
                    raise TypeError(f"HashableSet must be initialized with 'set' of 'int' or hash number, not {type(s)}")
                sm += 1<<i
            self._hash = sm
        elif type(s)==int:
            if s<0: raise ValueError("hash must be positive")
            self._hash = s
        else:
            raise TypeError(f"HashableSet must be initialized with 'set' or hash number, not {type(s)}")
    
    @property
    def hash(self):
        return self._hash
    @hash.setter
    def hash(self, value):
        raise SubstitutionError("hash can't be changed")

    def __hash__(self):
        return self.hash
    def __eq__(self, other):
        return self.hash == other.hash
    def __contains__(self, other):
        if type(other)!=int:
            raise TypeError(f"'in <HashableIntSet>' requires a integer as left operand, not {type(other)}")
        return self.hash>>other&1 
    def __len__(self):
        return bin(self.hash).count("1")
    def __add__(self, other):
        if type(other)==int:
            return HashableIntSet(self.hash|(1<<other))
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'HashableIntSet' and '{type(other)}'")
    def __or__(self, other):
        if type(other)==set:
            other = HashableIntSet(other)
        if type(other)==HashableIntSet:
            return HashableIntSet(self.hash | other.hash)
        else:
            raise TypeError(f"unsupported operand type(s) for |: 'HashableIntSet' and '{type(other)}'")
    def __and__(self, other):
        if type(other)==set:
            other = HashableIntSet(other)
        if type(other)==HashableIntSet:
            return HashableIntSet(self.hash & other.hash)
        else:
            raise TypeError(f"unsupported operand type(s) for &: 'HashableIntSet' and '{type(other)}'")
    def __sub__(self, other):
        if type(other)==int:
            return HashableIntSet(self.hash^(1<<other)&self.hash)
        if type(other)==HashableIntSet:
            other = other.toSet()
        if type(other)==set:
            h = self.hash
            for o in other: h = h^(1<<o)&h
            return HashableIntSet(h)
        else:
            raise TypeError(f"unsupported operand type(s) for -: 'HashableIntSet' and '{type(other)}'")
    def __iter__(self):
        return iter(self.toSet())
    def toSet(self):
        s = set()
        h = self.hash
        i = 0
        while h>0:
            if h&1: s.add(i)
            h >>= 1
            i += 1
        return s
    def __str__(self):
        return str(self.toSet())
    def __repr__(self):
        return f"HashableIntSet({self.toSet()})"
    # TODO
    def __xor__(self, other):
        pass
    def __le__(self, other):
        pass
    def __ge__(self, other):
        pass
    def __lt__(self, other):
        pass
    def __gt__(self, other):
        pass
    @classmethod
    def EmptySet(cls):
        return cls(set())

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
