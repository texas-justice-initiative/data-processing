"""Summary
"""
import os
import sys
import pytz
import yaml
import boto3
import logging
import argparse
import nbformat
import tji_utils
import pygsheets
import dateutil.parser

from tji_emailer import TJIEmailer

from io import BytesIO
from datetime import datetime
from botocore.exceptions import ClientError
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError


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
        self.cleaning_nbs = cleaning_nbs
        self.compression_nbs = compression_nbs

        timestamp = datetime.now().strftime('%Y-%m-%d')
        log_file = 'logs/%s+%s.log' % (self.dataset, timestamp)
        self.logger = tji_utils.set_up_logger(name=dataset, log_file=log_file)

    def run(self):
        if self.is_sheet_updated() or self.force_full_update:
            self.logger.info("Sheet has been updated since last run. Cleaning and compressing...")
            self.set_up_environment()
            self.clean()
            self.compress()
            self.update_last_ran_ts()
            self.clean_up_environment()
        else:
            self.logger.info("Sheet has not been updated since last run. Exiting.")
            self.update_last_ran_ts()

    def clean(self):
        """ Runs cleaning notebooks
        """
        try:
            for cleaning_nb in self.cleaning_nbs:
                self.run_cleaning_notebook(cleaning_nb)
            self.emailer.send_email(is_success=True, action="Cleaning", dataset=self.dataset)
        except Exception as e:
            self.logger.exception(e)
            self.emailer.send_email(is_success=False, action="Cleaning", dataset=self.dataset)
            self.logger.error('Cleaning failed.')
            sys.exit('Exiting: encountered an issue while cleaning.')

    def compress(self):
        """ Runs compression notebooks
        """
        try:
            for compression_nb in self.compression_nbs:
                self.run_compression_notebook(compression_nb)
            self.emailer.send_email(is_success=True, action="Compressing", dataset=self.dataset)
        except Exception as e:
            self.logger.exception(e)
            self.logger.error('Compressing failed.')
            self.emailer.send_email(is_success=False, action="Compressing", dataset=self.dataset)
            sys.exit('Exiting: encountered an issue while compressing.')
        self.logger.info("Successfully cleaned and compressed data.")

    def run_cleaning_notebook(self, cleaning_nb_name):
        """Runs a single cleaning notebook
        
        Args:
            cleaning_nb_name (string): File name of cleaning notebook in data_cleaning directory
        """
        out_notebook_name = 'output_notebooks/cleaning_%s_result_nb.ipynb' % self.dataset
        nb = nbformat.read('../data_cleaning/%s' % cleaning_nb_name, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        self.run_notebook(ep, nb, out_notebook_name)
        self.logger.info("Successfully cleaned.")

    def run_compression_notebook(self, compression_nb_name):
        """Runs a single compression notebook
        
        Args:
            compression_nb_name (string): File name of a compression notebook in data_cleaning directory
        """
        out_notebook_name = 'output_notebooks/compression_%s_result_nb.ipynb' % self.dataset
        nb = nbformat.read('../data_cleaning/%s' % compression_nb_name, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        self.run_notebook(ep, nb, out_notebook_name)
        self.logger.info("Successfully compressed.")

    def run_notebook(self, ep, nb, out_notebook_name):
        """Runs a notebook and write out the output notebook
        
        Args:
            ep (ExecutePreprocessor): ExecutePreprocessor instance
            nb (NotebookNode): NotebookNode instance
            out_notebook_name (string): Where to write output notebook
        """
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
        gc.enableTeamDriveSupport = True
        sheet = gc.open_by_key(self.sheet_key)
        last_updated_ts = sheet.updated
        return last_updated_ts

    def update_last_ran_ts(self):
        """Drops current time as timestamp in s3, to be used next time this job runs
        """
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        buff = BytesIO()
        buff.write(timestamp.encode('utf-8'))
        buff.seek(0)
        self.s3_client.put_object(Body=buff, Bucket='tji-timestamps', Key=self.dataset)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check gsheets for changes and re-clean and re-compress.')
    parser.add_argument('-config', dest='fd', required=True,
                        help='File path of config .yaml file', metavar="FILE",
                        type=lambda x: tji_utils.is_valid_file(parser, x))

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
                              cleaning_nbs=settings['cleaning notebooks'],
                              compression_nbs=settings['compression notebooks'],
                              force=settings['force'],
                              sync=settings['sync'])
            sc.run()
