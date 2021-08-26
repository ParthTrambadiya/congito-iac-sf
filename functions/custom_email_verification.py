import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

email_subject = 'Confirm your email'
email_message = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Custom Email</title>
</head>
<body>
    <h1>Welcome, <span>{name}</span></h1>
    <p>We're excited to have you get started. First, you need to confirm your <span>{email}</span> To do that just click on below button.</p>
    {link}
</body>
</html>"""

def lambda_handler(event, context):
    logger.info('Event: {}'.format(event))

    if event['triggerSource'] == 'CustomMessage_SignUp':
        user_name = event['request']['userAttributes']['name']
        user_email = event['request']['userAttributes']['email']
        verification_link = event['request']['linkParameter']

        response_email_subject = email_subject
        response_email_message = email_message.format(name = user_name, email = user_email, link = verification_link)

        event['response']['emailSubject'] = response_email_subject
        event['response']['emailMessage'] = response_email_message
        return event
    else:
        return event