"""This module provides the Loan Manager CLI App database functionality."""
# loan_manager/database.py

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple


from loan_manager import DB_READ_ERROR, DB_WRITE_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

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

class DBResponse(NamedTuple):
    loan_list: List[Dict[str, Any]]
    error: int

class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_loans(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR)
        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)

    def write_loans(self, loan_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(loan_list, db, indent=4)
            return DBResponse(loan_list, SUCCESS)
        except OSError:  # Catch file IO problems
            return DBResponse(loan_list, DB_WRITE_ERROR)