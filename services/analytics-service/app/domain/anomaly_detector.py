from collections import defaultdict
from statistics import mean
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta, timezone


class AnomalyDetector:

    def __init__(self):

        # historical cost per (account_id, service)
        self.history: Dict[Tuple[str, str], List[float]] = defaultdict(list)

        # last anomaly timestamp per resource
        self.last_anomaly_time: Dict[Tuple[str, str], datetime] = {}

        # cooldown window to prevent alert flooding
        self.cooldown = timedelta(minutes=10)

    def check_anomaly(
        self,
        account_id: str,
        service: str,
        cost: float
    ) -> Optional[dict]:

        key = (account_id, service)
        history = self.history[key]

        now = datetime.now(timezone.utc)
        result = None

        # 🔴 PHASE 1 — Cold Start (0–1 data points)
        if len(history) < 2:
            expected_cost = cost
            result = None

        # 🟡 PHASE 2 — Weak Pattern (2 data points)
        elif len(history) == 2:

            growth = history[1] - history[0]
            expected_cost = history[-1] + growth

            deviation = cost - expected_cost
            ratio = deviation / expected_cost if expected_cost else 0

            if abs(ratio) > 0.7:  # stricter threshold

                last_time = self.last_anomaly_time.get(key)

                if not last_time or (now - last_time) >= self.cooldown:
                    result = {
                        "expected_cost": expected_cost,
                        "deviation": deviation,
                        "anomaly_type": "spike" if ratio > 0 else "drop",
                        "confidence": "low"
                    }

                    self.last_anomaly_time[key] = now

        # 🟢 PHASE 3 — Stable Pattern (≥3 data points)
        else:

            growths = [
                history[i] - history[i - 1]
                for i in range(1, len(history))
            ]

            avg_growth = mean(growths)
            expected_cost = history[-1] + avg_growth

            deviation = cost - expected_cost
            ratio = deviation / expected_cost if expected_cost else 0

            if abs(ratio) > 0.5:

                last_time = self.last_anomaly_time.get(key)

                if not last_time or (now - last_time) >= self.cooldown:
                    result = {
                        "expected_cost": expected_cost,
                        "deviation": deviation,
                        "anomaly_type": "spike" if ratio > 0 else "drop",
                        "confidence": "high"
                    }

                    self.last_anomaly_time[key] = now

        # 🔄 Store new value AFTER evaluation
        history.append(cost)

        # keep last 20 points (sliding window)
        if len(history) > 20:
            history.pop(0)

        return result