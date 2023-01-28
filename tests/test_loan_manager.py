# tests/test_loan_manager.py
import json

import pytest
from typer.testing import CliRunner

from loan_manager import (
    DB_READ_ERROR,
    SUCCESS,
    __app_name__,
    __version__,
    cli,
    loan_manager,
)

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

@pytest.fixture
def mock_json_file(tmp_path):
    todo = [{"Description": "Netflix January", "Amount": 24.9, "Paid": False}]
    db_file = tmp_path / "loan.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file

test_data1 = {
    "description": ["Payment", "Energy", "Service"],
    "amount": 150,
    "loan": {
        "Description": "Payment Energy Service.",
        "Amount": 150,
        "Paid": False,
    },
}
test_data2 = {
    "description": ["Payment", "Water", "Service"],
    "amount": 60,
    "loan": {
        "Description": "Payment Water Service.",
        "Amount": 60,
        "Paid": False,
    },
}

@pytest.mark.parametrize(
    "description, amount, expected",
    [
        pytest.param(
            test_data1["description"],
            test_data1["amount"],
            (test_data1["loan"], SUCCESS),
        ),
        pytest.param(
            test_data2["description"],
            test_data2["amount"],
            (test_data2["loan"], SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, description, amount, expected):
    loan_repository = loan_manager.LoanRepository(mock_json_file)
    assert loan_repository.add(description, amount) == expected
    read = loan_repository._db_handler.read_loans()
    assert len(read.loan_list) == 2