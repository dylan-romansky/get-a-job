This set of scripts is designed to search linkedin for job
listings that meet the given criteria, dump the job
descriptions along with a link to the original post, and
keep a local copy as well as a copy on Google Drive.

At the time of writing this, the google drive portion
relies on having your own project on the Google's cloud
platform that's allowed to have access to Google drive.
I will be updating this listing with the instructions on
how to do that in the coming days.

This project uses Selenium in conjunction with
BeautifulSoup to aquire the job listings and parse them.
I found BeautifulSoup to be easier to work with for the
purposes of actually getting the information from the
webpage, however BeautifulSoup doesn't work well with
websites that dynamically load portions of the page. For
that reason, I'm using Selenium to handle the actual
browsing, then passing the pages it gets to
BeautifulSoup to handle parsing the data.

In addition to this, I've used the `argparse` Python
module to implement a more userfriendly interface in the
form of the `get_a_job.py` script. It allows me to
quickly and efficiently add flags, descriptions of those
flags, and defined behaviour for them so I can easily
expand the program and its capabilities.

The following flags have been implemented so far:

--experience, -e: the experience level you want to
				filter for. Possible options are 
				internship, entry level, associate,
				mid senior level, directory, executive.
				Options with whitespace characters in them
				must be quoted. Multiple choices are possible
				by using multiple instances of the flag

--type, -t:	the type of job you're looking for. Possible
				options are full-time, part-time,
				contract, temp, internship, other. Multiple
				choices are possible by using multiple
				instances of the flag

--workplace, -w: whether you're looking for remote, on-site,
				or hybrid work. Multiple choices are possible
				by using multiple instances of the flag

--date-posted, -d: use the option "day", "week", or "month"
				to limit the age of scraped results down to
				listings posted in the last 24 hours, 7 days,
				or month. If left unspecified, it defaults to
				the last 24 hours

--location, -l: where you want to search for listings in the
				form "city, state/province, country". Must be
				quoted. Country is the only mandatory option.
				examples of valid input:
				"Los Angeles, California, United States"
				"Colorado, United States"
				"Canada"

--sort, -s: when present, the found urls are unsorted. When
				absent, they are sorted in order of posting
				time

--no-upload, -u: when present, the found listings are only
				saved locally. They are not uploaded to 
				Google Drive

After inputting your desired flags and their parameters, enter
a list of keywords you want the script to actually search for.

I've taken a "site by site" approach to writing scripts that
interact with job boards. Currently it only supports linkedin,
in the form of the contents of `linkedin.py`, however as time
goes on I suspect I will find more sites to scrape from and
will add separate modules to scrape for each of them. By
default, running `linkedin.py` directly will scrape for all
listings for sre roles in California posted in the last 24
hours and save them locally.

Lastly, the `open_links.py` script takes a given list of
files containing a link as the first line, then opens them
one by one in a browser window. As of the time of writing,
this requires you to not have a Google Chrome instance open
at the time of running the script. I am going to start
looking into how to connect to an already active browser
session so that this is no longer an inconvenience.
