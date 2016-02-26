#!/usr/local/bin/python

''' wiki_crawl.py
    -------------
    @author = Ankai Lou
    -------------------
    Module for crawling and curating generic Wikia pages to scrape
'''

import sys
import os
import re
import urllib2
from time import time
from json import loads
from bs4 import BeautifulSoup
from urlparse import urlparse, urljoin
from scraper import scrape

###############################################################################
############################## global veriables ###############################
###############################################################################

wiki_base = None
selectors = {'menu'   : 'div#p-Navigation div.pBody a',
             'nav'    : 'nav.WikiNav li.nav-item .subnav-2-item a',
             'embed1' : 'div#bodyContent a',
             'embed2' : 'div#WikiaArticle a' }

###############################################################################
################ helper functions to crawl & curate wiki pages ################
###############################################################################

def __relevant(url):
    ''' function: relevant
        ------------------
        determine if url contains relevant content
    '''
    global wiki_base
    if re.match(wiki_base + '.+', url)\
       and url.count(':') < 2\
       and url.count('#') == 0:
        return True
    return False

def __append_sublist(lis, sublis):
    ''' function: append_sublist
        ------------------------
        extract links recursively down sublists
    '''
    for d in sublis:
        lis.append(ign_base + d['href'])
        if d.has_key('sub'): __append_sublist(lis, d['sub'])

def __get_neighbors(url):
    ''' function: get_neighbors
        -----------------------
        return list of non-visited neighbors of @url
    '''
    neighbors = list()
    try:
        soup = BeautifulSoup(urllib2.urlopen(url).read(), 'html.parser')
    except:
        print 'Cannot get neighbors from argument:', url
        return neighbors

    for link in soup.select(selectors['menu']) + soup.select(selectors['nav']):
        neighbors.append(urljoin(wiki_base,link['href']))
    for link in soup.select(selectors['embed1']) + soup.select(selectors['embed2']):
        if link.has_attr('href'):
            fqdn = urljoin(wiki_base,link['href'])
            if re.match(wiki_base + '.+', fqdn): neighbors.append(fqdn)
    return neighbors

def crawl(url, html='../html/wikia/'):
    ''' function: crawl
        ---------------
        bfs traversal of urls in main content section of @url
    '''
    global wiki_base
    start = time()
    parsed_uri = urlparse(url)
    netloc = '{uri.netloc}'.format(uri=parsed_uri)
    wiki_base = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    explored, frontier = set(), list()
    if url not in explored: frontier.append(url)
    while len(frontier) > 0:
        node = frontier.pop(0)
        explored.add(node)
        for neighbor in __get_neighbors(node):
            if neighbor not in frontier and neighbor not in explored:
                frontier.append(neighbor)
        if __relevant(node):
            scrape(node, html, netloc)
    print 'Crawling complete in', time() - start, 'seconds'
    return explored

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
            crawl(arg)
    print 'Total time elapsed:', time() - total_start, 'seconds'

if __name__ == '__main__':
    main(sys.argv[1:])

