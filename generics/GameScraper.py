#!/usr/local/bin/oython

''' GameScraper.py
    --------------
    @author = Ankai Lou
    -------------------
    Class description for MMRICA Web Scraper for singular pages
'''

###############################################################################
######################## import libraries & frameworks ########################
###############################################################################

import os
import sys
from time import time
from urllib2 import urlopen
from bs4 import BeautifulSoup
from util import *

###############################################################################
################### Class definition for GameScraper object ###################
###############################################################################

class GameScraper(object):
    def __init__(self, gt, gp, pt, pc, bt, bp, home='html/'):
        ''' function: constructor
            ---------------------
            instantiate game scraper object for site type
            ---------------------------------------------
            @gt      list of css selectors for game title, or str
            @gp      list of css selectors for game platform, or str
            @pt      list of css selectors for page title
            @pc      list of css selectors for page content
            @bt      list of css selectors for bad tags to be sanitized
            @bp      list of sub-names of pages not to be created, e.g. Home
            @home    directory path for generated html files
        '''
        # objects used for scraping
        self.soup = None

        # selectors & strings for content generation
        self.game = [gt, gp]
        self.page = [pt, pc]
        self.bad_tags = bt
        self.bad_page = bp
        self.bad_char = [':', ';', ',', '/', '*', '^', '$', '@', '!']

        # base directory & generation
        self.home = os.path.join(os.getcwd(), home)
        if not os.path.exists(home): os.makedirs(self.home)

    ###########################################################################
    ############## helper functions for file generation process ###############
    ###########################################################################

    def __generate_html(self):
        ''' function: generate_html
            -----------------------
            generate HTML file from parse tree @soup and selectors
            ------------------------------------------------------
        '''
        # scrape information from @soup
        game = []
        for g in self.game:
            game.append(self.__pull(g, 'text') if type(g) is list else str(g))
        self.__generate_split(game) if type(self.page[1]) is dict else self.__generate_single(game)

    def __generate_single(self, game):
        ''' function: generate_single
            -------------------------
            generate single html file from game/page information
            ----------------------------------------------------
            @game    list containing game title and platform information
        '''
        page = []
        for p in self.page: page.append(self.__pull(p, 'html'))
        filename = ' '.join([e.get_text().strip() for e in page[0]])
        self.__generate_file(filename, game, page, None)

    def __generate_split(self, game):
        ''' function: generate_split
            ------------------------
            generate multiple html files from game/page information
            -------------------------------------------------------
            @game    list containing game title and platform information
            @split   dictionary of category/selector pairs for splitting
        '''
        for selector, category in self.page[1].iteritems():
            tags = self.__pull([selector], 'html')
            for content in tags:
                title = []
                for pt in self.page[0]: title = title + content.select(pt)
                filename = ' '.join([e.get_text().strip() for e in title])
                self.__generate_file(filename, game, [[], content], category)

    def __generate_file(self, filename, game, page, category=None):
        ''' function: generate_file
            -----------------------
            name, open and write @page information to file
            ----------------------------------------------
            @filename    string representing base name of the file
            @game        list containing game title and platform information
            @page        list containing page title and content information
            @category    OPTIONAL category for the full filename
        '''
        if any(len(p.findAll(text=True)) > 0 for p in page[1]) and len(filename) > 0 and not any(s in filename for s in self.bad_page):
            print 'Generating HTML file for content: %s.' % filename

            # append/prepend game information to full filename
            if category:         filename = category + ' ' + filename
            if len(game[0]) > 0: filename = game[0]  + ' ' + filename
            if len(game[1]) > 0: filename = filename + ' ' + game[1]

            # filter out illegal characters for filename
            for c in self.bad_char: filename = filename.replace(c, '')

            # open, create, and write to file
            file = open(os.path.join(self.home, '[MMRICA] %s.html' % filename), 'w')
            file.write('<html>\n<head></head>\n<body>')
            for tag in page:
                for content in tag:
                    content = self.__finalize_extract(content)
                    body = unicode(content).strip().encode('ascii','ignore')
                    file.write(body)
            file.write('</body>\n</html>')
            file.close()
        else:
            print 'Blacklisted page or content length/filename too short.'

    ###########################################################################
    ########## helper functions for scraping content from self.soup ###########
    ###########################################################################

    def __pull(self, selectors, format='text'):
        ''' function: pull
            --------------
            pull out tags or text based on list @selectors and sanitize
            -----------------------------------------------------------
            @selectors  list of str for css selectors to extract
            @format     html: HTML tag list([]); text: joined text str()
        '''
        content = []
        for selector in selectors:
            content = content + self.__sanitize(self.soup.select(selector))

        if format == 'html': pass
        elif format == 'text':
            content = ' '.join([t.get_text().strip() for t in content])
        else:
            print 'Invalid format type %s for generating content...' % format
            content = ''
        return content

    def __sanitize(self, content):
        ''' function: sanitize
            ------------------
            clean HTML tags to ensure Watson compatibility
            ----------------------------------------------
            @content    string to be sanitized for Watson compatibility
        '''
        for tag in content:
            for selector in self.bad_tags: self.__safe_extract(tag, selector)
            # TODO: Flatten <td/tr> with <span> child for IGN
            # TODO: ADD ADDITIONAL SANITIZATION STEPS HERE
        return content

    def __safe_extract(self, content, selector):
        ''' function: safe_extract
            ----------------------
            replace all of a certain tag in parse tree with <span>
            ------------------------------------------------------
            @content    string to have @selector replaced with <span>
            @selector   css selector representing tag to be safe extracted
        '''
        for url in content.select(selector):
            span = self.soup.new_tag('span')
            span.string = ''.join(url.findAll(text=True))
            url.replace_with(span)
        return content

    def __finalize_extract(self, content):
        ''' function: finalize_extract
            --------------------------
            extract all useless tags in bulk before file write
            --------------------------------------------------
            @content    bs4 tag ready for finalization of tag extraction
        '''
        for t in content.findAll(lambda tag: tag.name == 'span' and not tag.contents and (tag.string is None or not tag.string.strip())):
            t.extract()
        return content

    ###########################################################################
    ########### callable functions from outside object declaration ############
    ###########################################################################

    def scrape(self, url=None):
        ''' function: scrape
            ----------------
            compile content from @url into HTML file in @self.home
            ------------------------------------------------------
            @url    str for fully-qualified url to scrape for content
            @split  dictionary of categorys to split page
        '''
        start = time()
        if url:
            code = self.update(url)
            if code == 0: pass
            elif code == 1:
                print 'Processing Error when scraping url: %s' % url
                return
            elif code == 127:
                sys.exit(127)
        if self.soup:
            self.__generate_html()
            print 'URL scraped in: %s seconds!' % str(time() - start)
        else:
            print 'Nothing to scrape. Try again with an actual URL.'

    def update(self, url):
        ''' function: update
            -----------------
            error-free way to attempt to open/parse url
            -------------------------------------------
            @url    string representing fqdn to attempt to open/parse
        '''
        try:
            self.soup = BeautifulSoup(urlopen(url), 'html.parser')
            code = 0
        except KeyboardInterrupt:
            print 'Process terminated for url: %s' % url
            code = 127
        except:
            code = 1
        return code

