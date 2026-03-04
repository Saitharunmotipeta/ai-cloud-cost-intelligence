from collections import defaultdict
from statistics import mean, stdev
from typing import Dict, List, Tuple
from datetime import datetime, timedelta, timezone


class AnomalyDetector:

    def __init__(self):

        # historical cost baseline
        self.history: Dict[Tuple[str, str], List[float]] = defaultdict(list)

        # last anomaly timestamp per resource
        self.last_anomaly_time: Dict[Tuple[str, str], datetime] = {}

        # cooldown window
        self.cooldown = timedelta(minutes=10)

    def check_anomaly(self, account_id: str, service: str, cost: float):

        key = (account_id, service)
        history = self.history[key]

        now = datetime.now(timezone.utc)

        result = None

        # need baseline first
        if len(history) >= 3:

            avg = mean(history)
            deviation = stdev(history)

            threshold = avg + (2 * deviation)

            if cost > threshold:

                last_time = self.last_anomaly_time.get(key)

                # check cooldown
                if last_time and (now - last_time) < self.cooldown:
                    result = None

                else:
                    result = {
                        "expected_cost": avg,
                        "deviation": cost - avg
                    }

                    # record anomaly timestamp
                    self.last_anomaly_time[key] = now

        # store new value AFTER evaluation
        history.append(cost)

        if len(history) > 20:
            history.pop(0)

        return result