import configparser

from utt.components.default_config import DEFAULTS
from utt.components.report_args import SortBy


class ReportConfig:
    def __init__(self, project_tasks_sort_by: SortBy):
        self._project_tasks_sort_by = project_tasks_sort_by

    def project_tasks_sort_by(self) -> SortBy: 
        return self._project_tasks_sort_by


def report_config(config: configparser.ConfigParser) -> ReportConfig:
    sort_by_value = config.get("report", "project_tasks_sort_by")
    return ReportConfig(SortBy(sort_by_value))
