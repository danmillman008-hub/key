import unittest
from planner.schedule import build, subtract, union, test_count


def task(key, **extra):
    return dict(id=key, subject='زیست یازدهم', topic='نمونهٔ مصنوعی', detail='مطالعه',
                duration_minutes=75, tests=0, **extra)


def day(date='2026-10-18', **extra):
    return dict(date=date, awake_windows=[['08:00','12:00']], reserve_minutes=30, **extra)


class ScheduleTests(unittest.TestCase):
    def test_union(self):
        self.assertEqual(union([(1,5),(3,7)]),[(1,7)])
        self.assertEqual(subtract([(0,10)],[(2,6),(7,9)]),[(0,2),(6,7),(9,10)])

    def test_count(self):
        self.assertEqual(test_count(75,5,2,1.5),20)
        self.assertEqual(test_count(75,5,3,2),14)
        with self.assertRaises(ValueError): test_count(75,0,0,0)

    def test_blocked_break_reserve(self):
        d=day(blocked=[['09:00','10:00'],['09:30','10:30']]); d['reserve_minutes']=15
        result=build(dict(days=[d], tasks=[task('a'),task('b')]))
        self.assertEqual(result['days'][0]['free_minutes'],150)
        self.assertEqual(result['tasks'][0]['start'],'10:30')
        self.assertEqual(len(result['unscheduled']),1)

    def test_gap(self):
        result=build(dict(days=[day(),day('2026-10-19'),day('2026-10-20')],
                    tasks=[task('learn'),task('test',after=['learn'],min_gap_days=2)]))
        self.assertEqual(result['tasks'][1]['date'],'2026-10-20')

    def test_completed_gap(self):
        result=build(dict(days=[day()],completed_task_ids=['old'],completed_dates={'old':'2026-10-16'},
                         tasks=[task('test',after=['old'],min_gap_days=2)]))
        self.assertEqual(len(result['tasks']),1)

    def test_missing_dated_completion(self):
        with self.assertRaises(ValueError):
            build(dict(days=[day()],completed_task_ids=['old'],tasks=[task('a',after=['old'],min_gap_days=2)]))

    def test_cycle(self):
        with self.assertRaises(ValueError):
            build(dict(days=[day()],tasks=[task('a',after=['b']),task('b',after=['a'])]))

    def test_long_task(self):
        t=task('a'); t['duration_minutes']=100
        with self.assertRaises(ValueError): build(dict(days=[day()],tasks=[t]))

    def test_duplicate(self):
        with self.assertRaises(ValueError): build(dict(days=[day()],tasks=[task('a'),task('a')]))

    def test_no_fabricated_tests(self):
        t=task('a'); t['tests']=None
        r=build(dict(days=[day()],tasks=[t]))
        self.assertEqual(r['totals']['unknown_test_boxes'],1)
        self.assertIsNone(r['tasks'][0]['tests'])

    def test_expired(self):
        r=build(dict(days=[day()],tasks=[task('a',due='2026-10-17')]))
        self.assertEqual(r['status'],'partial_requires_review')

    def test_overnight_and_overlap(self):
        for w in [[['23:00','06:00']],[['08:00','10:00'],['09:00','11:00']]]:
            d=day();d['awake_windows']=w
            with self.assertRaises(ValueError): build(dict(days=[d],tasks=[]))

    def test_unknown_dep(self):
        with self.assertRaises(ValueError): build(dict(days=[day()],tasks=[task('a',after=['x'])]))

    def test_adjacent(self):
        r=build(dict(days=[day()],tasks=[task('a'),task('z',after=['a'],prefer_adjacent=True),task('b')]))
        self.assertEqual([x['id'] for x in r['tasks']],['a','z'])
        self.assertEqual(r['tasks'][1]['start'],'09:30')

    def test_impossible_reserve(self):
        d=day();d['reserve_minutes']=241
        with self.assertRaises(ValueError):build(dict(days=[d],tasks=[]))


if __name__ == '__main__': unittest.main()
