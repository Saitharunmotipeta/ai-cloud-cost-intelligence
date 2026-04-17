import boto3
import json
import os


class SQSBroker:
    def __init__(self):
        self.sqs = boto3.client("sqs", region_name=os.getenv("AWS_DEFAULT_REGION"))

        # Map your old stream names → SQS queues
        self.queue_map = {
            "cost_data_ingested_v1": os.getenv("INGESTION_QUEUE_URL"),
            "cost_data_ready_for_analysis_v1": os.getenv("ANALYTICS_QUEUE_URL"),
            "cost_insight_generated_v1": os.getenv("INTELLIGENCE_QUEUE_URL"),
        }

    async def publish(self, stream_name: str, event):
        queue_url = self.queue_map.get(stream_name)

        if not queue_url:
            raise ValueError(f"No queue mapped for stream: {stream_name}")

        self.sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(event.model_dump(mode="json"))
        )