#!/usr/local/bin/python

''' ign_crawler.py
    --------------
    @author = Ankai Lou
    -------------------
    Module for scraping IGN wiki, cheat, and walkthrough pages into HTML
'''

import sys
import os
import re
from time import time
from urllib2 import urlopen
from wiki.crawler import crawl
from cheat.scraper import scrape

###############################################################################
############################## global variables ###############################
###############################################################################

ign_base = 'http://www.ign.com'

###############################################################################
############### helper functions for scraping generic IGN pages ###############
###############################################################################

def dissect(url):
    ''' function: dissect
        -----------------
        extract sub-links from IGN game page and crawl/scrape
    '''
    pass

def classify(url):
    ''' function: classify
        ------------------
        determine action for @url based on regex matching
    '''
    if re.match(ign_base + '/games/.+'):
        dissect(url)
    elif re.match(ign_base + '/wikis/.+'):
        crawl(url)
    elif re.match(ign_base + '/cheats/.+'):
        scrape(url)
    else:
        print 'Argument', url, 'cannot be processed...'

###############################################################################
##################### main function for testing purposes ######################
###############################################################################

def main(argv):
    ''' function: main
        --------------
        accept list of urls & filepaths to url lists as @argv
    '''
    total_start = time()
    for arg in argv:
        if os.path.isfile(arg):
            print 'Processing arguments in file:', arg
            for line in open(arg, 'r'): argv.append(line.rstrip())
        else:
            print 'Processing argument:', arg
            classify(arg)
    print 'Total time elapsed:', time() - total-start, 'seconds'

if __name__ == '__main__':
    main(sys.argv[1:])
