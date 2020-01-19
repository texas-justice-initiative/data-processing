# TJI Automation
## Overview
The Sheet Checker `sheet_checker.py` is intended to live on an AWS EC2 instance and run as a cronjob. Each instance checks if the Google sheet containing raw data has been updated since the last time the cronjob ran successfully. If so, it runs the associated cleaning notebook(s), followed by the associated compression notebook(s), and updates the last run time stamp in s3. Successes and failures are both reported as emails. Each instance logs to separate, timestamped log files, and places the logs in `logs/`. The notebooks that result after cleaning and compression are saved in `output_notebooks/` for debuggging purposes.

This directory also contains a helper file, `tji_emailer.py` which houses methods related to sending emails.

## Configuration
Pass a configuration .yaml file with `-config`. Take a look at `config-sample.yaml` in this repo as an example.

#### Configuring Datasets
Provide the dataset name as the top-level key for each dataset you want to check for updates.

Nested keys:
* **enabled**: true/false
* **force**: true/false, force clean and update even if google sheet has not been updated since last run
* **sync**: true/false, sync to data.world
* **cleaning notebooks**: filenames of cleaning notebooks to run
* **compression notebooks**: filename of compression notebooks to run
* **sheet key**: the Google Sheet key associated with the sheet you want to check for updates

#### Configuring Email Settings
* **sender**: email to send notifications from
* **recipients**: a list of emails to send notifications to
* **region**: the AWS region associated with SES

## Usage
python sheet_checker.py -config <*.yaml>

## Deploying a Change
The data processing scripts are checked out on the EC2 instance in the directory `/home/ec2-user/data-processing`. 
Deploying a change is a simple: 
- connect to the EC2 instance 
- cd into the directory 
- running `git pull` on the repository in the instance  

[Here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-methods.html) is the AWS documentation for connecting to an EC2 instance. The simplest method is the _Connect Using the Browser-based Client_ option.

**Only after pulling the changes into the EC2 instance does the data on the TJI website get updated.** 
