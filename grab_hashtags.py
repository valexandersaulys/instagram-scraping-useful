import sys
import re
import json
import pprint
from collections import Counter

hashtag_regexp = re.compile("#(\w*)\s?")

if __name__ == "__main__":

    print("Processing %s" % sys.argv[1])

    with open(sys.argv[1], "r") as f:
        J = json.load(f)["GraphImages"]  # no care for GraphProfileInfo right now

    list_of_hashtags = []
    number_of_comments = 0

    for j in J:
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

    c = Counter(list_of_hashtags)

    print("Number of comments read: %d => Now writing to file" % number_of_comments)
    with open("output.txt", "wt") as out:
        pp = pprint.PrettyPrinter(indent=2, stream=out)
        pp.pprint(c)

    # scrape the hashtags next
