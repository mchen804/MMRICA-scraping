#!/usr/local/bin/python

''' GameCrawler.py
    --------------
    @author = Ankai Lou
    -------------------
    Class description for MMRICA Web Crawler for large subsets of pages
'''

###############################################################################
######################## import libraries & frameworks ########################
###############################################################################

import os
import sys
import re
from time import time
from json import loads

###############################################################################
################### Class definition for GameCrawler object ###################
###############################################################################

class GameCrawler(object):
    def __init__(self, scraper, selectors, base=''):
        ''' function: constructor
            ---------------------
            instantiate game crawler object for site type
            ---------------------------------------------
            @scraper   GameScraper object used for scraping/updating url
            @selector  dictionary of css selector for URL curation
            @base      base URL for incomplete paths (thanks IGN)
        '''
        self.scraper = scraper
        self.selectors = selectors
        self.base = base
        self.explored = set()
        self.frontier = list()

    ###########################################################################
    ######################## helper functions for bfs #########################
    ###########################################################################

    def __relevant(self, url):
        ''' function: relevant
            ------------------
            determine if @url and content are relevant for scraping
            -------------------------------------------------------
            @url    string representing URL to classify
        '''
        # TODO: OVERRIDE IN INHERITANCE
        return True

    def __get_neighbors(self):
        ''' function: get_neighbors
            -----------------------
            return relevant, non-visited neighbors to @self.scraper.soup
            ------------------------------------------------------------
        '''
        # TODO: OVERRIDE IN INHERITANCE
        neighbors, soup = [], self.scraper.soup
        if soup: pass
        return neighbors

    ###########################################################################
    ########### calleable functions from outside object declaration ###########
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
                self.scraper.scrape()
                for neighbor in self.__get_neighbors():
                    if neighbor not in self.frontier and neighbor not in self.explored:
                        self.frontier.append(neighbor)
            else: continue
        print 'Crawling complete in', time() - start, 'seconds'

