"""
Central definition of all Redis Streams used in the system.
Keeping them here avoids hardcoding names across services.
"""

# Core pipeline streams

COST_DATA_INGESTED_STREAM = "cost_data_ingested_v1"

COST_DATA_READY_FOR_ANALYSIS_STREAM = "cost_data_ready_for_analysis_v1"

COST_ANOMALY_DETECTED_STREAM = "cost_anomaly_detected_v1"

COST_INSIGHT_GENERATED_STREAM = "cost_insight_generated_v1"

DEAD_LETTER_STREAM = "cost_data_dead_letter_v1"