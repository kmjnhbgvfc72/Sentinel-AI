import argparse, time, urllib.request

def verify(url: str, attempts: int = 12):
    failures=[]
    for _ in range(attempts):
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                if response.status != 200: failures.append(response.status)
        except Exception as exc: failures.append(str(exc))
        time.sleep(1)
    if len(failures) > 2: raise SystemExit(f"Failover SLO failed: {failures}")

if __name__ == "__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("url"); args=parser.parse_args(); verify(args.url)

