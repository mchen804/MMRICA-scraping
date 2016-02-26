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
from bs4 import BeautifulSoup
from generics.GameScraper import GameScraper
from generics.GameCrawler import GameCrawler

###############################################################################
############################## global variables ###############################
###############################################################################

sublinks = ['wiki-guide', 'cheats']

bad_tags = ['a', 'div.gh-next-prev-buttons', 'img', 'p.wiki-videoEmbed']
gt = ['h2.contentTitle a']
pt = ['h1.gh-PageTitle']
gp = ['div.contentPlatformsText span a']
pc = ['div.grid_12.push_4.alpha.omega.bodyCopy.gh-content']
bp = ['Recent Changes', 'Orphaned Pages', 'Dead-end Pages', 'Wanted Pages', 'Short Pages', 'Long Pages', 'All Pages']
home = '../html/ign/'
selectors = {'menu'  : 'div.ghn-L1.ghn-hasSub', 'embed' : 'div.grid_12.push_4.alpha.omega.bodyCopy.gh-content a' }
base = 'http://www.ign.com'

cheat_pt = ['h3.maintext16.bold.grey']
cheat_pc = []
categories = {'div#category_cheat div.cheatBody div.grid_12.omega' : 'Cheat',
              'div#category_unlockable div.cheatBody div.grid_12.omega' : 'Unlockable',
              'div#category_hint div.cheatBody div.grid_12.omega' : 'Hint',
              'div#category_easter-egg div.cheatBody div.grid_12.omega' : 'Easter Egg',
              'div#category_achievement div.cheatBody div.grid_12.omega' : 'Achievement'}

scraper = GameScraper(gt, gp, pt, pc, bad_tags, bp, home)
crawler = GameCrawler(scraper, selectors, base)
cheat_scraper = GameScraper(gt, gp, cheat_pt, cheat_pc, bad_tags, bp, home, categories)

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
    for link in soup.select('ul.contentNav.clear.noprint a[title=%s]'%attr)]:
        classify(a['href'])

def classify(url):
    ''' function: classify
        ------------------
        determine action for @url based on regex matching
    '''
    global explored
    if re.match(base + '/games/.+', url):
        __dissect(url)
    elif os.path.isfile(url):
        return
    else:
        if re.match(base + '/wikis/.+', url):
            crawler.crawl(url)
        elif re.match(base + '/cheats/.+', url):
            cheat_scraper.scrape(url)
        else:
            print url, 'cannot be processed by existing scrapers...'

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
