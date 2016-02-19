MMRICA-scraping
===============

## Table of Contents
1. [Overview](#overview)
2. [Module Description](#description)
3. [Usage](#usage)
4. [Development](#development)
5. [Contributors](#contributors)
6. [License](#the-mit-license)

## Overview
The purpose of this module is to implement intelligent web crawling and scraping for various game walkthrough/cheats/tips sites.

## Description
This python module contains the following files and directories:

* crawler.py - Unfinished generic url crawler
* html/
  * auto-generated .html files
* ign/
  * crawler.py - super-module for crawling/scraping IGN pages
  * wiki/
    * \_\_init\_\_.py
    * scraper.py - module to scrape IGN wiki pages into .html files
    * crawler.py - module to crawl over IGN wiki pages for curation
  * cheat/
    * \_\_init\_\_.py
    * scraper.py - module to scrape IGN cheat pages into multiple .html files
* wikia/
  * \_\_init\_\_.py
  * scraper.py - module for scraping Wikia pages
  * crawler.py - module for crawling over Wikia links
* seed/
  * ign_wiki_scraper_test - test file for ign/wiki/scraper.py
  * ign_wiki_crawler_test - test file for ign/wiki/crawler.py
  * ign_cheat_scraper_test - file file for ign/cheat/scraper.py
  * ign_crawler_test - test file for ign/crawler.py
  * wiki_scraper_test - test file for wikia/scraper.py
  * wiki_crawler_test _ test file for wikia/crawler.py

## Usage
Ensure python and the beautifulsoup4 library is installed:

* python ign/crawler.py [file/url, [...]]

## Development
This module was developed and tested on Python 2.7.5 and OS 10.11.3

## Contributors
* Ankai Lou (lou.56@osu.edu)

## The MIT License (MIT)

Copyright (c) 2016 Ankai Lou

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
