#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chrome_start
import sys
import os

def user_input():
	print('Filenames:')
	return input().split(' ')

if (len(sys.argv) < 2):
	file_set = user_input()
else:
	file_set = sys.argv[1:]
if not file_set or not file_set[0] or not os.path.exists(file_set[0]):
	print("Error: files not present")
	exit()
caps = DesiredCapabilities.CHROME
caps["pageLoadStrategy"] = "none"
try:
	driver = chrome_start.chrome_start(caps)
except:
	print("Please close other browser windows and try again")
	#until I figure out how to implement connecting to an
	#active browser session, exiting and making the user close
    #their browser and run the script againagain is the
	#best solution I have
	exit()
for file in file_set:
	print("Opening: " + file)
	driver.switch_to.new_window('tab')
	with open(file, 'r') as link:
		driver.get(link.readline())
