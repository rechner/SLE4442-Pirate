
from dataset import Dataset
import unittest


class TestDataset(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_insert(self):
        initial_data = "The brown fox jumps over the lazy dog"
        dataset = Dataset(initial_data)

        dataset.insert(4, "quick ")  # insert the word 'quick '
        self.assertEqual("The quick brown fox jumps over the lazy dog", dataset.data)
        dataset.undo()
        self.assertEqual("The brown fox jumps over the lazy dog", dataset.data)
        dataset.redo()
        self.assertEqual("The quick brown fox jumps over the lazy dog", dataset.data)

    def test_delete(self):
        initial_data = "The quick brown fox jumps over the lazy dog"
        dataset = Dataset(initial_data)

        dataset.delete(4, 6)  # remove the word 'quick '
        self.assertEqual("The brown fox jumps over the lazy dog", dataset.data)
        dataset.undo()
        self.assertEqual("The quick brown fox jumps over the lazy dog", dataset.data)
        dataset.redo()
        self.assertEqual("The brown fox jumps over the lazy dog", dataset.data)

    def test_overwrite(self):
        initial_data = "The quick brown fox jumps over the lazy dog"
        dataset = Dataset(initial_data)

        dataset.overtype(16, "dog")  # replace first instance of fox with dog
        dataset.overtype(40, "fox")  # replace second instance of dog with fox
        self.assertEqual("The quick brown dog jumps over the lazy fox", dataset.data)
        dataset.undo()
        self.assertEqual("The quick brown dog jumps over the lazy dog", dataset.data)
        dataset.redo()
        self.assertEqual("The quick brown dog jumps over the lazy fox", dataset.data)

    def test_remove(self):
        initial_data = "The quick brown fox jumps over the lazy dog"
        dataset = Dataset(initial_data)

        dataset.delete(4,6)  # remove the word 'quick '
        self.assertEqual(dataset.data, "The brown fox jumps over the lazy dog")
        self.assertEqual(len(dataset.data), 37)

    def test_undo(self):
        initial_data = "The quick brown fox jumps over the lazy dog"
        dataset = Dataset(initial_data)

        dataset.delete(4, 6)  # remove the word 'quick '
        dataset.delete(0, 4)  # remove the word 'The '
        self.assertEqual(dataset.data, "brown fox jumps over the lazy dog")
        dataset.undo()
        self.assertEqual(dataset.data, "The brown fox jumps over the lazy dog")

    def test_redo(self):
        initial_data = "The quick brown fox jumps over the lazy dog"
        dataset = Dataset(initial_data)

        dataset.delete(4, 6)  # remove the word 'quick '
        dataset.delete(0, 4)  # remove the word 'The '
        self.assertEqual("brown fox jumps over the lazy dog", dataset.data)
        dataset.undo()
        self.assertEqual("The brown fox jumps over the lazy dog", dataset.data)
        dataset.redo()
        self.assertEqual("brown fox jumps over the lazy dog", dataset.data)

if __name__ == '__main__':
    unittest.main()
