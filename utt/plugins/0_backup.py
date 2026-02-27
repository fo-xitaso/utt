# -b, --backup
# optional: filepath (default is the same as the data file with timestamp + .bak extension)

import argparse
from pathlib import Path

from ..api import _v1


class BackupHandler:
    def __init__(
        self,
        args: argparse.Namespace,
        now: _v1.Now,
        output: _v1.Output,
        backup: _v1._private.Backup,
    ):
        self._args = args
        self._now = now
        self._output = output
        self._backup = backup

    def __call__(self):
        backup_path = self._backup(self._args.filepath, self._args.overwrite, self._now)
        print(f"Backup created. (path: {backup_path})", file=self._output)


def add_args(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-f", "--filepath",
        help="optional: filepath (default is the same as the data file with timestamp + .bak extension)",
        type=Path,
        default=None
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="Allow overwriting an existing backup file (use with caution)",
    )


add_command = _v1.Command("backup", "Backup the current data file", BackupHandler, add_args)

_v1.register_command(add_command)
