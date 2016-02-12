#!/usr/local/bin/python

''' ign_wiki_scrape.py
    ------------------
    @author = Ankai Lou
    -------------------
    Module for scraping, preprocessing, and compiling IGN wiki pages into HTML
'''

import sys
import os
import time
import itertools
import urllib2
from bs4 import BeautifulSoup

###############################################################################
############################## global veriables ###############################
###############################################################################

html_dir = 'html/'
garbage_tags = ['a', 'img', 'p.wiki-videoEmbed']
selectors = {'gTitle' : 'h2.contentTitle a',
             'pTitle' : 'h1.gh-PageTitle' ,
             'gPlat' : 'div.contentPlatformsText span a',
             'pCont' : 'div.grid_12.push_4.alpha.omega.bodyCopy.gh-content'}

###############################################################################
############### helper functions for web scraping IGN wiki pages ##############
###############################################################################

def __generate_html(game_title, game_platform, page_title, page_content):
    ''' function: generate_html
        -----------------------
        generate clean html files for Watson ingestion in /html/
    '''
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    # generate title from tags
    filename = ' '.join([ str(t.get_text().strip()) for t in page_title ])\
             + ' - ' + ' '.join([ str(t) for t in game_title]) + ' '\
             + ' '.join([ str(p) for p in game_platform])\
             + '.html'

    # generate file & contents
    print 'Generating file:', filename
    file = open(os.path.join(html_dir, filename), 'w+')
    file.write('<html>\n<head></head>\n<body>')
    for p in page_title:
        file.write(str(p).strip().decode('unicode_escape').encode('ascii','ignore'))
    for p in page_content:
        file.write(str(p).strip().decode('unicode_escape').encode('ascii','ignore'))
    file.write('</body>\n</html>')
    file.close()

def __sanitize_html(content):
    ''' function: sanitize_html
        -----------------------
        extract unnecessary <a>, <img>, and other tags from html content
    '''
    for t in [tag
              for tree, selector in itertools.product(content,garbage_tags)
              for tag in tree.select(selector)]: t.extract()
    return content

def compile_url(url):
    ''' function: compile_url
        ---------------------
        compile relevant title, content, and system into HTML document
    '''
    try:
        page = urllib2.urlopen(url)
    except:
        print 'Argument', url, 'cannot be processed...'
        return

    print 'Scraping url:', url
    soup = BeautifulSoup(page, 'html.parser')

    # select elements used in file title
    game_title = [e.get_text().strip() for e in soup.select(selectors['gTitle'])]
    game_platform = [e.get_text().strip() for e in soup.select(selectors['gPlat'])]

    # select elements used in file contents & sanitize
    page_title = __sanitize_html(soup.select(selectors['pTitle']))
    page_content = __sanitize_html(soup.select(selectors['pCont']))

    __generate_html(game_title, game_platform, page_title, page_content)


###############################################################################
##################### main function for testing purposes ######################
###############################################################################

def main(argv):
    ''' function: main
        --------------
        accept list of urls & filepaths to url lists as @argv
    '''
    total_start = time.time()
    for arg in argv:
        if os.path.isfile(arg):
            print 'Processing arguments in file:', arg
            for line in open(arg, 'r'): argv.append(line.rstrip())
        else:
            start = time.time()
            compile_url(arg)
            print 'Document scraped in', time.time() - start, 'seconds'
    print 'Total time elapsed:', time.time() - total_start, 'seconds'

if __name__ == '__main__':
    main(sys.argv[1:])
