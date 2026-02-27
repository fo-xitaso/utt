from ...report.activities.model import ActivitiesModel
from ...report.details.model import DetailsModel
from ...report.per_day.model import PerDayModel
from ...report.projects.model import ProjectsModel
from ...report.summary.model import SummaryModel
from ..activities import Activities
from ..report_args import ReportArgs
from ..report_config import ReportConfig


def report(report_args: ReportArgs, filtered_activities: Activities, local_timezone: LocalTimezone, report_config: ReportConfig):
    return ReportModel(activities=filtered_activities, args=report_args, local_timezone=local_timezone, report_config=report_config)


class ReportModel:
    def __init__(self, activities: Activities, args: ReportArgs, local_timezone: LocalTimezone, report_config: ReportConfig):
        self.args = args
        self.summary_model = SummaryModel(activities, args.range)
        self.projects_model = ProjectsModel(activities, args.project_tasks_sort_by or report_config.project_tasks_sort_by())
        self.per_day_model = PerDayModel(activities)
        self.activities_model = ActivitiesModel(activities, args.activities_sort_by)
        self.details_model = DetailsModel(activities, local_timezone)
