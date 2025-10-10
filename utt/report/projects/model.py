import datetime
import itertools
from typing import Dict, List

from ...components.report_args import SortBy
from ...data_structures.activity import Activity
from .. import formatter
from ..common import filter_activities_by_type


class ProjectsModel:
    def __init__(self, activities: List[Activity], sort_by: SortBy):
        self.projects = groupby_project(filter_activities_by_type(activities, Activity.Type.WORK), sort_by)


def groupby_project(activities: List[Activity], sort_by: SortBy) -> List[Dict]:
    def key(act):
        return act.name.project

    result = []
    sorted_activities = sorted(activities, key=key)

    for project, _activities in itertools.groupby(sorted_activities, key):
        activities = list(_activities)
        result.append(
            {
                "duration": formatter.format_duration(sum((act.duration for act in activities), datetime.timedelta())),
                "project": project,
                "name": ", ".join(_tasks_sorted(activities, sort_by)),
            }
        )

    return sorted(result, key=lambda result: result["project"].lower())


def _tasks_sorted(activities: List[Activity], by: SortBy) -> List[str]:
    tasks = sorted(set(act.name.task for act in activities))
    sort_map = {
        None: lambda ts: ts,
        SortBy.asc: lambda ts: ts,
        SortBy.desc: lambda ts: list(reversed(ts)),
        SortBy.date_desc: lambda ts: sorted(
            ts, key=lambda t: max(act.start for act in activities if act.name.task == t), reverse=True
        ),
        SortBy.date_asc: lambda ts: sorted(
            ts, key=lambda t: min(act.start for act in activities if act.name.task == t)
        ),
        SortBy.duration_asc: lambda ts: sorted(
            ts,
            key=lambda t: sum(
                (act.duration for act in activities if act.name.task == t), datetime.timedelta()
            ),
        ),
        SortBy.duration_desc: lambda ts: sorted(
            ts,
            key=lambda t: sum(
                (act.duration for act in activities if act.name.task == t), datetime.timedelta()
            ),
            reverse=True,
        ),
    }
    try:
        return sort_map[by](tasks)
    except KeyError:
        raise ValueError(f"Unsupported sort key: {by}")
