import unittest
from pathlib import Path
import os, sys
import json

parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

import tempfile
import src.compile_word_counts as q1
import src.compute_pony_lang as q2

STOP_WORDS_PATH = Path('data/stopwords.txt')
MAIN_CHARACTERS = ['twilight sparkle', 'applejack', 'rarity', 'pinkie pie', 'rainbow dash', 'fluttershy']


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')

    def test_task1(self):
        # use self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        print(f"Test Task 1")
        with open(STOP_WORDS_PATH) as stopf:
            stopwords = stopf.readlines()
        with tempfile.TemporaryDirectory() as tmpdir:
            q1.start('test/fixtures/mock_dialog.csv', f'{tmpdir}/tmp.json', MAIN_CHARACTERS, stopwords)
            with open(self.true_word_counts) as jf:
                with open(f'{tmpdir}/tmp.json') as jf2:
                    self.assertEqual(json.load(jf), json.load(jf2))

    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        print(f"\nTest Task 2")
        with open(STOP_WORDS_PATH) as stopf:
            stopwords = stopf.readlines()
        with tempfile.TemporaryDirectory() as tmpdir:
            q1.start('test/fixtures/mock_dialog.csv', f'{tmpdir}/tmp.json', MAIN_CHARACTERS, stopwords)

            q2_dict = q2.start(f'{tmpdir}/tmp.json', 10, MAIN_CHARACTERS)

            with open(self.true_tf_idfs) as jf:
                expected_json = json.load(jf)
                self.assertEqual(expected_json, q2_dict)

if __name__ == '__main__':
    unittest.main()
