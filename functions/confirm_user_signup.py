import json
import logging
import os
import datetime
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    logger.info('Event: {}'.format(event))

    user_table = os.environ["USERS_TABLE"]

    if event['triggerSource'] == 'PostConfirmation_ConfirmSignUp':
        user_sub = event['request']['userAttributes']['sub']
        user_name = event['request']['userAttributes']['name']
        user_email = event['request']['userAttributes']['email']
        user_status = event['request']['userAttributes']['cognito:user_status']
        user_email_status = event['request']['userAttributes']['email_verified']

        user = {
            'id': {
                'S': user_sub
            },
            'name': {
                'S': user_name
            },
            'email': {
                'S': user_email
            },
            'status': {
                'S': user_status
            },
            'email_status': {
                'S': user_email_status
            },
            'createdOn': {
                'S': datetime.datetime.now().astimezone().isoformat()
            }
        }

        dynamodb_client.put_item(
            TableName = user_table,
            Item = user,
            ConditionExpression = 'attribute_not_exists(id)'
        )
        return event
    else:
        return event