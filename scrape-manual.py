#! /usr/bin/env python3
from instagram_scraper.app import InstagramScraper


if __name__ == "__main__":
    # grab only the metadata
    scraper = InstagramScraper(
        usernames=["patagonia"],  # 'username' arg does not work
        destination="./",
        maximum=12,
        comments=True,
        media_types="none",  # to not download media
        media_metadata=True,
        profile_metadata=True,
    )
    scraper.authenticate_as_guest()
    scraper.scrape()
    scraper.save_cookies()
