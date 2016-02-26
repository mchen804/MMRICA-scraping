#!/usr/local/bin/python

''' WikiaCrawler.py
    ---------------
    @author = Ankai Lou
    -------------------
    Module for scraping general Wikia/Wiki pages into HTML
'''

import sys
import os
import re
from time import time
from urlparse import urlparse, urljoin
from generics.GameScraper import GameScraper
from generics.GameCrawler import GameCrawler

###############################################################################
############## global variables relating to Wikia/Wiki metadata ###############
###############################################################################

home = 'html/wikia/'
base = ''
gt = []
pt = ['h1#firstHeading', 'div.header-column.header-title']
gp = ['table.infobox.bordered.vevent tr td b']
pc = ['div#bodyContent', 'div#WikiaArticle']
bt = ['a', 'div.gh-next-prev-buttons', 'img', 'iframe']
bp = ['Home', 'Main Page', 'Redirected', 'Disambiguation', 'Logged', 'New images',
      'logged in to chat', 'Forum', 'New User', 'Help', 'Special', 'News', 'Recent Wiki Activity']
selector = {'menu'  : ['div#p-Navigation div.pBody a', 'nav.WikiNav li.nav-item .subnav-2-item a'],
            'embed' : ['div#bodyContent a', 'div#WikiaArticle a']}

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
        self.type = ['jpg', 'png', 'gif', 'webm']
        self.wiki, self.base = '', ''

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
        if re.match(self.base + '.+', url) and url.count(':') < 2 and url.count('#') == 0:
            return True
        elif any([re.match(r'.+\.%s' % filetype , url) for filetype in self.types]):
            return False
        else:
            return False

    def __get_neighbors(self):
        ''' function: get_neighbors
            -----------------------
            return relevant, non-visited neighbors to @self.scraper.soup
            ------------------------------------------------------------
        '''
        neighbors, soup = [], self.scraper.soup
        if soup:
            # get navigation bar URLs
            for css in self.selectors['menu']:
                for link in soup.select(css):
                    neighbors.append(urljoin(self.base, link['href']))
            # get embedded URLs
            for css in self.selectors['embed']:
                for link in soup.select(css):
                    if link.has_attr('href'):
                        fqdn = urljoin(self.base, link['href'])
                        if self.__relevant(fqdn): neighbors.append(fqdn)
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
        if url not in self.explored:
            self.frontier.append(url)
            self.scraper.game[0] = '{uri.netloc}'.format(uri=urlparse(url))
            self.base = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))

        while len(self.frontier) > 0:
            node = self.frontier.pop(0)
            if self.scraper.update(node) == 0:
                self.explored.add(node)
                self.scraper.scrape()
                for neighbor in self.__get_neighbors():
                    if neighbor not in self.frontier and neighbor not in self.explored:
                        self.frontier.append(neighbor)
            else: continue
        print 'Crawling complete in', time() - start, 'seconds'

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
