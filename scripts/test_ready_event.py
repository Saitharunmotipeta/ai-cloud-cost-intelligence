from datetime import datetime,timezone
from shared.events.cost_data_ready_for_analysis_v1 import (
    CostDataReadyForAnalysisEvent,
    CostDataReadyForAnalysisPayload
)

event = CostDataReadyForAnalysisEvent(
    source="analytics-service",
    payload=CostDataReadyForAnalysisPayload(
        account_id="acc-123",
        service="EC2",
        cost=42.5,
        usage_timestamp=datetime.now(timezone.utc)
    )
)

print(event.to_json())