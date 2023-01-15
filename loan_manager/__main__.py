"""Loan Manager CLI App entry point script."""
# loan_manager/__main__.py

from loan_manager import cli, __app_name__

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()