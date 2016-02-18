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
    pass
    # if game page
    # elif wiki page
    # elif cheat page
    # elif walkthrough page
    # else cannot process

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
