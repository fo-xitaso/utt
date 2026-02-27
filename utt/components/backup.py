import errno
import os
from pathlib import Path

from utt.components.now import Now

from .data_filename import DataFilename

class Backup:
    def __init__(self, data_filename: DataFilename, ):
        self._data_filename = data_filename
    def __call__(self, target_backup_path: Path | None, overwrite: bool, timestamp: Now) -> Path:

        if target_backup_path is None:
            target_backup_path = _create_backup_filename(self._data_filename, timestamp)
        
        target_backup_path = _normalize_path(self._data_filename, target_backup_path)

        _validate_backup_path(self._data_filename, target_backup_path, overwrite)

        _create_directories_for_file(target_backup_path)
        with open(self._data_filename, "r") as source:
            with open(target_backup_path, "w") as target:
                target.write(source.read())

        return target_backup_path


def _create_directories_for_file(filename: Path|DataFilename):
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError as err:
        # If the exception is errno.EEXIST, we ignore it
        if err.errno != errno.EEXIST:
            raise

def _normalize_path(data_filename: DataFilename, path: Path) -> Path:
    if not path.is_absolute():
        path = Path(data_filename).parent / path
    return path.expanduser().resolve()

def _validate_backup_path(data_filename: DataFilename, backup_path: Path, overwrite: bool):

    if backup_path.is_dir():
        raise IsADirectoryError(f"Backup path is a directory: {backup_path}")

    if backup_path == Path(data_filename):
        raise ValueError("Backup file path cannot be the same as the data file path.")  
     
    if backup_path.exists() and not overwrite:
        raise FileExistsError(f"Backup file already exists: {backup_path}")
    

def _create_backup_filename(data_filename: DataFilename, timestamp: Now) -> Path:
    return Path(f"{data_filename}.{timestamp.strftime('%Y%m%d_%H%M%S')}.bak")