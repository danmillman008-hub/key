"""Checks of the manual transcription, NOT a claim of a universal MAZ algorithm."""
import collections
import json
from pathlib import Path
import unittest


class VerifiedMazCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = json.loads((Path(__file__).parents[1] / 'data/verified_12T_case.json').read_text())
        cls.cells = [c for day in cls.case['days'] for c in day['cells']]

    def units(self, kind):
        return {(u['subject'], u['unit']) for c in self.cells if c['kind'] == kind for u in c['units']}

    def test_exact_box_accounting(self):
        c = collections.Counter(x['kind'] for x in self.cells)
        self.assertEqual(dict(c), dict(L=34, T=22, R=8, F=13, S=30, H=10))
        self.assertEqual(len(self.cells), 13 * 9)
        self.assertEqual((c['L'] + c['T'] + c['R']) * 90, 96 * 60)

    def test_daily_flex_is_real_box(self):
        for day in self.case['days']:
            self.assertEqual([c['column'] for c in day['cells'] if c['kind'] == 'F'], [6])

    def test_grouped_review_and_test_units(self):
        self.assertEqual(len(self.units('R')), 20)
        self.assertEqual(len(self.units('T')), 36)
        self.assertEqual(len(self.units('L')), 35)
        self.assertEqual(self.units('T') - self.units('L'), {('chem10', 7)})

    def test_sample_delayed_biology_and_earth(self):
        starts = {}
        for di, day in enumerate(self.case['days']):
            for c in day['cells']:
                h, m = map(int, self.case['slots'][c['column']][0].split(':'))
                timestamp = di * 1440 + h * 60 + m
                for u in c['units']:
                    key = (u['subject'], u['unit'])
                    if c['kind'] == 'L':
                        starts[key] = timestamp
                    if c['kind'] == 'T' and u['subject'] in ('bio10', 'bio12', 'earth11'):
                        self.assertIn(key, starts)
                        self.assertGreaterEqual(timestamp - starts[key], 48 * 60)

    def test_first_thursday_is_not_empty(self):
        day = self.case['days'][6]
        self.assertEqual(day['weekday'], 'پنجشنبه')
        self.assertEqual(collections.Counter(c['kind'] for c in day['cells']), dict(L=5, T=3, F=1))
