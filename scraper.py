import argparse
import re
import requests
import sys
import pprint
from bs4 import BeautifulSoup

url_search = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]\
            |[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+;\?'

email_search = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'


def url_scraper(url):
    r = requests.get(url)
    pp = pprint.PrettyPrinter(indent=4)
    url_match = re.findall(url_search, r.text)
    email_match = re.findall(email_search, r.text)
    phone_match = re.findall(r'[\(]?\d{3}[\-, \)]?\d{3}[\-, \s]+\d{4}', r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    rel_links = []
    for rel_url in soup.find_all():
        rel_href = rel_url.get('href')
        rel_img = rel_url.get('img')
        if rel_href:
            rel_links.append(rel_href)
        elif rel_img:
            rel_links.append(rel_img)
    merged_lists = set(url_match + rel_links)
    pp.pprint(merged_lists)
    pp.pprint(email_match + phone_match)


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--tourl', help='URL to be scraped')

    return parser


def main(args):
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    if parsed_args.tourl:
        url_scraper(parsed_args.tourl)
    else:
        parser.print_usage()


if __name__ == '__main__':
    main(sys.argv[1:])
