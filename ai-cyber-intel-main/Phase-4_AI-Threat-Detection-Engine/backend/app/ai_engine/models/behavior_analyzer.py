class BehaviorAnalyzer:
    def analyze(self, features: dict[str, float]) -> list[str]:
        flags = []
        if features["failed_login_count"] >= 5:
            flags.append("multiple_failed_logins")
        if features["new_device"]:
            flags.append("new_device")
        if features["location_changed"]:
            flags.append("location_change")
        if features["abnormal_time"]:
            flags.append("abnormal_activity_time")
        if features["frequency_ratio"] >= 3:
            flags.append("activity_frequency_spike")
        if features["unknown_ip"]:
            flags.append("unknown_ip")
        return flags
