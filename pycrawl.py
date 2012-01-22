#Python Web Crawler App - Main Python Script
#By Tom Peters
#tom@tjpeters.org

import pycrawllib
import argparse #For parsing command-line input

#Argument parsing
argparser = argparse.ArgumentParser(description="Search web pages recursively for a search string")
argparser.add_argument('-d', nargs=1, default=['5'])
argparser.add_argument('-s', nargs=1, default=[''])
argparser.add_argument('-v', action='store_true')
argparser.add_argument('URL')
args = argparser.parse_args()

#Crawling
crawl = pycrawllib.Crawler(args.URL, args.s[0], int(args.d[0]), verbose=args.v)
crawl.startCrawl()

#Output to stdout
for line in crawl.getResultURLList():
	print line
