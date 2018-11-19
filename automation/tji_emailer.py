import boto3
import logging
from botocore.exceptions import ClientError

CHARSET = "UTF-8"


class TJIEmailer():
    def __init__(self, sender, recipients, aws_region):
        self.sender = sender
        self.recipients = recipients
        self.logger = logging.getLogger(__name__)
        self.client = boto3.client('ses', region_name=aws_region)

    def send_email(self, is_success, action, dataset):
        indicator = "SUCCESS" if is_success else "FAILURE"
        content = "{0} {1} {2}".format(action.capitalize(), dataset, indicator)
        subject = content
        body = """<html>
               <head></head>
               <body>
                 <h1>{}</h1>
               </body>
               </html> """.format(content)
        try:
            self.client.send_email(
                Destination={
                    'ToAddresses': self.recipients,
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
                Source=self.sender
            )
        except ClientError as e:
            self.logger.exception(e.response['Error']['Message'])

