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
        loop_start = time.perf_counter()
        receive_start = time.perf_counter()

        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=10
        )

        receive_ms = (
            time.perf_counter() - receive_start
        ) * 1000

        messages = response.get("Messages", [])

        print(
            f"📥 Queue Receive Time : {receive_ms:.2f} ms"
        )

        for msg in messages:
            body = json.loads(msg["Body"])

            print("📩 Received event:", body)

            # 🔥 For now just log it (no processing yet)

            processing_start = time.perf_counter()

            # anomaly detection
            # publish next event
            # any future processing

            processing_ms = (
                time.perf_counter() - processing_start
            ) * 1000

            print(
                f"📊 Processing Time : {processing_ms:.2f} ms"
            )
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"]
            )

        loop_ms = (
            time.perf_counter() - loop_start
                ) * 1000

        print(
            f"⏱ Analytics Loop : {loop_ms:.2f} ms"
        )

        time.sleep(2)