"""Transparent workload estimates, independent of calendar placement (minutes).
Rates and importance are supplied observations, not official MAZ coefficients.
python -m planner.workload input.json
"""
import json
import math
import sys


def number(value, name, low=0, high=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(name + ' must be finite numeric')
    if value < low or (high is not None and value > high):
        raise ValueError(name + ' out of range')
    return value


def estimate(topic):
    """remaining_units exclude verified completed or class-mastered units already.
    Analysis is included in practice; retrieval/review are separate, never counted twice.
    No automatic subtraction merely for attending class.
    """
    units = number(topic['remaining_units'], 'remaining_units')
    rate = number(topic['learn_minutes_per_unit'], 'learn rate')
    questions = topic['questions']
    if isinstance(questions, bool) or not isinstance(questions, int) or questions < 0:
        raise ValueError('questions must be nonnegative integer')
    solve = number(topic['solve_minutes'], 'solve', low=0.000001)
    analysis = number(topic['analysis_minutes'], 'analysis')
    review = number(topic.get('review_minutes', 0), 'review')
    learn = math.ceil(units * rate)
    practice = math.ceil(questions * (solve + analysis))
    total = learn + practice + math.ceil(review)
    return dict(id=topic['id'], learn_minutes=learn, practice_including_analysis_minutes=practice,
                review_minutes=math.ceil(review), total_minutes=total,
                learning_share_of_learn_practice=learn / (learn + practice) if learn + practice else None)


def budget(data):
    capacity = number(data['net_capacity_minutes'], 'capacity')
    # Net capacity is AFTER blocked events and breaks, BEFORE these explicit reserves.
    reserve = number(data.get('reserve_minutes', 0), 'reserve')
    fixed = number(data.get('fixed_school_and_exam_minutes', 0), 'fixed')
    if reserve + fixed > capacity:
        raise ValueError('reserves and fixed work exceed capacity')
    estimates = [estimate(t) for t in data['topics']]
    if len({t['id'] for t in estimates}) != len(estimates):
        raise ValueError('duplicate topic id')
    available = math.floor(capacity - reserve - fixed)
    demand = sum(t['total_minutes'] for t in estimates)
    return dict(status='volume_fits_calendar_unverified' if demand <= available else 'volume_deficit',
                available_minutes=available, required_minutes=demand,
                deficit_minutes=max(0, demand - available),
                spare_minutes=max(0, available - demand), estimates=estimates,
                warning='Do not proportionally shrink prerequisites, sleep or analysis. Select coherent topic packages; then check the calendar with planner.schedule.')


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as source:
        print(json.dumps(budget(json.load(source)), ensure_ascii=False, indent=2))
