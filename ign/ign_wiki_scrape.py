#!/usr/local/bin/python

''' ign_wiki_scrape.py
    ------------------
    @author = Ankai Lou
    -------------------
    Module for scraping, preprocessing, and compiling IGN wiki pages into HTML
'''

import sys
import os
from time import time
from itertools import product
from urllib2 import urlopen
from bs4 import BeautifulSoup

###############################################################################
############################## global veriables ###############################
###############################################################################

html_dir = '../html/ign/'
bad_tags = ['div.gh-next-prev-buttons', 'img', 'p.wiki-videoEmbed']
selectors = {'gt' : 'h2.contentTitle a',
             'pt' : 'h1.gh-PageTitle',
             'gp' : 'div.contentPlatformsText span a',
             'pc' : 'div.grid_12.push_4.alpha.omega.bodyCopy.gh-content'}

###############################################################################
############### helper functions for web scraping IGN wiki pages ##############
###############################################################################

def __generate_html(gt, gp, pt, pc):
    ''' function: generate_html
        -----------------------
        generate clean html files for Watson ingestion in @html_dir
    '''
    if not os.path.exists(html_dir): os.makedirs(html_dir)

    if len(pc) > 0:
        filename = ' '.join([str(t) for t in gt])\
                 + ' - ' + ' '.join([str(t.get_text().strip()) for t in pt])\
                 + ' - ' + ' '.join([str(p) for p in gp]) + '.html'
        print 'Generating file:', filename
        file = open(os.path.join(html_dir, filename.replace('/',' - ')), 'w+')
        file.write('<html>\n<head></head>\n<body>')
        for p in pt: file.write(unicode(p).strip().encode('ascii','ignore'))
        for p in pc: file.write(unicode(p).strip().encode('ascii','ignore'))
        file.write('</body>\n</html>')
        file.close()
    else:
        print 'Content length too short. No file generated.'

def __sanitize_html(content):
    ''' function: sanitize_html
        -----------------------
        extract unnecessary <a>, <img>, and other tags from html content
    '''
    tmp = BeautifulSoup('', 'html.parser')
    for tree in content:
        for a in tree.select("a"):
            p = tmp.new_tag("p")
            p.string = a.get_text().strip()
            a.replace_with(p)
    for t in [tag
              for tree, selector in product(content, bad_tags)
              for tag in tree.select(selector)]: t.extract()

    return content

def scrape_url(url):
    ''' function: scrape_url
        --------------------
        compile relevant title, content, and system into HTML document
    '''
    start = time()
    try:
        soup = BeautifulSoup(urlopen(url), 'html.parser')
    except KeyboardInterrupt:
        print 'Process Terminated.'
        sys.exit(1)
    except:
        print 'Argument', url, 'cannot be processed...'
        return

    gt = [e.get_text().strip() for e in soup.select(selectors['gt'])]
    gp = [e.get_text().strip() for e in soup.select(selectors['gp'])]
    pt = __sanitize_html(soup.select(selectors['pt']))
    pc = __sanitize_html(soup.select(selectors['pc']))
    __generate_html(gt, gp, pt, pc)
    print 'Document scraped in', time() - start, 'seconds'

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
            scrape_url(arg)
    print 'Total time elapsed:', time() - total_start, 'seconds'

if __name__ == '__main__':
    main(sys.argv[1:])
