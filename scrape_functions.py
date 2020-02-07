import os
import json
from statistics import mean, stdev, median, variance
import concurrent
import itertools

import pandas as pd
from instagram_scraper.app import InstagramScraper

MAX_WORKERS = 16


def scrape_username(username="patagonia", dst="./", maximum=12):
    """grab the metadata for a username"""
    if not os.path.exists(os.path.join(dst, username, username + ".json")):
        scraper = InstagramScraper(
            login_user=os.environ.get("INSTAGRAM_USER", None),
            login_pass=os.environ.get("INSTAGRAM_PWD", None),
            usernames=username.split(","),
            destination=dst,
            maximum=maximum,
            comments=True,
            media_types="none",
            media_metadata=True,
            profile_metadata=True,
        )
        if os.environ.get("INSTAGRAM_USER", False):
            scraper.authenticate_with_login()
        else:
            scraper.authenticate_as_guest()
        scraper.scrape()

    f = open(os.path.join(dst, username, username + ".json"), "rt")
    j = json.load(f)
    f.close()
    return j


def try_get_user_stats(*args, **kwargs):
    try:
        return get_user_stats(*args, **kwargs)
    except:
        return {}


def get_user_stats(u, dst="./"):
    """Get the stats of a particular users"""

    if not os.path.exists(os.path.join(dst, u, u + ".json")):
        scraper = InstagramScraper(
            login_user=os.environ.get("INSTAGRAM_USER", None),
            login_pass=os.environ.get("INSTAGRAM_PWD", None),
            usernames=[u],
            destination=dst,
            maximum=12,
            comments=True,
            media_types="none",
            media_metadata=True,
            profile_metadata=True,
        )
        scraper.authenticate_as_guest()
        scraper.scrape()

    f = open(os.path.join(dst, u, u + ".json"), "rt")
    J = json.load(f)
    f.close()

    if (
        J["GraphProfileInfo"]["info"]["is_private"]
        or "GraphImages" not in J
        or len(J["GraphImages"]) < 2
    ):
        print("Skipping user %s" % J["GraphProfileInfo"]["username"])
        return {
            "followers_count": J["GraphProfileInfo"]["info"]["followers_count"],
            "following_count": J["GraphProfileInfo"]["info"]["following_count"],
            "username": J["GraphProfileInfo"]["username"],
            "avg_likes": None,
            "std_likes": None,
            "median_likes": None,
            "avg_comments": None,
            "std_comments": None,
            "median_comments": None,
            "hashtags_in_user": None,
        }

    likes_gen = [j["edge_media_preview_like"]["count"] for j in J["GraphImages"]]
    avg_likes = mean(likes_gen)
    std_likes = variance(likes_gen) ** (1 / 2)
    median_likes = median(likes_gen)

    comments_gen = [j["edge_media_to_comment"]["count"] for j in J["GraphImages"]]
    avg_comments = mean(comments_gen)
    std_comments = variance(comments_gen) ** (1 / 2)
    median_comments = median(comments_gen)

    list_of_hashtags = {}
    for image in J["GraphImages"]:
        if "tags" not in image:
            continue

        for tag in image["tags"]:
            if tag not in list_of_hashtags:
                list_of_hashtags[tag] = 0
            list_of_hashtags[tag] += 1

    d = {
        "followers_count": J["GraphProfileInfo"]["info"]["followers_count"],
        "following_count": J["GraphProfileInfo"]["info"]["following_count"],
        "username": J["GraphProfileInfo"]["username"],
        "avg_likes": avg_likes,
        "std_likes": std_likes,
        "median_likes": median_likes,
        "avg_comments": avg_comments,
        "std_comments": std_comments,
        "median_comments": median_comments,
        "hashtags_in_user": list_of_hashtags,
    }

    return d


def scrape_hashtag(hashtag="wooliscruel", dst="./"):
    """ """
    scraper = InstagramScraper(
        login_user=os.environ.get("INSTAGRAM_USER", None),
        login_pass=os.environ.get("INSTAGRAM_PWD", None),
        usernames=[hashtag],
        destination=dst,
        maximum=12,
        comments=True,
        media_types="none",
        media_metadata=True,
        profile_metadata=True,
        tag=True,
    )
    scraper.authenticate_as_guest()
    scraper.scrape()

    f = open(os.path.join(dst, hashtag, hashtag + ".json"), "rt")
    j = json.load(f)
    f.close()
    return j


def process_hashtags_from_comments(J):
    """Process all hashtags from the comments """
    list_of_hashtags = []
    number_of_comments = 0

    for j in J["GraphImages"]:
        h = hashtag_regexp.findall(
            j["edge_media_to_caption"]["edges"][0]["node"]["text"]
        )
        [list_of_hashtags.append(i) for i in h]

        # former for profiles, latter for hashtags
        if "comments" in j:
            comments = j["comments"]["data"]
        if "edge_media_to_comment" in j:
            comments = j["edge_media_to_comment"]["data"]

        number_of_comments += len(comments)
        for comment in comments:
            h = hashtag_regexp.findall(comment["text"])
            [list_of_hashtags.append(i) for i in h]

    return Counter(list_of_hashtags)


def process_users_commenting(J, dst="./"):
    """Process all the users who comment on a post, return their stats"""
    list_of_users_to_scrape = []
    for j in J["GraphImages"]:
        for comment in j["comments"]["data"]:
            list_of_users_to_scrape.append(comment["owner"]["username"])

    fs = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        print("- - - - - processing %d users" % len(list_of_users_to_scrape))
        for user in list_of_users_to_scrape:
            fs.append(executor.submit(try_get_user_stats, user, dst))

    list_of_user_stats, _ = concurrent.futures.wait(fs, timeout=60)
    list_of_user_stats = (x.result() for x in list_of_user_stats)
    list_of_user_stats = list(filter(lambda x: x, list_of_user_stats))

    return list_of_user_stats


def scrape_user(user="patagonia"):
    # example here
    # scrape a username:
    J = scrape_username(user, dst="./scrapes", maximum=12)
    list_of_user_stats = process_users_commenting(J, dst="./%s/%s" % ("scrapes", user))
    df = pd.DataFrame(list_of_user_stats)

    df["follower-following-ratio"] = df["followers_count"] / df["following_count"]
    df["comments_likes_ratio"] = df["avg_comments"] / df["avg_likes"]
    df.to_csv("user_stats_@%s.csv" % user)


def scrape_hashtag_fully(hashtag=""):
    J = scrape_hashtag(hashtag="wooliscruel", dst="./")
    list_of_user_stats = process_users_commenting(J, dst="./%s" % user)
    df = pd.DataFrame(list_of_user_stats)

    df["follower-following-ratio"] = df["followers_count"] / df["following_count"]
    df["comments_likes_ratio"] = df["avg_comments"] / df["avg_likes"]
    df.to_csv("user_stats_#%s.csv" % user)


def main():
    scrape_user()


if __name__ == "__main__":
    main()
