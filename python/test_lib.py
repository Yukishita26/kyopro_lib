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

if __name__ == '__main__':
    unittest.main()
