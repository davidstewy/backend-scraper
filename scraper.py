#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Using HTML Parser, scrapes a given URL for URLS, Emails, and Phone numbers
"""

# With help during mob coding session

__author__ = "davidstewy"

import argparse
import requests
import re
import sys
from HTMLParser import HTMLParser


class MyHTMLParser(HTMLParser):
    url_list = []
    email_list = []
    phone_list = []

    def handle_starttag(self, tag, attrs):
        """Search for URLs and Emails in the starting anchor tag"""
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href' and value.startswith('http'):
                    self.url_list.append(value)
                if attr == 'href' and value.startswith('mailto'):
                    self.email_list.append(value[7:])

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        """Search for phone numbers and emails matching the
        given regex patterns in between HTML tags """
        pattern_phone = r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?'
        phone_number_matches = re.findall(pattern_phone, data)
        for number in phone_number_matches:
            if number:
                self.phone_list.append(
                    number[0]+'-'+number[1]+'-'+number[2])
        pattern_email = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
        email_matches = re.findall(pattern_email, data)
        self.email_list.extend(email_matches)


def create_parser():
    """Builds parser"""
    parser = argparse.ArgumentParser(description='Scrapes given URL')
    parser.add_argument("url", help='website / URL to start scraping')
    return parser


def scrape(url):
    """Instantiate the parser and feed it some HTML"""
    r = requests.get(url)
    parser = MyHTMLParser()
    parser.feed(r.text)
    print '----URL List----'
    print '\n'.join(set(parser.url_list))
    print '----Email List----'
    print '\n'.join(set(parser.email_list))
    print '----Phone List----'
    print '\n'.join(set(parser.phone_list))


def main():
    parser = create_parser()
    args = parser.parse_args()

    if not args:
        parser.print_usage()
        sys.exit(1)

    scrape(args.url)


if __name__ == '__main__':
    main()
