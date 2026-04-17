from shared.broker.sqs_broker import SQSBroker


def get_broker() -> SQSBroker:
    """
    Factory for SQS Broker.
    Replaces Redis with SQS.
    """
    return SQSBroker()