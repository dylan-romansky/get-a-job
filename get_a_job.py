#!/usr/bin/env python3

#designed to be a wrapper for job-scraping scripts as I
#complete new scripts. all results are currently saved in a
#hardcoded location on my machine and are then uploaded to
#a directory on my google drive so I have both a local copy
#and a copy I can access from any machine

import os
import argparse
import linkedin
import drive_handling
from datetime import date
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def arg_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('--experience', '-e', action='append', choices=['internship', 'entry level', 'associate', 'mid senior level', 'director', 'executive'], help='argument must be quoted')
	parser.add_argument('--type', '-t', action='append', choices=['full-time', 'part-time', 'contract', 'temp', 'internship', 'other'])
	parser.add_argument('--workplace', '-w', action='append', choices=['on-site', 'remote', 'hybrid'])
	parser.add_argument('--date-posted', '-d', default='day', choices=['day', 'week', 'month'])
	parser.add_argument('--location', '-l', default='California, United States', help='argument must be quoted')
	parser.add_argument('--sort', '-s', action='store_false')
	parser.add_argument('--no-upload', '-u', action='store_true')
	parser.add_argument('keywords', metavar='kwargs', nargs='+')
	return parser.parse_args()

SCOPE = ['https://www.googleapis.com/auth/drive']
start_dir = os.path.expandvars('$HOME/jobhunt/')

#parse our command line arguments to make our lives easier
args=vars(arg_parser())
print(args)

#create our output directories if they don't exist
os.chdir(start_dir)
drive = drive_handling.drive_setup(SCOPES=SCOPE, token_dir=start_dir)
if os.path.exists('output') == False:
	os.mkdir('output')
os.chdir('output')
if os.path.exists('linkedin') == False:
	os.mkdir('linkedin')

#scrape for our listings, upload them to GDrive if desired
subdir=args['location'].split(',')[0]
linkedin.crawl_linkedin(linkedin.gen_url(args), subdir)
ul_path=start_dir + 'output/linkedin/' + subdir + '/' + str(date.today())
if args['no_upload'] == False and os.path.exists(ul_path):
    os.chdir(ul_path)
    drive_handling.drive_fill(drive.files().list(q='name = "linkedin"').execute(), drive, SUBDIR=subdir)
