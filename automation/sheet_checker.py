import os
import sys
import pytz
import boto3
import logging
import nbformat
import pygsheets
import dateutil.parser

from io import StringIO, BytesIO
from datetime import datetime
from botocore.exceptions import ClientError
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError


class SheetChecker(object):
    def __init__(self, dataset, sheet_name, cleaning_nbs):
        self.s3_client = boto3.client('s3')
        self.dataset = dataset
        self.sheet_name = sheet_name
        self.cleaning_nbs = cleaning_nbs
        self.logger = logging.getLogger(__name__)
        timestamp = datetime.now().strftime('%Y-%m-%d')
        logging.basicConfig(filename='%s+%s.log' % (self.dataset, timestamp), level=logging.INFO)


    def run(self):
        if self.is_sheet_updated():
            self.logger.info("Sheet has been updated since last run. Cleaning and compressing...")
            self.set_up_environment()
            try:
                for cleaning_nb in self.cleaning_nbs:
                    self.run_cleaning_notebook(cleaning_nb)
            except Exception as e:
                self.logger.exception(e)
                self.logger.warning('Cleaning failed.')
                sys.exit('Exiting: encountered an issue while cleaning.')
            try:
                self.run_compression_notebook()
            except Exception as e:
                self.logger.exception(e)
                self.logger.warning('Compressing failed.')
                sys.exit('Exiting: encountered an issue while compressing.')
            self.logger.info("Successfully cleaned and compressed data.")
            self.update_last_ran_ts()
        else:
            self.logger.info("Sheet has not been updated since last run. Exiting.")
            self.update_last_ran_ts()
            

    def run_cleaning_notebook(self, cleaning_nb_name):
        out_notebook_name = 'cleaning_%s_result_nb.ipynb' % self.dataset
        nb = nbformat.read('../data_cleaning/%s' % cleaning_nb_name, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        self.run_notebook(ep, nb, out_notebook_name)
        self.logger.info("Successfully cleaned.")

    def run_compression_notebook(self):
        out_notebook_name = 'compression_%s_result_nb.ipynb' % self.dataset
        nb = nbformat.read('../data_cleaning/create_datasets_for_website.ipynb', as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        self.run_notebook(ep, nb, out_notebook_name)
        self.logger.info("Successfully compressed.")
        return True

    def run_notebook(self, ep, nb, out_notebook_name):
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


    def print_progress(self, cell_idx):
        self.logger.debug(cell_idx)


    def is_sheet_updated(self):
        sheet_last_updated_ts = dateutil.parser.parse(self.get_sheet_update_ts())
        last_run_ts = self.fetch_last_run_ts()
        if not last_run_ts:
            return False
        else:
            job_last_run_ts = dateutil.parser.parse(last_run_ts)
            job_last_run_ts = job_last_run_ts.replace(tzinfo=pytz.UTC)
            return sheet_last_updated_ts >= job_last_run_ts


    def get_sheet_update_ts(self):
        gc = pygsheets.authorize(service_file='client_secret.json')
        sheet = gc.open(self.sheet_name)
        last_updated_ts = sheet.updated
        return last_updated_ts

    def update_last_ran_ts(self):
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        buff = BytesIO()
        buff.write(timestamp.encode('utf-8'))
        buff.seek(0)
        self.s3_client.put_object(Body=buff, Bucket='tji-timestamps', Key=self.dataset)
        self.logger.info("Updated %s timestamp." % self.dataset)

    
    def fetch_last_run_ts(self):
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
        # Assume for now we want to clean and compress. 
        # Make more configurable 
        dataset = self.dataset.upper()
        os.environ['CLEAN_%s_S3' % dataset] = 'TRUE'
        os.environ['COMPRESS_%s_S3' % dataset] = 'TRUE'
        os.environ['COMPRESS_DATASET'] = dataset


class CDRChecker(SheetChecker):
    def __init__(self, *args, **kwargs):
        super(CDRChecker, self).__init__(*args, **kwargs)

class OISChecker(SheetChecker):
    def __init__(self, *args, **kwargs):
        super(OISChecker, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    cdr = CDRChecker(dataset='cdr', sheet_name='CDR-Testing', cleaning_nbs=['clean_cdr.ipynb'])
    cdr.run()
    ois = OISChecker(dataset='ois', sheet_name='OIS-Testing',
      cleaning_nbs=['clean_ois_civilians_shot.ipynb', 'clean_ois_officers_shot.ipynb'])
    ois.run()