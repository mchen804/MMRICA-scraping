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
################### Class definition for GameScraper object ###################
###############################################################################

class GameCrawler:
    def __init__(self, scraper, selectors, base=''):
        ''' function: constructor
            ---------------------
            instantiate game crawler object for site type
            ---------------------------------------------
            @scraper  GameScraper object used for scraping/updating url
            @base     base URL for incomplete paths (thanks IGN)
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
        if re.match(self.base + '/wikis/.+/.+', url):
            return True
        else:
            return False

    def __append_sublist(self, lis, sublis):
        ''' function: append_sublist
            ------------------------
            extract links recursively down sublists
            ---------------------------------------
        '''
        for d in sublis:
            lis.append(self.base + d['href'])
            if d.has_key('sub'): self.__append_sublist(lis, d['sub'])

    def __get_neighbors(self):
        ''' function: get_neighbors
            -----------------------
            return relevant, non-visited neighbors to @self.scraper.soup
            ------------------------------------------------------------
        '''
        neighbors, soup = [], self.scraper.soup
        if soup:
            for link in soup.select(self.selectors['menu']):
                for doc in loads(link['data-sub']):
                    if doc.has_key('href'): neighbors.append(self.base + doc['href'])
                    if doc.has_key('sub'): self.__append_sublist(neighbors, doc['sub'])
            for link in soup.select(self.selectors['embed']):
                fqdn = self.base + link['href']
                if re.match(self.base + '/wikis/.+', fqdn) and self.__relevant(fqdn): neighbors.append(fqdn)
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
            if self.scraper.update(node) == 0: pass
            else:
                continue
            self.explored.add(node)
            for neighbor in self.__get_neighbors():
                if neighbor not in self.frontier and neighbor not in self.explored:
                    self.frontier.append(neighbor)
            self.scraper.scrape()
