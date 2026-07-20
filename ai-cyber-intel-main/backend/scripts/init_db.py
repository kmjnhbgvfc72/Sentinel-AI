"""Create missing central database tables without deleting existing data."""

from backend.database import initialize_database
from backend.scripts.database_cli import database_connection_error
from sqlalchemy.exc import OperationalError


def main() -> None:
    try:
        initialize_database()
    except OperationalError as exc:
        raise database_connection_error(exc) from None
    print("Central database initialization completed.")


if __name__ == "__main__":
    main()
