import pandas as pd

FEATURE_COLUMNS = ["failed_login_count", "ioc_reputation", "vulnerability_score", "frequency_ratio", "unknown_ip", "new_device", "location_changed", "abnormal_time", "malware_indicator", "severity_value", "data_access_log"]


def feature_frame(records: list[dict[str, float]]) -> pd.DataFrame:
    frame = pd.DataFrame(records)
    for column in FEATURE_COLUMNS:
        if column not in frame:
            frame[column] = 0.0
    return frame[FEATURE_COLUMNS].astype(float).fillna(0.0)
