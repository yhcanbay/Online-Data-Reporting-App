import unittest
from data_processor import preprocess

class TestDataProcessor(unittest.TestCase):
    def test_preprocess_empty(self):
        self.assertEqual(preprocess(""), "")
        self.assertEqual(preprocess(None), "")

    def test_preprocess_whitespaces(self):
        self.assertEqual(preprocess("Merhaba!!!  Dünya   "), "Merhaba!!! Dünya")

    def test_preprocess_newlines(self):
        text = "Satır\n\n\nYeni Satır"
        self.assertEqual(preprocess(text), "Satır Yeni Satır")

if __name__ == '__main__':
    unittest.main()
