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
from bs4 import BeautifulSoup

###############################################################################
############################## global variables ###############################
###############################################################################

explored = set()
html_dir = '../html/ign/'
ign_base = 'http://www.ign.com'
sublinks = ['wiki-guide', 'cheats']
selectors = { 'sublink' : 'ul.contentNav.clear.noprint a' }

###############################################################################
############### helper functions for scraping generic IGN pages ###############
###############################################################################

def __dissect(url):
    ''' function: dissect
        -----------------
        extract sub-links from IGN game page and crawl/scrape
    '''
    try:
        soup = BeautifulSoup(urlopen(url).read(), 'html.parser')
    except:
        print 'Cannot get sub-links for argument:', url
        return

    global explored
    for a in [link
              for attr in sublinks
              for link in soup.select(selectors['sublink'] + '[title=%s]'%attr)
              if link['href'] not in explored]: classify(a['href'])

def classify(url):
    ''' function: classify
        ------------------
        determine action for @url based on regex matching
    '''
    global explored
    if re.match(ign_base + '/games/.+', url):
        __dissect(url)
    elif os.path.isfile(url): 
        print 'LOL'
        return
    elif url not in explored:
        if re.match(ign_base + '/wikis/.+', url):
            explored = explored | crawl(url, html_dir)
        elif re.match(ign_base + '/cheats/.+', url):
            explored = explored | scrape(url, html_dir)
        else:
            print url, 'cannot be processed by existing scrapers...'
    return explored

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
    print 'Total time elapsed:', time() - total_start, 'seconds'

if __name__ == '__main__':
    main(sys.argv[1:])
