import logging
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

import tji_utils

CHARSET = "UTF-8"


class TJIEmailer():
    # TJIEmailer sends success and failure emails via Amazon SES during cleaning
    # and compressing of a TJI dataset.

    def __init__(self, sender, recipients, aws_region):
        """Constructor for TJIEmailer object

        Args:
            sender (string): Email of sender
            recipients ([] of strings): List of recipient emails
            aws_region (string): AWS region associated with SES
        """
        self.sender = sender
        self.recipients = recipients
        self.logger = logging.getLogger('em')
        self.client = boto3.client('ses', region_name=aws_region)
        timestamp = datetime.now().strftime('%Y-%m-%d')
        log_file = 'logs/emailer+%s.log' % timestamp
        self.logger = tji_utils.set_up_logger(name='emailer', log_file=log_file)

    def send_email(self, action, dataset, exception=None):
        """Composes and sends a single email

        Args:
            action (string): "cleaning" or "compression"
            dataset (string): Dataset name
            exception (Exception): If processing failed, the cause.
        """
        try:
            self.client.send_email(
                Destination={
                    'ToAddresses': self.recipients
                },
                Message=TJIEmailer.get_message(action, dataset, exception),
                Source=self.sender
            )
        except ClientError as e:
            self.logger.exception(e.response['Error']['Message'])

    def get_message(action, dataset, exception):
        subject = TJIEmailer.get_subject(action, dataset, exception)
        body = TJIEmailer.get_body(subject, exception)
        return {
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
        }

    def get_body(subject, exception):
        if exception:
            return """<html>
                   <head></head>
                   <body>
                     <p>Error Message:
                     <p>{}
                   </body>
                   </html> """.format(exception)
        else:
            return """<html>
                   <head></head>
                   <body>
                     <h1>{0}</h1>
                   </body>
                   </html> """.format(subject)

    def get_subject(action, dataset, exception):
        indicator = "SUCCESS" if not exception else "FAILURE"
        return "{0} {1} {2}".format(action.capitalize(), dataset, indicator)
