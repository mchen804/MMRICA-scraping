#!/usr/local/bin/python

''' IGNCrawler.py
    -------------
    @author = Ankai Lou
    -------------------
    Module for scraping IGN wiki, cheat, and walkthrough pages into HTML
'''

###############################################################################
######################## import libraries & frameworks ########################
###############################################################################

import sys
import os
import re
from time import time
from json import loads
from generics.GameScraper import GameScraper
from generics.GameCrawler import GameCrawler

###############################################################################
################# global variables relating to IGN metadata ###################
###############################################################################

home = 'html/ign/'
base = 'http://www.ign.com'
gt = ['h2.contentTitle a']
pt = ['h1.gh-PageTitle']
gp = ['div.contentPlatformsText span a']
pc = ['div.grid_12.push_4.alpha.omega.bodyCopy.gh-content']
bt = ['a', 'div.gh-next-prev-buttons', 'img', 'p.wiki-videoEmbed']
bp = ['Recent Changes', 'Orphaned Pages', 'Dead-end Pages',
      'Wanted Pages', 'Short Pages', 'Long Pages', 'All Pages']
selector = {'cheats' : 'ul.contentNav.clear.noprint a[title=cheats]',
            'wiki'   : 'ul.contentNav.clear.noprint a[title=wiki-guide]',
            'menu'   : 'div.ghn-L1.ghn-hasSub',
            'embed'  : 'div.grid_12.push_4.alpha.omega.bodyCopy.gh-content a' }
cheat_pt = ['h3.maintext16.bold.grey']
cheat_pc = {'div#category_cheat div.cheatBody div.grid_12.omega'       : 'Cheat',
            'div#category_unlockable div.cheatBody div.grid_12.omega'  : 'Unlockable',
            'div#category_hint div.cheatBody div.grid_12.omega'        : 'Hint',
            'div#category_easter-egg div.cheatBody div.grid_12.omega'  : 'Easter Egg',
            'div#category_achievement div.cheatBody div.grid_12.omega' : 'Achievement'}

###############################################################################
####### Class definition for IGNCrawler object that extends GameCrawler #######
###############################################################################

class IGNCrawler(GameCrawler):
    def __init__(self, scraper, cscraper, selectors, base=''):
        ''' function: constructor
            ---------------------
            instantiate crawler for relevant IGN sites
            ------------------------------------------
            @scraper    GameScraper object used for scraping wiki peages
            @cscraper   GameScraoer object used for scraping cheat pages
            @selectors  dictionary of css selectors for URL curation
            @base       base URL for incomplete paths
        '''
        GameCrawler.__init__(self, scraper, selector, base)
        self.cscraper = cscraper

    ###########################################################################
    ######################### helper function for bfs #########################
    ###########################################################################

    def __relevant(self, url):
        ''' function: relevant
            ------------------
            determine if @url and content are relevant for scraping
            -------------------------------------------------------
            @url    string representing URL to test for relevance
        '''
        return True if re.match(self.base + '/.+/.+/.+', url) else False

    def __get_neighbors(self):
        ''' function: get_neighbors
            -----------------------
            return relevant, non-visited neighbors to @self.scraper.soup
        '''
        neighbors, soup = [], self.scraper.soup
        if soup:
            # get navigation bar URLs
            for a in soup.select(self.selectors['cheats']): neighbors.append(a['href'])
            for a in soup.select(self.selectors['wiki']): neighbors.append(a['href'])
            # get menu URLs
            for url in soup.select(self.selectors['menu']):
                neighbors = neighbors + self.__cascade(loads(url['data-sub']))
            # get embedded URLS
            for url in soup.select(self.selectors['embed']):
                fqdn = self.base + url['href']
                if self.__relevant(fqdn): neighbor.append(fqdn)
        return neighbors

    def __cascade(self, submenu):
        ''' function: cascade
            -----------------
            recursively extract submenu into @neighbors list
            ------------------------------------------------
            @submenu      JSON sublist of URLs
        '''
        neighbors = []
        for item in submenu:
            if item.has_key('href'): neighbors.append(self.base + item['href'])
            if item.has_key('sub'): neighbors = neighbors + self.__cascade(item['sub'])
        return neighbors

    ###########################################################################
    ################ crawl function inherited from GameCrawler ################
    ###########################################################################

    def crawl(self, url):
        ''' function: crawl
            ---------------
            scrapes all relevant/reachable nodes from @url
            ----------------------------------------------
            @url    starting url node to begin crawling process
        '''
        start = time()
        if url not in self.explored: self.frontier.append(url)
        while len(self.frontier) > 0:
            node = self.frontier.pop(0)
            if self.scraper.update(node) == 0:
                self.explored.add(node)
                if re.match(self.base + '/cheats/.+', url):
                    self.cscraper.scrape(url)
                else:
                    self.scraper.scrape()
                    for neighbor in self.__get_neighbors():
                        if neighbor not in self.frontier and neighbor not in self.explored:
                            self.frontier.append(neighbor)
            else: continue
        print 'Crawling complete in', time() - start, 'seconds'

###############################################################################
##################### main function for testing purposes ######################
###############################################################################

def main(argv):
    ''' function: main
        --------------
        accept list of urls & filepaths to url lists as @argv
        -----------------------------------------------------
    '''
    total_start = time()
    scraper  = GameScraper(gt, gp, pt, pc, bt, bp, home)
    cscraper = GameScraper(gt, gp, cheat_pt, cheat_pc, bt, bp, home)
    crawler  = IGNCrawler(scraper, cscraper, selector, base)
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

