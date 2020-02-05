# README

Michael Barenstein pinged me over LinkedIn about finding shit for his
account.



## Breakdown Idea part deux

(from standard notes 2020-02-04)

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
