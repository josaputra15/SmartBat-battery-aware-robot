"""logger.py — CSV telemetry logger."""

import csv
import time
from datetime import datetime
import config


class DataLogger:
    """Writes timestamped telemetry to a CSV file."""

    HEADER = [
        "timestamp",
        "elapsed_s",
        "battery_v",
        "battery_pct",
        "battery_state",
        "distance_cm",
        "action",
        "speed",
        "reason",
    ]

    def __init__(self, filepath: str = None):
        self.filepath = filepath or config.LOG_FILE
        self.enabled = config.LOG_ENABLED
        self._start_time = time.time()
        self._file = None
        self._writer = None

        if self.enabled:
            self._file = open(self.filepath, "w", newline="", encoding="utf-8")
            self._writer = csv.writer(self._file)
            self._writer.writerow(self.HEADER)

    def log(
        self,
        battery_v: float,
        battery_pct: int,
        battery_state: str,
        distance_cm: float,
        action: str,
        speed: int,
        reason: str,
    ):
        if not self.enabled or self._writer is None:
            return

        elapsed = round(time.time() - self._start_time, 2)
        row = [
            datetime.now().isoformat(timespec="milliseconds"),
            elapsed,
            battery_v,
            battery_pct,
            battery_state,
            distance_cm,
            action,
            speed,
            reason,
        ]
        self._writer.writerow(row)
        self._file.flush()

    def close(self):
        if self._file:
            self._file.close()
            self._file = None
            self._writer = None
            print(f"  [LOGGER] Data saved to {self.filepath}")
