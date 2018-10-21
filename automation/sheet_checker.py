import os
import sys
import boto3
import logging
import datetime
import pygsheets
import dateutil.parser


from cStringIO import StringIO
from IPython.nbformat.current import read
from runipy.notebook_runner import NotebookRunner


class SheetChecker(object):
	def __init__(self, dataset, sheet_name, cleaning_nbs):
		self.s3_client = boto3.client('s3')
		self.dataset = dataset
		self.sheet_name = sheet_name
		self.cleaning_nbs = cleaning_nbs
		self.logger = logging.get_logger(__name__)
		timestamp = datetime.now().strftime('%Y-%m-%d')
		logging.basicConfig(filename='%s+%s.log' % (self.dataset, timestamp), level=logging.DEBUG)


	def run():
		if is_sheet_updated():
			self.set_up_environment()
			try:
				for cleaning_nb in self.cleaning_nbs:
					self.run_cleaning_notebook(cleaning_nb)
			except Exception as e:
				self.logger.exception(e)
				self.logger.warning('Cleaning failed.')
				sys.exit('Exiting: encountered an issue while cleaning.')
			try: 
				# TODO: Set any environment variables needed for compression nb
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
			

	def run_cleaning_notebook(cleaning_nb_name)
		notebook = read(open('../data_cleaning/%s' % cleaning_nb_name), 'json')
		runner = NotebookRunner(notebook)
		try:
			runner.run_notebook(skip_exceptions=False, progress_callback=print_progress(cell_idx))
		except Exception as e:
			raise
		self.logger.info("Successfully cleaned.")

	def run_compression_notebook():
		notebook = read(open('../data_cleaning/create_datasets_for_website.ipynb'), 'json')
		runner = NotebookRunner(notebook)
		try:
			runner.run_notebook(skip_exceptions=False, progress_callback=print_progress(cell_idx))
		except Exception as e:
			raise
		self.logger.info("Successfully compressed.")
		return True


	def print_progress(cell_idx):
		self.logger.debug("Progress: cell %d" % cell_idx, end='\r')


	def is_sheet_updated(self):
		sheet_last_updated_ts = dateutil.parser(self.get_sheet_update_ts())
		last_run_ts = self.fetch_last_run_ts()
		if not last_run_ts:
			return False
		else:
			job_last_run_ts = dateutil.parser(last_run_ts)
			return sheet_last_updated_ts >= job_last_run_ts


	def get_sheet_update_ts(self):
		gc = pygsheets.authorize(service_file='client_secret.json')
		sheet = gc.open(self.sheet_name)
		last_updated_ts = sheet.updated
		return last_updated_ts

	def update_last_ran_ts(self):
		timestamp = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
		buffer = StringIO()
		buffer.write(timestamp)
		buffer.seek(0)
		self.s3_client.put_object(buffer, Bucket='tji-timestamps', Key=self.dataset)
		self.logger.info("Updated %s timestamp." % self.dataset)

	
	def fetch_last_run_ts(self):
		try:
			self.s3_client.get_object(Bucket='tji-timestamps', Key=self.dataset)
			body = s3_object['Body']
			last_run_ts = body.read()
			return last_run_ts
		except botocore.exceptions.ClientError as e:
    		if e.response['Error']['Code'] == "404":
    			self.logger("No timestamp found.")
    		else:
    			self.logger.exception(e)
    			self.logger("Something went wrong while fetching timestamp.")

    def set_up_environment(self):




 class CDRChecker(SheetChecker):
 	def __init__(self, *args, **kwargs):
 		super(CDRChecker, self).__init__(*args, **kwargs)

 class OISChecker(SheetChecker):
 	def __init__(self, *args, **kwargs):
 		super(CDRChecker, self).__init__(*args, **kwargs)    				


if __name__ == '__main__':
	cdr = CDRChecker(dataset='cdr', sheet_name='CDR-Testing', cleaning_nbs=['clean_cdr.ipynb'])
	cdr.run()
	# ois = OISChecker(dataset='ois', sheet_name'OIS-Testing',
	# 	cleaning_nbs=['clean_ois_civilians_shot.ipynb', 'clean_ois_officers_shots.ipynb'])
	# ois.run()