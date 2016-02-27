MMRICA-scraping
===============

## Table of Contents
1. [Overview](#overview)
2. [Module Description](#description)
3. [Usage](#usage)
4. [Development](#development)
5. [License](#the-mit-license)

## Overview
The purpose of this module is to provide a framework for implementing clean, modular, and 
extensible web scrapers/crawlers for the MMRICA question-answering web application for games. 

The purpose of these web crawlers/scrapers is to intelligently curate and extract relevant 
content and information from various video game walkthrough/cheat/dossier sites. The objective 
is to implement an intelligent, robust, and efficient crawler that selects URLs based on a 
relevance score using context derived from site structure, page content, and NLP. 

Currently there are working implementations of scrapers/crawlers for IGN wiki/cheat pages 
and general Wikia/Wiki pages. The selection process excludes meta-pages, embedded images/videos,
main/home pages, dead/orphaned pages, and other sites that lack enough relevant content for the 
Watson API to ingest and utilize.

This module provides an API/skeleton for extending and implementing additional Scraper and 
Crawler classes from the generics.WebScraper and generics.WebCrawler class definitions. The 
goal is to implement scraping to be robust, powerful, and fault-tolerant - as well as an 
efficient and flexible superclass implementation of crawling.

## Description
This python module contains the following files and directories:

* IGNCrawler.py   -- extension of generics.WebCrawler to scrape cheat/wiki sites from IGN
* WikiaCrawler.py -- extension of generics.WebCrawler to scrape general wikia/wiki site
* generics/
  * \_\_init\_\_.py
  * GameScraper.py -- module containing class definition for generic, extensible Web Scraper
  * GameCrawler.py -- module containing class definition for generic, extensible Web Crawler
  * util.py -- module containing useful helper function(s) for scraping - e.g. deHTMLfy
* html/  -- auto-generated .html files
* seed/  -- .txt files for testing scrapers/crawlers

## Usage
Ensure python and the beautifulsoup4 library is installed:

* python IGNCrawler.py [file/url, [...]]
  * file -- .txt file w one URL/file per line
  * url  -- fully-qualified domain name to scrape

## Development
This module was developed and tested on Python 2.7.5 and OS 10.11.3

The following Python 2.7.5 packages were used in development:

* os, sys, time
* beautifulsoup4
* urllib2
* urlparse
* re
* json
* hashlib

At the moment, crawling is implemented using breadth first search. Relevance selection 
returns True/False. Future iteration will include a more granular scoring for relevance based 
on page content, HTML structure, site quality, and application of NLP/ML concepts. A more 
precise relevance function will allow web crawling to implement a PageRank-esque indexing
algorithm that allows for efficient search/traversal algorithms - e.g. A-star, Djikstra's, etc.

The GameScraper.py class sanitizes HTML files by flattening uneven \<table\> elements, 
converting content to ascii, and extracting comments, empty tags, and irrelevant tags - 
e.g. links, images, videos, iframes, etc.

The GameScraper.py class supports generation of clean HTML files for URls. At the moment, the 
basic class definition supports 1-to-1, 1-to-many, and many-to-1 URL to document matching and 
generation. All generated content is deHTMLfied using an md5 hexdump to allow for Watson ingestion.

### API for Extended Scrapers/Crawlers

The __generics__ package is implemented to allow for simple extension and integration of the 
base GameScraper.py and GameCrawler.py classes to adapt to various site structure. Note that
GameScraper.py has enough self-sufficient functionality to scrape sites - GameCrawler.py must 
be extended with certain key methods implemented in order to have relevant functionality.

To implement an extension of GameScraper.py:

The GameScraper class constructor has the following fields:

* @gt -- string representing game title or list of selectors to extract title from URL
* @gp -- string representing game platforms of list of selectors to extract platforms from URL
* @pt -- list of css selectors for extracting page titles from URLs
* @pc -- list of css selectors for extracting page content from URLs
* @bt -- list of css selectors for irrelevant tags to be filters from content during sanitization
* @bp -- list of strings representing substrings of page names to be blacklisted from the scraping
* @home -- base directory to store generated HTML files - auto-generated if non-existent

These fields must be supplied with values in the class constructor of the subclass - with the 
addition of new fields. The following methods from inherited and available for overriding:

* __generate_html(self)
* __generate_single(self, game)
* __generate_split(self, game)
* __generate_file(self, game, page, category=None)
* __pull(self, selectors, format='text')
* __sanitize(self, content)
* __safe_extract(self, content, selector)
* __final_extract(self, content)
* scrape(self, url=None)
* update(self, url)

The documentation for these methods and the parameters/return values are found in the 
class definition for GameScraper.py. Extension of this module is permitted under the assumption
that the parameter/return values will remaining the same type and structure in order to integrate 
smoothly into other components -- e.g. GameCrawler, etc.

To implement an extension of GameCrawler.py:

The GameCrawler class constructor has the following fields:

* @scraper  -- GameScraper object or functional instantiation of a subclass Scraper class
* @selector -- dictionary of (keyword, selector) pairs for use during neighbor URL retrieval
* @base     -- optional parameter providing a base URL for certain sites that do not link full FQDNs

The following functions __MUST__ be overridden and implemented as their base definitions do 
not perform any relevant operations.

* __relevant(self, url)
* __get_neighbors(self)

Note that a GameCrawler object and subclass must be provided with a functional GameScraper or 
subclass object in order to function. Many of the function-calls during the crawling process 
reference the current @soup parameter of the provided crawler to extract information. This 
dependency was inserted in order to prevent multiple calls to urllib2/bs4 for the same URL.

### Contributors
* Ankai Lou (lou.56@osu.edu)

## The MIT License

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
