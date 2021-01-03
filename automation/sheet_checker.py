"""Summary
"""
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import argparse
import os
import sys
from datetime import datetime

import boto3
import dateutil.parser
import nbformat
import pygsheets
import pytz
import yaml
from botocore.exceptions import ClientError
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError

import tji_utils
from tji_emailer import TJIEmailer

class SheetChecker(object):

    """ Sheet Checker is intended to run as a cronjob. It checks the last update timestamp of a google sheet against
    the cronjob's last run timestamp. If the sheet has been updated since the last run, it runs the cleaning notebooks
    and compression notebooks, then updates the timestamp.

    Author: Aiden Yang <aiden.yang@texasjusticeinitiative.org>
    """

    def __init__(self, dataset, emailer, sheet_key, cleaning_nbs, compression_nbs, force, sync):
        """ Constructor for Sheet Checker object.

        Args:
            dataset (string): Name of dataset
            emailer (TJIEmailer): Emailer obj used for sending success and failures emails through SES
            sheet_key (string): Google Sheets key
            cleaning_nbs ([] of strings): List of cleaning notebooks to run
            compression_nbs ([] of strings): List of compression notebooks to run
            force (boolean): Controls whether or not to run cleaning and compression nbs even if sheet has not been updated
            sync (bolean): Controls whether or not notebooks will sync data to Data.world
        """
        self.s3_client = boto3.client('s3')
        self.emailer = emailer
        self.force_full_update = force
        self.sync_dw = sync
        self.dataset = dataset
        self.sheet_key = sheet_key
        self.sheet_name = sheet_name
        self.cleaning_nbs = cleaning_nbs
        self.compression_nbs = compression_nbs

        timestamp = datetime.now().strftime('%Y-%m-%d')
        log_file = 'logs/%s+%s.log' % (self.dataset, timestamp)
        self.logger = tji_utils.set_up_logger(name=dataset, log_file=log_file)

    def run(self):
        if self.is_sheet_updated() or self.force_full_update:
            self.logger.info("Cleaning and compressing...")
            self.set_up_environment()
            self.clean()
            self.compress()
            self.update_last_ran_ts()
            self.clean_up_environment()
        else:
            self.logger.info("Sheet has not been updated since last run."
                             "Set force=True if you want to clean and compress anyway. Exiting.")
            self.update_last_ran_ts()

    def clean(self):
        """ Runs cleaning notebooks
        """
        try:
            for cleaning_nb in self.cleaning_nbs:
                self.run_notebook(cleaning_nb)
            self.emailer.send_email(action="Cleaning", dataset=self.dataset)
        except Exception as e:
            self.logger.exception(e)
            self.emailer.send_email(action="Cleaning", dataset=self.dataset, exception=e)
            self.logger.error('Cleaning failed.')
            sys.exit('Exiting: encountered an issue while cleaning.')

    def compress(self):
        """ Runs compression notebooks
        """
        try:
            for compression_nb in self.compression_nbs:
                self.run_notebook(compression_nb)
            self.emailer.send_email(action="Compressing", dataset=self.dataset)
        except Exception as e:
            self.logger.exception(e)
            self.logger.error('Compressing failed.')
            self.emailer.send_email(action="Compressing", dataset=self.dataset, exception=e)
            sys.exit('Exiting: encountered an issue while compressing.')
        self.logger.info("Successfully cleaned and compressed data.")

    def run_notebook(self, nb_name):
        """Runs a notebook and write out the output notebook

        Args:
            nb_name (string): notebook filename
        """
        out_notebook_name = 'output_notebooks/%s_result_nb.ipynb' % nb_name
        nb = nbformat.read('../data_cleaning/%s' % nb_name, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        try:
            ep.preprocess(nb, {'metadata': {'path': '../data_cleaning/'}})
        except CellExecutionError:
            msg = 'Error executing the notebook'
            msg += 'See notebook "%s" for the traceback.' % out_notebook_name
            self.logger.info(msg)
            raise
        finally:
            with open(out_notebook_name, mode='wt') as f:
                nbformat.write(nb, f)

    def is_sheet_updated(self):
        """Checks if google sheet has been updated since the last time this job ran

        Returns:
            boolean
        """
        sheet_last_updated_ts = dateutil.parser.parse(self.get_sheet_update_ts())
        last_run_ts = self.fetch_last_run_ts()
        if not last_run_ts:
            return False
        else:
            job_last_run_ts = dateutil.parser.parse(last_run_ts)
            job_last_run_ts = job_last_run_ts.replace(tzinfo=pytz.UTC)
            return sheet_last_updated_ts >= job_last_run_ts

    def get_sheet_update_ts(self):
        """
        Returns:
            timestamp: Last update timestamp of google sheet
        """
        gc = pygsheets.authorize(service_file='client_secret.json')
        gc.drive.enable_team_drive('0ACeQWapAwOLqUk9PVA')
        sheet = gc.open_by_key(self.sheet_key)
        last_updated_ts = sheet.updated
        return last_updated_ts

    def get_sheet_update_ts(self):
        """
        Returns:
        timestamp: Last update timestamp of google sheet
        """
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('/home/ec2-user/test/data-processing/automation/google_token.pickle'):
            with open('/home/ec2-user/test/data-processing/automation/google_token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '/home/ec2-user/test/data-processing/automation/google_v3_credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('/home/ec2-user/test/data-processing/automation/google_token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)

        # search for timestamp by name

        results = service.files().list(
        pageSize=10, 
        driveId = '0ACeQWapAwOLqUk9PVA', 
        includeItemsFromAllDrives = 'true', 
        corpora = 'drive',
        supportsAllDrives = 'true',
        fields="nextPageToken, files(id, name, modifiedTime)",
        q = "name = '{}'".format(sheet_name)).execute()
        
        items = results.get('files', [])
        assert(len(items) == 1)
        assert(items[0]['id'] == sheet_key)
        return(items[0]['modifiedTime'])

    def update_last_ran_ts(self):
        """Drops current time as timestamp in s3, to be used next time this job runs
        """
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        self.s3_client.put_object(Body=timestamp, Bucket='tji-timestamps', Key=self.dataset)
        self.logger.info("Updated %s timestamp." % self.dataset)

    def fetch_last_run_ts(self):
        """Fetches last job run timestamp from s3

        Returns:
            last_run_ts: Last time this job ran
        """
        try:
            timestamp = self.s3_client.get_object(Bucket='tji-timestamps', Key=self.dataset)
            body = timestamp['Body']
            last_run_ts = body.read()
            return last_run_ts
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                self.logger.info("No timestamp found.")
            else:
                self.logger.exception(e)
                self.logger.info("Something went wrong while fetching timestamp.")

    def set_up_environment(self):
        """Sets environment variables that controls whether or not notebooks write to data.world and/or s3
        """
        dataset = self.dataset.upper()
        if self.sync_dw:
            os.environ['CLEAN_%s_DW' % dataset] = 'TRUE'
        os.environ['CLEAN_%s_S3' % dataset] = 'TRUE'
        os.environ['COMPRESS_%s_S3' % dataset] = 'TRUE'

    def clean_up_environment(self):
        """Unsets all environment variables
        """
        dataset = self.dataset.upper()
        os.unsetenv('CLEAN_%s_DW' % dataset)
        os.unsetenv('CLEAN_%s_S3' % dataset)
        os.unsetenv('COMPRESS_%s_S3' % dataset)


def is_valid_file(argument_parser, file_name):
    """
    Checks if file exists and returns open file object; displays an error message and usage information if it does not.
    Args:
        argument_parser (ArgumentParser): instance of ArgumentParser
        file_name (string): file name

    """
    if not os.path.exists(file_name):
        argument_parser.error("The file %s does not exist." % file_name)
    else:
        return open(file_name, 'r')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check gsheets for changes and re-clean and re-compress.')
    parser.add_argument('-config', dest='fd', required=True,
                        help='File path of config .yaml file', metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))

    args = parser.parse_args()

    # Parse config.yaml
    config = yaml.load(args.fd)
    args.fd.close()

    # Set up emailer obj
    email_config = config['Email Settings']
    emailer = TJIEmailer(sender=email_config['sender'],
                         recipients=email_config['recipients'],
                         aws_region=email_config['region'])

    # Create and run sheet checker for one dataset
    for dataset, settings in config['Datasets'].items():
        if settings['enabled']:
            sc = SheetChecker(dataset=dataset,
                              emailer=emailer,
                              sheet_key=settings['sheet key'],
                              sheet_name = settings['sheet name'],
                              cleaning_nbs=settings['cleaning notebooks'],
                              compression_nbs=settings['compression notebooks'],
                              force=settings['force'],
                              sync=settings['sync'])
            sc.run()
