import unittest

from data_structures.binary_search_tree import BinarySearchTree


class BinarySearchTreeTests(unittest.TestCase):
    def test_empty_tree_does_not_contains_elements(self):
        # Arrange
        tree = BinarySearchTree()

        # Act
        contained = tree.contains(10)

        # Assert
        self.assertFalse(contained)

    def test_tree_inserted_element_is_found(self):
        # Arrange
        tree = BinarySearchTree()
        tree.insert(1)

        # Act
        contained = tree.contains(1)

        # Assert
        self.assertTrue(contained)

    def test_multiple_values_are_found(self):
        # Arrange
        tree = BinarySearchTree()
        tree.insert(12)
        tree.insert(13)
        tree.insert(4)
        tree.insert(9)
        tree.insert(16)

        # Act
        contained_12 = tree.contains(12)
        contained_13 = tree.contains(13)
        contained_4 = tree.contains(4)
        missed_25 = tree.contains(25)

        # Assert
        self.assertTrue(contained_12)
        self.assertTrue(contained_13)
        self.assertTrue(contained_4)
        self.assertFalse(missed_25)

    def test_tree_multiple_values_successor_is_found(self):
        # Arrange
        tree = BinarySearchTree()
        tree.insert(12)
        tree.insert(25)
        tree.insert(6)
        tree.insert(27)
        tree.insert(21)
        tree.insert(3)
        tree.insert(7)
        tree.insert(26)

        # Act
        successor = tree.get_successor(25)

        # Assert
        self.assertEqual(successor, 27)

    def test_tree_multiple_values_range_is_correct(self):
        # Arrange
        tree = BinarySearchTree()
        tree.insert(12)
        tree.insert(25)
        tree.insert(6)
        tree.insert(27)
        tree.insert(21)
        tree.insert(3)
        tree.insert(7)
        tree.insert(26)

        # Act
        range_values = tree.range(21, 26)

        # Assert
        self.assertCountEqual(range_values, [21, 25, 26])
