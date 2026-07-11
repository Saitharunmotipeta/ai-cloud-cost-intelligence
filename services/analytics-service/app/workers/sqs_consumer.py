import boto3
import json
import os
from shared.observability.metrics import (
    start_timer,
    stop_timer,
)

sqs = boto3.client(
    "sqs",
    region_name=os.getenv("AWS_DEFAULT_REGION")
)

QUEUE_URL = os.getenv("INGESTION_QUEUE_URL")


def poll_messages():
    print("🚀 Analytics consumer started...")

    while True:
        loop_timer = start_timer()
        receive_timer = start_timer()

        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=10
        )

        receive_ms = stop_timer(receive_timer)

        messages = response.get("Messages", [])

        print(
            f"📥 Queue Receive Time : {receive_ms:.2f} ms"
        )

        for msg in messages:
            body = json.loads(msg["Body"])

            print("📩 Received event:", body)

            # 🔥 For now just log it (no processing yet)

            processing_timer = start_timer()

            # anomaly detection
            # publish next event
            # any future processing

            processing_ms = stop_timer(processing_timer)

            print(
                f"📊 Processing Time : {processing_ms:.2f} ms"
            )
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"]
            )

        loop_ms = stop_timer(loop_timer)

        print(
            f"⏱ Analytics Loop : {loop_ms:.2f} ms"
        )