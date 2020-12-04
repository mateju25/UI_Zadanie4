import unittest

import kdtree


class MyTestCase(unittest.TestCase):
    def test_search(self):
        root = None
        root = kdtree.insert_tree(root, [0, 5, 5])
        root = kdtree.insert_tree(root, [0, 2, 3])
        root = kdtree.insert_tree(root, [0, 4, 6])
        root = kdtree.insert_tree(root, [0, 1, 7])
        root = kdtree.insert_tree(root, [0, 6, 2])
        best = kdtree.search_k_tree(root, [0, 7, 7], 1)
        self.assertEqual(best, [[0, 5, 5]])
        best = kdtree.search_k_tree(root, [0, 7, 7], 1)
        self.assertEqual(best, [[0, 4, 6]])

    def test_clear(self):
        root = None
        root = kdtree.insert_tree(root, [0, 5, 5])
        root = kdtree.insert_tree(root, [0, 2, 3])
        root = kdtree.insert_tree(root, [0, 4, 6])
        root = kdtree.insert_tree(root, [0, 1, 7])
        root = kdtree.insert_tree(root, [0, 6, 2])
        best = kdtree.search_k_tree(root, [0, 7, 7], 1)
        self.assertEqual(best, [[0, 5, 5]])
        root = kdtree.clear_tree(root, best)
        best = kdtree.search_k_tree(root, [0, 7, 7], 1)
        self.assertEqual(best, [[0, 5, 5]])


if __name__ == '__main__':
    unittest.main()
