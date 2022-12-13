#!/usr/bin/env python3

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import requests
from datetime import date
import os
import re

#TODO: only save results if they've been posted since the
#last time I scraped
#---implemented temp workaround. url now only gets results
#	from whatever time frame I've specified. Default is 24
#	hours

start_dir = os.path.expandvars('$HOME/projects/Python/learning/scraping/output/linkedin')

def str_gen(dic, arg, st):
	nstr = st + str(dic[arg[0]])
	for each in arg[1:]:
		nstr = nstr + "%2C" + str(dic[each])
	return nstr

def gen_url(args):
	exp={"internship": 1, "entry level": 2, "associate": 3, "mid senior level": 4, "director": 5, "executive": 6}
	jt={"full-time": 'F', "part-time": 'P', "contract": 'C', "temp": 'T', "internship": 'I', "other": 'O'}
	wt={"on-site": 1, "remote": 2, "hybrid": 3}
	dp={"day": "r86400", "week": "r604800", "month": "r2592000"}
	urlstr = "?"
	strtab = []
	if args["experience"]:
		strtab.append(str_gen(exp, args["experience"], "f_E="))
	if args["type"]:
		strtab.append(str_gen(jt, args["type"], "f_JT="))
	if args["workplace"]:
		strtab.append(str_gen(wt, args["workplace"], "f_WT="))
	strtab.append("f_TPR=" + dp[args["date_posted"]])
	nstr="keywords=" + args["keywords"][0]
	for each in args["keywords"][1:]:
		nstr=nstr + "%20" + each
	strtab.append(nstr)
	nstr=args["location"]
	strtab.append("location=" + nstr.replace(' ', '%20').replace(',', '%2C'))
	nstr="https://www.linkedin.com/jobs/search/?" + strtab[0]
	for each in strtab[1:]:
		nstr=nstr + "&" + each
	return nstr

def get_job(link, i):
	desc = BeautifulSoup(requests.get(link).text, 'html.parser')
	title = desc.select("#main-content > section.core-rail > div > section.top-card-layout > div > div.top-card-layout__entity-info-container > div > h1")
	if not title:
		title = desc.select("body > div.application-outlet > div.authentication-outlet > div > div.job-view-layout.jobs-details > div.grid > div > div:nth-child(1) > div > div.p5 > h1")
	if not title or not title[0]:
		print("Failed to get title of '" + link + "'... retrying")
		get_job(link, i)
		return
	desc = desc.find('div', class_='show-more-less-html__markup')
	filename = str(i).zfill(2) + ' ' + title[0].string + ".txt"
	filename = filename.replace('/', ' -or- ')
	print("creating: " + filename)
	with open(filename, 'w') as file:
		file.write(link + '\n\n')
		for string in desc.stripped_strings:
			file.write(string + '\n')

#this function has a hardcoded default url in the event
#that it's invoked directly instead of through get_a_job.py
def crawl_linkedin(url="https://www.linkedin.com/jobs/search/?f_E=1%2C2&f_JT=F%2CP%2CI&f_TPR=r86400&geoId=102095887&keywords=sre&location=California%2C%20United%20States&sortBy=DD", sub='California', key='sre'):
	print(url)
	print(sub)
	print(key)
	os.chdir(start_dir)
	if os.path.exists(sub) == False:
		os.mkdir(sub)
	os.chdir(sub)
	today = str(date.today())
	#create the output directory for our results
	if os.path.exists(key) == False:
		os.mkdir(key)
	os.chdir(key)
	if os.path.exists(today) == False:
		os.mkdir(str(date.today()))
	os.chdir(str(date.today()))
	print("PATH: " + os.getcwd())

	try:
		options = Options()
		options.headless = True
#service_log_path has been depracted. I'll need to rewrite
#the below soon
		print('starting selenium driver')
		driver = webdriver.Firefox(options=options, service_log_path='/dev/null')
		driver.get(url)
		print('got page')
		res_list = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/section[2]/ul")
		listings = driver.find_elements(By.TAG_NAME, 'li')
		print('got listings')
		i = 1
		for listing in listings:
			for link in listing.find_elements(By.CLASS_NAME, 'base-card__full-link'):
				get_job(link.get_attribute('href'), i)
				i += 1
	except:
		print("error: no listings found")
		os.chdir("..")
		os.rmdir(key)
		os.chdir("..")
		os.rmdir(str(date.today()))
	driver.quit()

if __name__ == '__main__':
	crawl_linkedin()
