import json
import pathlib
import unittest


class CandidateTableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables = json.loads((pathlib.Path(__file__).parents[1] / 'data/maz_tables.json').read_text())

    def test_coordinate_integrity(self):
        for t in self.tables:
            self.assertEqual(len(t['cells']), t['rows'] * t['columns'])
            keys = {(c['row'], c['column']) for c in t['cells']}
            self.assertEqual(len(keys), len(t['cells']))
            for c in t['cells']:
                x0, y0, x1, y1 = c['bbox']
                self.assertLess(x0, x1)
                self.assertLess(y0, y1)

    def test_aban12_not_53_duplicate_rows(self):
        found = [t for t in self.tables if '12تجربی_برنامه_مطالعاتی_1_آبان' in t['file']]
        self.assertEqual({t['pdf_page'] for t in found}, {14, 15})
        self.assertTrue(all(t['rows'] == 14 for t in found))
        self.assertTrue(all(t['columns'] == 12 for t in found))

    def test_legend_is_not_time_header(self):
        for t in self.tables:
            for c in t['cells']:
                self.assertRegex(c['time_label'], r'\d+:\d+')
