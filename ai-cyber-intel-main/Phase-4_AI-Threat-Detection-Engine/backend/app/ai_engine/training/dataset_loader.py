from pathlib import Path

import pandas as pd


def load_dataset(path: str | Path) -> pd.DataFrame:
    source = Path(path).resolve()
    if source.suffix.lower() != ".csv" or not source.is_file():
        raise ValueError("Training dataset must be an existing CSV file")
    frame = pd.read_csv(source)
    if frame.empty:
        raise ValueError("Training dataset is empty")
    return frame
