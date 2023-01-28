"""This module provides the Loan Manager CLI App."""
# loan_manager/cli.py

from pathlib import Path
from typing import List, Optional

import typer

from loan_manager import (
    ERRORS, __app_name__, __version__, config, database, loan_manager
)

app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="loans database location?",
    ),
) -> None:
    """Initialize the loans database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The loans database is {db_path}", fg=typer.colors.GREEN)

def get_loan_repository() -> loan_manager.LoanRepository:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "loan_manager init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return loan_manager.LoanRepository(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "loan_manager init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def add(
    description: List[str] = typer.Argument(...),
    amount: float = typer.Option(0, "--amount", "-a"),
) -> None:
    """Add a new loan with a DESCRIPTION and AMOUNT."""
    loan_repository = get_loan_repository()
    loan, error = loan_repository.add(description, amount)
    if error:
        typer.secho(
            f'Adding loan failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""Loan: "{loan['Description']}" was added """
            f"""with amount: {loan['Amount']}""",
            fg=typer.colors.GREEN,
        )

@app.command(name="list")
def list_all() -> None:
    """List all loans."""
    loan_repository = get_loan_repository()
    loan_list = loan_repository.get_todo_list()
    if len(loan_list) == 0:
        typer.secho(
            "There are no loans in the loan list yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    typer.secho("\nloan list:\n", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID.  ",
        "| Description                                       ",
        "| Amount      ",
        "| Paid  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id, loan in enumerate(loan_list, 1):
        desc, amount, paid = loan.values()
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| {desc}{(len(columns[1]) - len(str(desc)) - 2) * ' '}"
            f"| S/. {amount}{(len(columns[2]) - len(str(amount)) - 6) * ' '}"
            f"| {paid}{(len(columns[3]) - len(str(paid)) - 2) * ' '}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return