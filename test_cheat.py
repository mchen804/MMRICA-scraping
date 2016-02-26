#!/usr/local/bin/python

''' ign_wiki_scrape.py
    ------------------
    @author = Ankai Lou
    -------------------
    Module for scraping, preprocessing, and compiling IGN wiki pages into HTML
'''

import sys
import os
from generics.GameScraper import GameScraper
from time import time

###############################################################################
############################## global veriables ###############################
###############################################################################

bad_tags = ['a', 'div.gh-next-prev-buttons', 'img', 'p.wiki-videoEmbed']

gt = ['h2.contentTitle a']
gp = ['div.contentPlatformsText span a']

pt = ['h3.maintext16.bold.grey']
pc = []
categories = {'div#category_cheat div.cheatBody div.grid_12.omega' : 'Cheat',
              'div#category_unlockable div.cheatBody div.grid_12.omega' : 'Unlockable',
              'div#category_hint div.cheatBody div.grid_12.omega' : 'Hint',
              'div#category_easter-egg div.cheatBody div.grid_12.omega' : 'Easter Egg',
              'div#category_achievement div.cheatBody div.grid_12.omega' : 'Achievement'}

bp = []
home = 'html/ign/cheat/'

###############################################################################
##################### main function for testing purposes ######################
###############################################################################

def main(argv):
    ''' function: main
        --------------
        accept list of urls & filepaths to url lists as @argv
    '''
    total_start = time()
    scraper = GameScraper(gt, gp, pt, pc, bad_tags, bp, home, categories)
    for arg in argv:
        if os.path.isfile(arg):
            print 'Processing arguments in file:', arg
            for line in open(arg, 'r'): argv.append(line.rstrip())
        else:
            print 'Processing argument:', arg
            scraper.scrape(arg)
    print 'Total time elapsed:', time() - total_start, 'seconds'

if __name__ == '__main__':
    main(sys.argv[1:])
