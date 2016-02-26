#!/usr/local/bin/python

''' ign_wiki_scrape.py
    ------------------
    @author = Ankai Lou
    -------------------
    Module for scraping, preprocessing, and compiling IGN wiki pages into HTML
'''

import sys
import os
from generics.GameScraper import GameScraper
from generics.GameCrawler import GameCrawler
from time import time

###############################################################################
############################## global veriables ###############################
###############################################################################

bad_tags = ['a', 'div.gh-next-prev-buttons', 'img', 'p.wiki-videoEmbed']
gt = ['h2.contentTitle a']
pt = ['h1.gh-PageTitle']
gp = ['div.contentPlatformsText span a']
pc = ['div.grid_12.push_4.alpha.omega.bodyCopy.gh-content']
bp = []
home = 'html/ign/wiki/'

selectors = {'menu'  : 'div.ghn-L1.ghn-hasSub', 'embed' : 'div.grid_12.push_4.alpha.omega.bodyCopy.gh-content a' }
base = 'http://www.ign.com'

###############################################################################
##################### main function for testing purposes ######################
###############################################################################

def main(argv):
    ''' function: main
        --------------
        accept list of urls & filepaths to url lists as @argv
    '''
    total_start = time()
    scraper = GameScraper(gt, gp, pt, pc, bad_tags, bp, home)
    crawler = GameCrawler(scraper, selectors, base)
    for arg in argv:
        if os.path.isfile(arg):
            print 'Processing arguments in file:', arg
            for line in open(arg, 'r'): argv.append(line.rstrip())
        else:
            print 'Processing argument:', arg
            crawler.crawl(arg)
    print 'Total time elapsed:', time() - total_start, 'seconds'

if __name__ == '__main__':
    main(sys.argv[1:])
