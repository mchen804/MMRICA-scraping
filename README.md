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

* IGNCrawler.py   - extension of generics.WebCrawler to scrape cheat/wiki sites from IGN
* WikiaCrawler.py - extension of generics.WebCrawler to scrape general wikia/wiki site
* generics/
  * \_\_init\_\_.py
  * GameScraper.py - module containing class definition for generic, extensible Web Scraper
  * GameCrawler.py - module containing class definition for generic, extensible Web Crawler
* html/   auto-generated .html files
* seed/   .txt files for testing scrapers/crawlers

## Usage
Ensure python and the beautifulsoup4 library is installed:

* python IGNCrawler.py [file/url, [...]]

## Development
This module was developed and tested on Python 2.7.5 and OS 10.11.3

## Contributors
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
