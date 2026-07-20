import argparse
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path


def backup(output_dir: str, database_url: str) -> Path:
    directory = Path(output_dir).resolve(); directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    target = directory / f"soc-{datetime.now(UTC):%Y%m%dT%H%M%SZ}.dump"
    subprocess.run(["pg_dump", "--format=custom", "--no-owner", "--file", str(target), database_url], check=True)
    target.chmod(0o600)
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--output", default="backups")
    args = parser.parse_args(); print(backup(args.output, os.environ["DATABASE_URL"]))

