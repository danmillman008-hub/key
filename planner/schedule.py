"""Schedule already-atomized tasks. ISO Gregorian dates; local minutes, no timezone conversion.
No curriculum inference, textbook lookup or official-exam-date inference occurs here.
"""
import copy
import datetime as dt
import json
import math
import sys


def minute(value):
    if not isinstance(value, str) or len(value.split(':')) != 2:
        raise ValueError('time must be HH:MM')
    h, m = map(int, value.split(':'))
    if not (0 <= h <= 24 and 0 <= m < 60 and (h < 24 or m == 0)):
        raise ValueError('invalid time')
    return h * 60 + m


def clock(value):
    return f'{value // 60:02d}:{value % 60:02d}'


def intervals(items):
    result = []
    for item in items:
        a, b = minute(item[0]), minute(item[1])
        if a >= b:
            raise ValueError('split overnight intervals at midnight')
        result.append((a, b))
    return sorted(result)


def union(items):
    result = []
    for a, b in sorted(items):
        if result and a <= result[-1][1]:
            result[-1] = (result[-1][0], max(b, result[-1][1]))
        else:
            result.append((a, b))
    return result


def subtract(windows, blocked):
    result = []
    for a, b in windows:
        cursor = a
        for x, y in blocked:
            if y <= cursor or x >= b:
                continue
            if x > cursor:
                result.append((cursor, x))
            cursor = max(cursor, y)
            if cursor >= b:
                break
        if cursor < b:
            result.append((cursor, b))
    return result


def integer(x, name, low=0):
    if isinstance(x, bool) or not isinstance(x, int) or x < low:
        raise ValueError(f'{name} must be integer >= {low}')
    return x


def test_count(minutes, review, solve, analysis):
    if not all(isinstance(x, (int, float)) and math.isfinite(x) for x in (minutes, review, solve, analysis)):
        raise ValueError('finite rates required')
    if minutes < 0 or review < 0 or solve <= 0 or analysis < 0:
        raise ValueError('invalid rates')
    return max(0, math.floor((minutes - review) / (solve + analysis)))


def build(data):
    data = copy.deepcopy(data)
    tasks = data['tasks']
    ids = [t['id'] for t in tasks]
    if len(set(ids)) != len(ids):
        raise ValueError('duplicate task id')
    by_id = {t['id']: t for t in tasks}
    completed = set(data.get('completed_task_ids', []))
    if completed & set(ids):
        raise ValueError('completed tasks must not also appear as remaining tasks')
    max_block = integer(data.get('max_block_minutes', 75), 'max_block', 1)
    pause = integer(data.get('break_minutes', 15), 'break')
    for t in tasks:
        integer(t['duration_minutes'], 'duration', 1)
        if t['duration_minutes'] > max_block:
            raise ValueError('atomize long tasks before scheduling: ' + t['id'])
        integer(t.get('min_gap_days', 0), 'min_gap_days')
        integer(t.get('priority', 3), 'priority')
        if t.get('energy', 2) not in (1, 2, 3):
            raise ValueError('energy must be 1, 2 or 3')
        if t.get('tests') is not None:
            integer(t['tests'], 'tests')
        if t.get('min_gap_days', 0) and not t.get('after'):
            raise ValueError('gap needs a predecessor')
        for key in ('not_before', 'due'):
            if key in t:
                dt.date.fromisoformat(t[key])
        for dep in t.get('after', []):
            if dep not in by_id and dep not in completed:
                raise ValueError('unknown prerequisite ' + dep)
            if dep in completed and t.get('min_gap_days', 0):
                if dep not in data.get('completed_dates', {}):
                    raise ValueError('dated completion required for gap')
                dt.date.fromisoformat(data['completed_dates'][dep])
    visiting, visited = set(), set()
    def visit(key):
        if key in visiting:
            raise ValueError('dependency cycle')
        if key in visited or key not in by_id:
            return
        visiting.add(key)
        for dep in by_id[key].get('after', []):
            visit(dep)
        visiting.remove(key)
        visited.add(key)
    for key in ids:
        visit(key)
    days = sorted(data['days'], key=lambda d: d['date'])
    if len({d['date'] for d in days}) != len(days):
        raise ValueError('duplicate date')
    pending = dict(by_id)
    done = {key: {'date': data.get('completed_dates', {}).get(key), 'end': 0} for key in completed}
    output, capacity = [], []
    for day in days:
        date = dt.date.fromisoformat(day['date'])
        windows = intervals(day['awake_windows'])
        if sum(b-a for a,b in windows) != sum(b-a for a,b in union(windows)):
            raise ValueError('overlapping awake windows')
        free = subtract(windows, union(intervals(day.get('blocked', []))))
        available = sum(b-a for a,b in free)
        reserve = integer(day['reserve_minutes'], 'reserve')
        if reserve > available:
            raise ValueError('reserve exceeds free time')
        # Withhold a physical tail of free time; never fill reserve by default.
        work, keep = [], available - reserve
        for a,b in free:
            take = min(keep, b-a)
            if take:
                work.append((a, a+take))
            keep -= take
        energy = day.get('energy', 2)
        if energy not in (1, 2, 3):
            raise ValueError('energy must be 1, 2 or 3')
        last_end = None
        last_id = None
        for a,b in work:
            cursor = a if last_end is None else max(a, last_end + pause)
            while cursor < b:
                candidates = []
                for t in pending.values():
                    if cursor + t['duration_minutes'] > b:
                        continue
                    if t.get('not_before', day['date']) > day['date'] or t.get('due', day['date']) < day['date']:
                        continue
                    deps = t.get('after', [])
                    if any(dep not in done for dep in deps):
                        continue
                    eligible = True
                    for dep in deps:
                        record = done[dep]
                        if record['date'] is None:
                            continue
                        dd = dt.date.fromisoformat(record['date'])
                        if (date-dd).days < t.get('min_gap_days', 0):
                            eligible = False
                        if dd == date and record['end'] > cursor:
                            eligible = False
                    if eligible:
                        candidates.append(t)
                if not candidates:
                    break
                # Heuristic only: deadlines/priority first, then immediate practice and energy fit.
                t = min(candidates, key=lambda x: (x.get('priority',3), x.get('due','9999-12-31'),
                    0 if x.get('prefer_adjacent') and last_id in x.get('after',[]) else 1,
                    abs(x.get('energy',2)-energy), x['id']))
                end = cursor + t['duration_minutes']
                output.append({**t, 'date':day['date'], 'start':clock(cursor), 'end':clock(end),
                               'hours':t['duration_minutes']/60, 'tests':t.get('tests'),
                               'provenance':t.get('provenance','PROPOSED')})
                done[t['id']] = {'date':day['date'], 'end':end}
                del pending[t['id']]
                last_id, last_end = t['id'], end
                cursor = end + pause
        capacity.append({'date':day['date'], 'free_minutes':available, 'reserved_minutes':reserve,
                         'scheduled_minutes':sum(t['duration_minutes'] for t in output if t['date']==day['date'])})
    remaining = [{**t, 'reason':'not_scheduled_by_heuristic; inspect capacity, dates, prerequisites and gaps'} for t in pending.values()]
    return {'status':'draft_complete' if not remaining else 'partial_requires_review',
            'method':'PROPOSED greedy scheduler; not a proof of feasibility or optimality',
            'tasks':output, 'unscheduled':remaining, 'days':capacity,
            'totals':{'study_minutes':sum(t['duration_minutes'] for t in output),
                      'known_tests':sum(t['tests'] or 0 for t in output),
                      'unknown_test_boxes':sum(t['tests'] is None for t in output)}}


if __name__ == '__main__':
    try:
        with open(sys.argv[1], encoding='utf-8') as stream:
            result = build(json.load(stream))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, KeyError, TypeError, IndexError) as exc:
        print(f'Invalid input: {exc}', file=sys.stderr)
        sys.exit(2)
