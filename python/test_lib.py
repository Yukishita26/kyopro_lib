import lib
import unittest

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

class TestHashableIntSet(unittest.TestCase):
    def testEquivalence(self):
        s1 = lib.HashableIntSet(5)
        s2 = lib.HashableIntSet({0, 2})
        self.assertEqual(str(s1), "{0, 2}")
        self.assertEqual(str(s2), "{0, 2}")
        self.assertEqual(s1, s2)
    def testLength(self):
        s = lib.HashableIntSet({0, 2})
        self.assertEqual(len(s), 2)
    def testContain(self):
        s = lib.HashableIntSet({0, 2})
        self.assertIn(0, s)
        self.assertNotIn(1, s)
        self.assertIn(2, s)
    def testAdd(self):
        s = lib.HashableIntSet({0, 2})
        s = s | {4}
        self.assertEqual(s, lib.HashableIntSet({0, 2, 4}))
        s |= {6}
        self.assertEqual(s, lib.HashableIntSet({0, 2, 4, 6}))
        s += 3
        self.assertEqual(s, lib.HashableIntSet({0, 2, 3, 4, 6}))
    def testOr(self):
        s = lib.HashableIntSet({0, 2})
        t = lib.HashableIntSet({2, 4})
        self.assertEqual(s | t, lib.HashableIntSet({0, 2, 4}))
        s |= t
        self.assertEqual(s, lib.HashableIntSet({0, 2, 4}))
    def testAnd(self):
        s = lib.HashableIntSet({0, 2})
        t = lib.HashableIntSet({2, 4})
        self.assertEqual(s & t, lib.HashableIntSet({2}))
        s &= t
        self.assertEqual(s, lib.HashableIntSet({2}))
    def testSub(self):
        s = lib.HashableIntSet({0, 2, 4})
        s = s - {4}
        self.assertEqual(s, lib.HashableIntSet({0, 2}))
        s = s - {3}
        self.assertEqual(s, lib.HashableIntSet({0, 2}))
        s = s - 2
        self.assertEqual(s, lib.HashableIntSet({0}))
        s -= 0
        self.assertEqual(s, lib.HashableIntSet(set()))
    def testToSet(self):
        s = lib.HashableIntSet({0, 2})
        self.assertEqual(s.toSet(), {0, 2})

if __name__ == '__main__':
    unittest.main()
