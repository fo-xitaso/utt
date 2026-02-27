import configparser

DEFAULTS = {
    "timezone": {"enabled": "false"},
    "report": {"project_tasks_sort_by": "asc"}
}

class DefaultConfig:
    def __init__(self):
        pass

    def __call__(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser()

        for section, options in DEFAULTS.items():
            config.add_section(section)

            for option, value in options.items():
                config.set(section, option, value)

        return config
