import unittest
from planner.workload import estimate, budget


class WorkloadTests(unittest.TestCase):
    def topic(self, **changes):
        t = dict(id='bio1', remaining_units=9, learn_minutes_per_unit=5,
                 questions=20, solve_minutes=2, analysis_minutes=1.5, review_minutes=10)
        t.update(changes)
        return t

    def test_measured_demand(self):
        x = estimate(self.topic())
        self.assertEqual((x['learn_minutes'], x['practice_including_analysis_minutes'], x['total_minutes']), (45, 70, 125))

    def test_class_mastery_is_explicit(self):
        x = estimate(self.topic(remaining_units=0))
        self.assertEqual(x['learn_minutes'], 0)
        self.assertEqual(x['total_minutes'], 80)

    def test_volume_fit_does_not_claim_calendar_fit(self):
        x = budget(dict(net_capacity_minutes=180, reserve_minutes=30, topics=[self.topic()]))
        self.assertEqual(x['status'], 'volume_fits_calendar_unverified')
        self.assertEqual(x['spare_minutes'], 25)

    def test_deficit_is_not_hidden(self):
        x = budget(dict(net_capacity_minutes=150, reserve_minutes=30,
                        fixed_school_and_exam_minutes=20, topics=[self.topic()]))
        self.assertEqual(x['deficit_minutes'], 25)
        self.assertEqual(x['estimates'][0]['total_minutes'], 125)

    def test_invalid_inputs(self):
        for changes in [dict(remaining_units=-1), dict(questions=1.5),
                        dict(solve_minutes=0), dict(analysis_minutes=float('nan'))]:
            with self.assertRaises(ValueError):
                estimate(self.topic(**changes))

    def test_legacy_arithmetic(self):
        # Preserved reference baseline, not a universal prescription.
        learn = [180, 60, 120, 180]
        practice = [720, 600, 600, 360]
        questions = [120, 150, 150, 75]
        self.assertEqual(sum(learn) + sum(practice), 47 * 60)
        self.assertEqual(sum(questions), 495)
        self.assertAlmostEqual(sum(learn) / (47 * 60), 9 / 47)

    def test_duplicate_topics(self):
        with self.assertRaises(ValueError):
            budget(dict(net_capacity_minutes=500, topics=[self.topic(), self.topic()]))
