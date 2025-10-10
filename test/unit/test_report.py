import datetime
import unittest

from utt.components.report_args import SortBy
from utt.data_structures.activity import Activity
from utt.report.common import timedelta_to_billable
from utt.report.projects.model import ProjectsModel

TEST_CASES = [
    (dict(minutes=0), " 0.0"),
    (dict(minutes=1), " 0.0"),
    (dict(minutes=2), " 0.0"),
    (dict(minutes=3), " 0.1"),
    (dict(minutes=4), " 0.1"),
    (dict(minutes=5), " 0.1"),
    (dict(minutes=6), " 0.1"),
    (dict(minutes=7), " 0.1"),
    (dict(minutes=8), " 0.1"),
    (dict(minutes=9), " 0.2"),
    (dict(minutes=14), " 0.2"),
    (dict(minutes=15), " 0.3"),
    (dict(minutes=30), " 0.5"),
    (dict(minutes=56), " 0.9"),
    (dict(minutes=57), " 1.0"),
    (dict(minutes=60), " 1.0"),
    (dict(minutes=62), " 1.0"),
    (dict(minutes=63), " 1.1"),
    (dict(minutes=66), " 1.1"),
    # NOTE, utt doesn't really deal with seconds, but this is how the
    #   rounding would work if it did.
    (dict(seconds=1), " 0.0"),
    (dict(seconds=179), " 0.0"),
    (dict(seconds=180), " 0.1"),
    (dict(seconds=181), " 0.1"),
    (dict(seconds=359), " 0.1"),
    (dict(seconds=360), " 0.1"),
    (dict(seconds=361), " 0.1"),
]


class TestTimedeltaToBillable(unittest.TestCase):
    def test_timedelta_to_billable(self):
        """Ensure that _timedelta_to_billable gives intended outcome.

        Hours are divided in 10, and we round up to the next "6 minute unit".
        """
        for delta, billable in TEST_CASES:
            with self.subTest(delta=delta, billable=billable):
                self.assertEqual(timedelta_to_billable(datetime.timedelta(**delta)), billable)


class TestProjectTasksSorting(unittest.TestCase):

    TEST_ACTIVITIES = [
        ("asc", "a, b, c"),
        ("desc", "c, b, a"),
        ("date_asc", "c, a, b"),
        ("date_desc", "b, a, c"),
        ("duration_asc", "a, c, b"),
        ("duration_desc", "b, c, a"),
    ],

    def test_project_tasks_sort_by(self):

        test_activities = [
            Activity("Project: a", datetime.datetime(2024, 1, 1, 6, 0), datetime.datetime(2024, 1, 1, 7, 0), False, None),
            Activity("Project: b", datetime.datetime(2024, 1, 1, 7, 0), datetime.datetime(2024, 1, 1, 10, 0), False, None),
            Activity("Project: c", datetime.datetime(2024, 1, 1, 5, 0), datetime.datetime(2024, 1, 1, 7, 0), False, None),
        ]

        for sort_by_value, expected in self.TEST_ACTIVITIES:
            sort_by = SortBy(sort_by_value)
            with self.subTest(sort_by=sort_by, expected=expected):
            
                model = ProjectsModel(test_activities, sort_by)

                result: str = model.projects[0]["name"]
                assert result == expected