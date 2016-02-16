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

* html/
  * auto-generated .html files
* ign/
  * ign_wiki_scrape.py - module to scrape IGN wiki pages into .html
  * ign_wiki_crawl.py - moedule to crawl over IGN wiki pages for curation
* seed/
  * ign_scrape_seed - test file for ign_wiki_scrape.py
  * ign_crawl_seed - test file for ign_wiki_crawl.py

## Usage
Ensure python and the beautifulsoup4 library is installed:

* python ign_wiki_scrape.py [file/url, [...]]
* python ign_wiki_crawl.py [file/url, [...]]

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
