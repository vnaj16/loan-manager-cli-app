"""This module provides the Loan Manager model-controller."""
# loan_manager\loan_manager.py

from pathlib import Path
from typing import Any, Dict, NamedTuple

from loan_manager.database import DatabaseHandler

class CurrentLoan(NamedTuple):
    loan: Dict[str, Any]
    error: int

class LoanRepository:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)