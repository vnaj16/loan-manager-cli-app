"""This module provides the Loan Manager model-controller."""
# loan_manager\loan_manager.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from loan_manager import DB_READ_ERROR

from loan_manager.database import DatabaseHandler

class CurrentLoan(NamedTuple):
    loan: Dict[str, Any]
    error: int

class LoanRepository:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, description: List[str], amount: float) -> CurrentLoan:
        """Add a new loan to the database."""
        description_text = " ".join(description)
        if not description_text.endswith("."):
            description_text += "."
        todo = {
            "Description": description_text,
            "Amount": amount,
            "Paid": False,
        }
        read = self._db_handler.read_loans()
        if read.error == DB_READ_ERROR:
            return CurrentLoan(todo, read.error)
        read.loan_list.append(todo)
        write = self._db_handler.write_loans(read.loan_list)
        return CurrentLoan(todo, write.error)

    def get_todo_list(self) -> List[Dict[str, Any]]:
        """Return the current loan list."""
        read = self._db_handler.read_loans()
        return read.loan_list

    # def set_done(self, todo_id: int) -> CurrentLoan:
    #     """Set a to-do as done."""
    #     read = self._db_handler.read_todos()
    #     if read.error:
    #         return CurrentTodo({}, read.error)
    #     try:
    #         todo = read.todo_list[todo_id - 1]
    #     except IndexError:
    #         return CurrentTodo({}, ID_ERROR)
    #     todo["Done"] = True
    #     write = self._db_handler.write_todos(read.todo_list)
    #     return CurrentTodo(todo, write.error)

    # def remove(self, todo_id: int) -> CurrentTodo:
    #     """Remove a to-do from the database using its id or index."""
    #     read = self._db_handler.read_todos()
    #     if read.error:
    #         return CurrentTodo({}, read.error)
    #     try:
    #         todo = read.todo_list.pop(todo_id - 1)
    #     except IndexError:
    #         return CurrentTodo({}, ID_ERROR)
    #     write = self._db_handler.write_todos(read.todo_list)
    #     return CurrentTodo(todo, write.error)

    # def remove_all(self) -> CurrentTodo:
    #     """Remove all to-dos from the database."""
    #     write = self._db_handler.write_todos([])
    #     return CurrentTodo({}, write.error)