import boto3
from botocore.exceptions import ClientError

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "Aiden Yang <aiden.yang@texasjusticeinitiative.org>"

# Replace recipient@example.com with a "To" address. If your account
# is still in the sandbox, this address must be verified.
RECIPIENTS = ["aiden.yang@texasjusticeinitiative.org",
                "eva.ruth@texasjusticeinitiative.org"]

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-east-1"

# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses', region_name=AWS_REGION)


def send_success_email(action, dataset):
    subject = "{} {} SUCCESS".format(action.capitalize(), dataset)
    success_html = """<html>
        <head></head>
        <body>
          <h1>{0} {1} dataset SUCCESS</h1>
          <p>{0} {1} was cleaned successfully</p>
        </body>
        </html> """.format(action.capitalize(), dataset)
    send_email(subject, success_html)


def send_fail_clean_email(action, dataset):
    subject = "{0} {1} FAIL".format(action.capitalize(), dataset)
    failed_html = """<html>
            <head></head>
            <body>
              <h1>{0} {} dataset FAILED</h1>
              <p>s dataset cleaning failed</p>
            </body>
            </html> """ .format(action.capitalize(), dataset)
    send_email(subject, failed_html)


def send_email(subject, body):
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body,
                    }
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

