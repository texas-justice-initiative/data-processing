import boto3
import logging
import tji_utils

from datetime import datetime
from botocore.exceptions import ClientError

CHARSET = "UTF-8"


class TJIEmailer():
    # TJIEmailer sends success and failure emails via Amazon SES during cleaning and compressing of a TJI dataset.
    
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

    def send_email(self, is_success, action, dataset):
        """Composes and sends a single email
        
        Args:
            is_success (boolean): success or failure email
            action (string): "cleaning" or "compression"
            dataset (string): Dataset name
        """
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

