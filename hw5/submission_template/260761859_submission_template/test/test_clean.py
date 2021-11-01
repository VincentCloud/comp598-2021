import unittest
from pathlib import Path
import os, sys
from src.clean import pipeline
import tempfile
import ast

parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class CleanTest(unittest.TestCase):
    def setUp(self):
        # load fixture files
        self.fixtures = {
            'no title or title_text': Path(f'{parentdir}/test/fixtures/test_1.json'),
            'invalid createdAt dates': Path(f'{parentdir}/test/fixtures/test_2.json'),
            'invalid json': Path(f'{parentdir}/test/fixtures/test_3.json'),
            'invalid author': Path(f'{parentdir}/test/fixtures/test_4.json'),
            'total_count cast to int': Path(f'{parentdir}/test/fixtures/test_5.json'),
            'tags get split': Path(f'{parentdir}/test/fixtures/test_6.json'),
        }

    def unittest_helper(self, fixture_key, expected_str):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_str = pipeline(self.fixtures[fixture_key], f'{tmpdir}/tmp.json')
        self.assertEqual(output_str, expected_str)

    def test_no_title_title_text(self):
        # load the fixture
        self.unittest_helper('no title or title_text', '')

    def test_invalid_dates(self):
        self.unittest_helper('invalid createdAt dates', '')

    def test_invalid_json(self):
        self.unittest_helper('invalid json', '')

    def test_invalid_author(self):
        self.unittest_helper('invalid author', '')

    def test_total_count(self):
        self.unittest_helper('total_count cast to int', '')

    def test_tags_gets_split(self):
        expected_str = "{'title': 'First title', 'createdAt': '2020-10-19T02:56:51+00:00', 'text': 'Some post " \
                       "content', 'author': 'druths', 'total_count': 12, 'tags': ['nba', 'basketball', 'game', " \
                       "'soccer']}\n"
        with tempfile.TemporaryDirectory() as tmpdir:
            output_str = pipeline(self.fixtures['tags get split'], f'{tmpdir}/tmp.json')

        expected_data = ast.literal_eval(expected_str)
        output_data = ast.literal_eval(output_str)

        self.assertEqual(len(output_data['tags']), len(expected_data['tags']))


if __name__ == '__main__':
    unittest.main()
