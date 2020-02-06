# README

Michael Barenstein pinged me over LinkedIn about finding shit for his
account.



## Breakdown Idea part deux

Start with a list of similar profiles.

For each of these, scrape out all the users (from comments) and
hashtags used.

For the list of hashtags, go through all of them with at least five
(?) uses. 

For each hashtag, get 100 images (or some other amount?) as a
proxy. Get the averages as a proxy for a sampling. (Get the total
counts somehow?). __finds candidate hashtags__

For each hashtag, also get each user. Get each user with high metrics
__finds candidate influencers__. All other users get put into
reachouts. 

For each user from the similar profile comments, get ones with high
metrics __finds candidate influencers__ and all other users as
reachouts.



## Scraped Metadata JSON

  * GraphImages -> list of all images scraped from a user

    * '__typename': specifies the media type
    * 'comments': has key 'data', contains the comments (not all though, why?)

      * 'created_at' =>  timestamp, looks like unix
      * 'id'
      * 'owner' =>  dictionary of [id, profile_pic_url, username]
      * 'text' =>  this is the category text

    * 'comments_disabled' =>  boolean
    
    * 'dimensions'
    
    * 'display_url' =>  image url
    
    * 'edge_media_preview_like' =>  ['count'] =>  this is the likes
      count
    
    * 'edge_media_to_caption' =>  ['edges'] =>  ['node'] =>  ['text']
      for caption text
       
    * 'edge_media_to_comment' => ['count'] =>  number of comments(?)
    * 'gating_info'
    * 'id' =>  ? def not the id in the URL
    * 'is_video' =>  boolean
    * 'media_preview'
    * 'owner'
    * 'shortcode'
    * 'tags'
    * 'taken_at_timestamp' =>  unix timestamp when this was taken
    * 'thumbnail_resources' =>  resized images
    * 'thumbnail_src' =>  literally no idea
    * 'urls': the url, list for some reason
    * 'username': self explanatory

  * GraphProfileInfo -> profile metadata


## How scraper works

```python
class InstagramScraper(object):

    def __init__(self, **kwargs):
        # ... defauilts below
        username="",
        usernames=[],
        filename=None,
        login_user=None,
        login_pass=None,
        followings_input=False,
        followings_output="profiles.txt",
        destination="./",
        logger=None,
        retain_username=False,
        interactive=False,
        quiet=False,
        maximum=0,
        media_metadata=False,
        profile_metadata=False,
        latest=False,
        latest_stamps=False,
        cookiejar=None,
        filter_location=None,
        filter_locations=None,
        media_types=["image", "video", "story-image", "story-video"],
        tag=False,
        location=False,
        search_location=False,
        comments=False,
        verbose=0,
        include_location=False,
        filter=None,
        proxies={},
        no_check_certificate=False,
        template="{urlname}",
        log_destination="",

def main():

    # ...

    scraper = InstagramScraper(**vars(args))

    if args.login_user and args.login_pass:
        scraper.authenticate_with_login()
    else:
        scraper.authenticate_as_guest()

    if args.followings_input:
        scraper.usernames = list(scraper.query_followings_gen(scraper.login_user))
        if args.followings_output:
            with open(scraper.destination+scraper.followings_output, 'w') as file:
                for username in scraper.usernames:
                    file.write(username + "\n")
            # If not requesting anything else, exit
            if args.media_types == ['none'] and args.media_metadata is False:
                scraper.logout()
                return

    if args.tag:
        scraper.scrape_hashtag()
    elif args.location:
        scraper.scrape_location()
    elif args.search_location:
        scraper.search_locations()
    else:
        scraper.scrape()

    scraper.save_cookies()
```



## GHs

  - https://github.com/rarcega/instagram-scraper (one mega
    InstagramScraper object)
    
  - ScriptSmith/insta-scrape
