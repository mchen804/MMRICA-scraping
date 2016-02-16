#!/usr/local/bin/python

''' ign_wiki_crawl.py
    -----------------
    @author = Ankai Lou
    -------------------
    Module for crawling and curating IGN wiki pages to scrape
'''

import sys
import os
import re
import urllib2
from time import time
from json import loads
from bs4 import BeautifulSoup

import ign_wiki_scrape as wiki_scrape

###############################################################################
############################## global veriables ###############################
###############################################################################

ign = 'http://www.ign.com'
explored = set()
selectors = {'menu'  : 'div.ghn-L1.ghn-hasSub',
             'embed' : 'div.grid_12.push_4.alpha.omega.bodyCopy.gh-content a' }

###############################################################################
################ helper functions to crawl & curate wiki pages ################
###############################################################################

def __relevant(url):
    ''' function: relevant
        ------------------
        determine if url contains relevant content
    '''
    if re.match(ign + '/wikis/.+/.+', url):
        return True
    else:
        return False

def __append_sublist(lis, sublis):
    ''' function: append_sublist
        ------------------------
        extract links recursively down sublists
    '''
    for d in sublis:
        lis.append(ign + d['href'])
        if d.has_key('sub'): __append_sublist(lis, d['sub'])

def __get_neighbors(url):
    ''' function: get_neighbors
        -----------------------
        return list of non-visited neighbors of @url
    '''
    neighbors = list()
    try:
        soup = BeautifulSoup(urllib2.urlopen(url).read(), 'html.parser')
    except KeyboardInterrupt:
        print 'Process Terminated'
        sys.exit(2)
    except:
        print 'Cannot get neighbors from argument:', url
        return

    for link in soup.select(selectors['menu']):
        for doc in loads(link['data-sub']):
            if doc.has_key('href'):
                neighbors.append(ign + doc['href'])
            if doc.has_key('sub'):
                __append_sublist(neighbors, doc['sub'])
    for link in soup.select(selectors['embed']):
        fqdn = ign + link['href']
        if re.match(ign + '/wikis/.+', fqdn): neighbors.append(fqdn)
    return neighbors

def crawl_url(url):
    ''' function: crawl_url
        -------------------
        bfs traversal of urls in main content section of @url
    '''
    explored = set()
    frontier = list()
    start = time()
    if url not in explored: frontier.append(url)
    while len(frontier) > 0:
        node = frontier.pop(0)
        explored.add(node)
        for neighbor in __get_neighbors(url):
            if neighbor not in frontier and neighbor not in explored: 
                frontier.append(neighbor)
        if __relevant(node):
            print 'Scraping:', node
            wiki_scrape.scrape_url(node)
    print 'Crawling complete in', time() - start, 'seconds'

###############################################################################
################## main function - single point of execution ##################
###############################################################################

def main(argv):
    ''' function: main
        --------------
        compile relevant urls to scrape via crawling wiki pages
    '''
    total_start = time()
    for arg in argv:
        if os.path.isfile(arg):
            print 'Processing arguments in file:', arg
            for line in open(arg, 'r'): argv.append(line.rstrip())
        else:
            print 'Processing argument:', arg
            crawl_url(arg)
    print 'Total time elapsed:', time() - total_start, 'seconds'

if __name__ == '__main__':
    main(sys.argv[1:])
