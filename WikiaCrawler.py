#!/usr/local/bin/python

''' WikiaCrawler.py
    ---------------
    @author = Ankai Lou
    -------------------
    Module for scraping general Wikia/Wiki pages into HTML
'''

import sys
import os
from time import time
from generics.GameScraper import GameScraper
from generics.GameCrawler import GameCrawler

###############################################################################
############## global variables relating to Wikia/Wiki metadata ###############
###############################################################################

home = ''
base = ''
gt = []
pt = []
gp = []
pc = []
bt = []
bp = []
selector = {}

###############################################################################
###### Class definition for WikiaCrawler object that extends GameCrawler ######
###############################################################################

class WikiaCrawler(GameCrawler):
    def __init__(self, scraper, selectors, base=''):
        ''' function: constructor
            ---------------------
            instantiate crawler for relevant Wikia/Wiki
            -------------------------------------------
            @scraper   GameScraper object used for scraping/updating url
            @selector  dictionary of css selector for URL curation
            @base      base URL for incomplete paths (thanks IGN)
        '''
        GameCrawler.__init__(self, scraper, selector, base)

    ###########################################################################
    ######################### helper function for bfs #########################
    ###########################################################################

    def __relevant(self, url):
        ''' function: relevant
            ------------------
            determine if @url and content are relevant for scraping
            -------------------------------------------------------
            @url    string represeting URL to test for relevance
        '''
        return True

    def __get_neighbors(self):
        ''' function: get_neighbors
            -----------------------
            return relevant, non-visited neighbors to @self.scraper.soup
            ------------------------------------------------------------
        '''
        neighbors, soup = [], self.scraper.soup
        if soup:
            pass
            # get menu and navbar URLs
            # get embedded URLs
        return neighbors

    ###########################################################################
    ################ crawl function inherited from GameCrawler ################
    ###########################################################################


###############################################################################
###################### main function for testing purpose ######################
###############################################################################

def main(argv):
    ''' function: main
        --------------
        accept list of urls & filepaths to url lists as @argv
        -----------------------------------------------------
    '''
    total_start = time()
    scraper  = GameScraper(gt, gp, pt, pc, bt, bp, home)
    crawler  = WikiaCrawler(scraper, selector, base)
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
