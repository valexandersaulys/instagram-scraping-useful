#!/usr/bin/env python3
import sys

from scrape_functions import scrape_user


if __name__ == "__main__":
    scrape_user(user=sys.argv[1])
