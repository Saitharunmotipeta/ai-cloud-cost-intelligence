import boto3
import json
import os
import time

sqs = boto3.client(
    "sqs",
    region_name=os.getenv("AWS_DEFAULT_REGION")
)

QUEUE_URL = os.getenv("INGESTION_QUEUE_URL")


def poll_messages():
    print("🚀 Analytics consumer started...")

    while True:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=10
        )

        messages = response.get("Messages", [])

        for msg in messages:
            body = json.loads(msg["Body"])

            print("📩 Received event:", body)

            # 🔥 For now just log it (no processing yet)

            # Delete message after processing
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"]
            )

        time.sleep(2)