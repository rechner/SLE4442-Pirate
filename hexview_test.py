from dataset import Dataset
import unittest
import tkinter
from hexview import HexViewer


class TestDataset(unittest.TestCase):
    def setUp(self):
        self.root = tkinter.Tk()
        self.hexview = HexViewer(master=self.root)
        self.root.pac

        initial_data = '010203040500060708095468652062726f776e20666f78206a756d7073206f76657220746865206c617a7920646f67010203040500'.decode('hex') * 20
        dataset = Dataset(initial_data)
        self.hexview.set_data(dataset)



    def tearDown(self):
        pass

    def test_bytewidth_8(self):
        self.hexview.change_byte_width(8)

    def test_bytewidth_16(self):
        self.test_loaddataset()

        self.hexview.change_byte_width(16)
        self.assertEqual(0, self.hexview.hextext_coord_to_offset(10, 15))
        self.assertEqual(1, self.hexview.hextext_coord_to_offset(50, 15))
        self.assertEqual(8, self.hexview.hextext_coord_to_offset(360, 15))
        self.assertEqual(24, self.hexview.hextext_coord_to_offset(360, 40))

        self.assertEqual((0, 0), self.hexview.hextext_offset_to_coord(0))
        self.assertEqual((1, 0), self.hexview.hextext_offset_to_coord(1))
        self.assertEqual((8, 0), self.hexview.hextext_offset_to_coord(8))
        self.assertEqual((8, 1), self.hexview.hextext_offset_to_coord(25))

        #hextext_offset_to_coord

    def test_bytewidth_32(self):
        self.hexview.change_byte_width(32)