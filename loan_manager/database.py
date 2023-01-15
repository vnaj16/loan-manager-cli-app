"""This module provides the Loan Manager CLI App database functionality."""
# loan_manager/database.py

import configparser
from pathlib import Path

from loan_manager import DB_WRITE_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_loans.json"
)

def get_database_path(config_file: Path) -> Path:
    """Return the current path to the loans database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """Create the loans database."""
    try:
        db_path.write_text("[]")  # Empty loans list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR