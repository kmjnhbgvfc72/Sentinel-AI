import argparse, subprocess, tempfile
from pathlib import Path

def restore_test(dump: str, target_url: str):
    source=Path(dump).resolve(strict=True)
    subprocess.run(["pg_restore", "--clean", "--if-exists", "--no-owner", "--dbname", target_url, str(source)], check=True)
    subprocess.run(["psql", target_url, "--command", "SELECT count(*) FROM threats; SELECT count(*) FROM response_audit;"], check=True)

if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("dump"); p.add_argument("target_url"); a=p.parse_args(); restore_test(a.dump,a.target_url)

