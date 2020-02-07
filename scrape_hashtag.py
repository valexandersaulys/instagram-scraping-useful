#!/usr/bin/env python3
import sys

from scrape_functions import scrape_hashtag_fully


if __name__ == "__main__":
    scrape_hashtag_fully(user=sys.argv[1])
