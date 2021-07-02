import lib
import unittest

import numpy as np
class TestEratosthenes(unittest.TestCase):
    def test_numpy(self):
        self.assertEqual(lib.eratosthenes(100).tolist(),
            [False, False,  True,  True, False,  True, False,  True, False,
                False, False,  True, False,  True, False, False, False,  True,
                False,  True, False, False, False,  True, False, False, False,
                False, False,  True, False,  True, False, False, False, False,
                False,  True, False, False, False,  True, False,  True, False,
                False, False,  True, False, False, False, False, False,  True,
                False, False, False, False, False,  True, False,  True, False,
                False, False, False, False,  True, False, False, False,  True,
                False,  True, False, False, False, False, False,  True, False,
                False, False,  True, False, False, False, False, False,  True,
                False, False, False, False, False, False, False,  True, False,
                False, False])
        self.assertEqual(np.arange(0,101,1)[lib.eratosthenes(100)].tolist(),
            [ 2,  3,  5,  7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
                61, 67, 71, 73, 79, 83, 89, 97])
    def test_plain(self):
        self.assertEqual(lib.eratosthenes_plain(100),
            [False, False,  True,  True, False,  True, False,  True, False,
                False, False,  True, False,  True, False, False, False,  True,
                False,  True, False, False, False,  True, False, False, False,
                False, False,  True, False,  True, False, False, False, False,
                False,  True, False, False, False,  True, False,  True, False,
                False, False,  True, False, False, False, False, False,  True,
                False, False, False, False, False,  True, False,  True, False,
                False, False, False, False,  True, False, False, False,  True,
                False,  True, False, False, False, False, False,  True, False,
                False, False,  True, False, False, False, False, False,  True,
                False, False, False, False, False, False, False,  True, False,
                False, False])

class TestUFT(unittest.TestCase):
    def testUnite(self):
        uft = lib.UnionFindTree(5)
        self.assertFalse(uft.is_same_set(1,3))
        uft.unite(1, 2)
        self.assertFalse(uft.is_same_set(1,3))
        uft.unite(2, 3)
        self.assertTrue(uft.is_same_set(1,3))
    def testRoot(self):
        uft = lib.UnionFindTree(5)
        for i in range(5):
            self.assertEqual(uft.root(i), i)
        uft.unite(1, 2)
        uft.unite(2, 3)
        self.assertEqual(uft.root(1), uft.root(3))
        self.assertNotEqual(uft.root(0), uft.root(3))

class TestTreeDiamiter(unittest.TestCase):
    def solveStr(self, s):
        s = s.split("\n")
        N = int(s[0].strip())
        d = [[] for _ in range(N+1)]
        for i in range(N-1):
            a, b = map(int, s[i+1].strip().split())
            d[a].append(b)
            d[b].append(a)
        return lib.tree_diameter(d)
        
    # テストケースは https://atcoder.jp/contests/typical90/tasks/typical90_c より
    def testTreeDiameter1(self):
        self.assertEqual(self.solveStr("""5
1 2
2 3
3 4
3 5
"""), 3)
    def testTreeDiameter2(self):
        self.assertEqual(self.solveStr("""10
1 2
1 3
2 4
4 5
4 6
3 7
7 8
8 9
8 10
"""), 7)
    def testTreeDiameter3(self):
        self.assertEqual(self.solveStr("""31
1 2
1 3
2 4
2 5
3 6
3 7
4 8
4 9
5 10
5 11
6 12
6 13
7 14
7 15
8 16
8 17
9 18
9 19
10 20
10 21
11 22
11 23
12 24
12 25
13 26
13 27
14 28
14 29
15 30
15 31
"""), 8)

class TestBinsearch(unittest.TestCase):
    def testBinsearch(self):
        ls = [0, 1, 3, 3, 4, 6, 8, 10]
        self.assertEqual(lib.binsearch(lambda x:ls[x]>=1, -1, 8), 1)
        self.assertEqual(lib.binsearch(lambda x:ls[x]>=2, -1, 8), 2)
        self.assertEqual(lib.binsearch(lambda x:ls[x]>=3, -1, 8), 2)
        self.assertEqual(lib.binsearch(lambda x:ls[x]>=4, -1, 8), 4)
    def testBinsearchList(self):
        ls = [0, 1, 3, 3, 4, 6, 8, 10]
        self.assertEqual(lib.binsearch_list_left(ls, 1), 1)
        self.assertEqual(lib.binsearch_list_left(ls, 2), 2)
        self.assertEqual(lib.binsearch_list_left(ls, 3), 2)
        self.assertEqual(lib.binsearch_list_left(ls, 4), 4)

class TestPermutation(unittest.TestCase):
    Id = lib.Permutation.Id(3)
    sigma = lib.Permutation([1,2,0])
    tau = lib.Permutation([0,2,1])
    rand = lib.Permutation([1,4,2,6,3,5,0])

    def testSize(self):
        self.assertEqual(self.sigma.size(), 3)
        self.assertNotEqual(self.rand.size(), 5)
    def testApply(self):
        self.assertEqual(self.sigma.apply(0), 1)
        self.assertEqual(self.sigma.apply(1), 2)
        self.assertEqual(self.sigma.apply(2), 0)
    def testMul(self):
        self.assertEqual(self.tau * self.tau, self.Id)
    def testPow(self):
        self.assertEqual(self.sigma ** 3, self.Id)
    def testOrder(self):
        self.assertEqual(self.Id.order(), 1)
        self.assertEqual(self.tau.order(), 2)
        self.assertEqual(self.sigma.order(), 3)
    def testSign(self):
        self.assertEqual(self.Id.sign(), 1)
        self.assertEqual(self.sigma.sign(), 1)
        self.assertEqual(self.tau.sign(), -1)

class TestModInt(unittest.TestCase):
    def testEq(self):
        mod = 10**9 + 7
        a = lib.ModInt(5)
        b = lib.ModInt(5 + mod)
        self.assertEqual(a, b)
        c = lib.ModInt(5, 107)
        d = lib.ModInt(5 + 107 * 1234, 107)
        self.assertEqual(c, d)
    def testAdd(self):
        #mod = 10**9 + 7
        a = lib.ModInt(5)
        b = lib.ModInt(3)
        self.assertEqual(a + b, lib.ModInt(8))
        self.assertEqual(a + 3, lib.ModInt(8))
        self.assertEqual(5 + b, lib.ModInt(8))
    def testMul(self):
        #mod = 10**9 + 7
        a = lib.ModInt(5)
        b = lib.ModInt(3)
        self.assertEqual(a * b, lib.ModInt(15))
        self.assertEqual(a * 3, lib.ModInt(15))
        self.assertEqual(5 * b, lib.ModInt(15))
    def testSub(self):
        mod = 10**9 + 7
        a = lib.ModInt(5)
        b = lib.ModInt(3)
        self.assertEqual(a - b, lib.ModInt(2))
        self.assertEqual(a - 3, lib.ModInt(2))
        self.assertEqual(5 - b, lib.ModInt(2))
        self.assertEqual(b - a, lib.ModInt(mod - 2))
    def testDiv(self):
        a = lib.ModInt(12)
        b = lib.ModInt(5)
        self.assertEqual(a / 3, lib.ModInt(4))
        self.assertEqual(24 / a, lib.ModInt(2))
        self.assertEqual(1 / b, lib.ModInt(400000003))
    def testPow(self):
        a = lib.ModInt(3)
        self.assertEqual(a ** 123, lib.ModInt(3 ** 123)) # 950574363
    def testString(self):
        a = lib.ModInt(3)
        b = lib.ModInt(3, 107)
        self.assertEqual(str(a), "3")
        self.assertEqual(str(b), "3")
        self.assertEqual(repr(a), "ModInt(3, 1000000007)")
        self.assertEqual(repr(b), "ModInt(3, 107)")
    def testComb(self):
        self.assertEqual(lib.ModInt.comb(5, 3).n, 10)
        self.assertEqual(lib.ModInt.comb(1003, 50).n, 55229169)
        self.assertEqual(lib.ModInt.comb(103, 5, mod=10**7+7).n, 7541189)


class TestSCC(unittest.TestCase):
    # 参考 https://twitter.com/e869120/status/1385363292739104775/photo/1
    def test1SCC(self):
        itr=iter("""9 11
1 2
2 7
7 1
4 2
4 6
6 9
9 5
5 4
6 8
8 3
3 8
""".split("\n"))
        Input=lambda:map(int,next(itr).split())
        N,M = Input()
        graph = [[] for _ in range(N+1)]
        for _ in range(M):
            A,B = Input()
            graph[A].append(B)

        scc = lib.SCC(graph)
        sections = scc.scc()
        self.assertEqual(sections, {1: [1, 2, 7], 3: [3, 8], 4: [4, 5, 6, 9]})
        ans = 0
        for v in sections.values():
            l = len(v)
            ans += l*(l-1)//2
        self.assertEqual(ans, 10)
    # 参考 https://atcoder.jp/contests/typical90/tasks/typical90_u test1
    def test2SCC(self):
        itr=iter("""4 7
1 2
2 1
2 3
4 3
4 1
1 4
2 3
""".split("\n"))
        Input=lambda:map(int,next(itr).split())
        N,M = Input()
        graph = [[] for _ in range(N+1)]
        for _ in range(M):
            A,B = Input()
            graph[A].append(B)

        scc = lib.SCC(graph)
        sections = scc.scc()
        self.assertEqual(sections, {1: [1, 2, 4], 3: [3]})
        ans = 0
        for v in sections.values():
            l = len(v)
            ans += l*(l-1)//2
        self.assertEqual(ans, 3)
    # 参考 https://atcoder.jp/contests/typical90/tasks/typical90_u test2
    def test3SCC(self):
        itr=iter("""100 1
1 2
""".split("\n"))
        Input=lambda:map(int,next(itr).split())
        N,M = Input()
        graph = [[] for _ in range(N+1)]
        for _ in range(M):
            A,B = Input()
            graph[A].append(B)

        scc = lib.SCC(graph)
        sections = scc.scc()
        self.assertEqual(sections, {1: [1], 2: [2], 3: [3], 4: [4], 5: [5], 6: [6], 7: [7], 8: [8], 9: [9], 10: [10], 11: [11], 12: [12], 13: [13], 14: [14], 15: [15], 16: [16], 17: [17], 18: [18], 19: [19], 20: [20], 21: [21], 22: [22], 23: [23], 24: [24], 25: [25], 26: [26], 27: [27], 28: [28], 29: [29], 30: [30], 31: [31], 32: [32], 33: [33], 34: [34], 35: [35], 36: [36], 37: [37], 38: [38], 39: [39], 40: [40], 41: [41], 42: [42], 43: [43], 44: [44], 45: [45], 46: [46], 47: [47], 48: [48], 49: [49], 50: [50], 51: [51], 52: [52], 53: [53], 54: [54], 55: [55], 56: [56], 57: [57], 58: [58], 59: [59], 60: [60], 61: [61], 62: [62], 63: [63], 64: [64], 65: [65], 66: [66], 67: [67], 68: [68], 69: [69], 70: [70], 71: [71], 72: [72], 73: [73], 74: [74], 75: [75], 76: [76], 77: [77], 78: [78], 79: [79], 80: [80], 81: [81], 82: [82], 83: [83], 84: [84], 85: [85], 86: [86], 87: [87], 88: [88], 89: [89], 90: [90], 91: [91], 92: [92], 93: [93], 94: [94], 95: [95], 96: [96], 97: [97], 98: [98], 99: [99], 100: [100]})
        ans = 0
        for v in sections.values():
            l = len(v)
            ans += l*(l-1)//2
        self.assertEqual(ans, 0)

if __name__ == '__main__':
    # use -v option to output verbose
    unittest.main()
