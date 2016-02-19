#!/usr/local/bin/python

''' wiki_scrape.py
    --------------
    @author = Ankai Lou
    -------------------
    Module for scraping, preprocessing, and compiling Wikia pages to HTML
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

bad_page = ['Home', 'Main Page', 'Redirected']
bad_char = [':', ';', ',', '/', '*', '&', '^', '%', '$', '#', '@']
bad_tags = ['div.gh-next-prev-buttons', 'img', 'iframe']
selectors = {'pt' : 'h1#firstHeading, div.header-column.header-title',
             'gp' : 'table.infobox.bordered.vevent tr td b',
             'pc' : 'div#bodyContent, div#WikiaArticle'}

###############################################################################
################# helper functions for web scraping wiki pages ################
###############################################################################

def __generate_html(pt, pc, html_dir, header):
    ''' function: generate_html
        -----------------------
        generate clean html files for Watson ingestion in @html_dir
    '''
    if not os.path.exists(html_dir): os.makedirs(html_dir)
    filename = ' '.join([unicode(t.get_text().strip()).encode('ascii', 'ignore')
                         for t in pt]).strip('\n\t\r')
    if len(pc) > 0 and len(filename) > 0 and not any(s in filename for s in bad_page):
        for c in bad_char: filename = filename.replace(c, ' - ')
        print 'Generating file:', filename
        file = open(os.path.join(html_dir, header + " " + filename + ' Wikia.html'), 'w+')
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
            p = tmp.new_tag("span")
            p.string = a.get_text().strip('\n')
            a.replace_with(p)
    for t in [tag
              for tree, selector in product(content, bad_tags)
              for tag in tree.select(selector)]: t.extract()
    return content

def scrape(url, html=os.getcwd()+"../html/wikia/", header=""):
    ''' function: scrape
        ----------------
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

    pt = __sanitize_html(soup.select(selectors['pt']))
    pc = __sanitize_html(soup.select(selectors['pc']))
    __generate_html(pt, pc, html, header)
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
            scrape(arg)
    print 'Total time elapsed:', time() - total_start, 'seconds'

if __name__ == '__main__':
    main(sys.argv[1:])
