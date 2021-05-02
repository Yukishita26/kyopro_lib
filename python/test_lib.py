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

if __name__ == '__main__':
    unittest.main()
