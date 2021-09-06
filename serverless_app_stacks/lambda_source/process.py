import json
import logging
import os

def lambda_handler(event, context):
    global LOGGER
    LOGGER = logging.getLogger()
    LOGGER.setLevel(level=os.getenv('LOG_LEVEL', 'DEBUG').upper())

    LOGGER.info(f"recevied_event:{event}")

    return {
        "StatusCode": 200,
        "body": json.dumps({
                "message": event
            })
    }
