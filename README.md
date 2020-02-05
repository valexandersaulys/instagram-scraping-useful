# README

Michael Barenstein pinged me over LinkedIn about finding shit for his
account.



## Breakdown Idea

(from standard notes 2020-02-04)

Start with a list of similar profiles.

Grab all users’ posts' metadata (at least until I'm blocked). Also get
metadata, include hashtags and commentary. Arrange these in a masonry
layout.  

Then scrape hashtags from these — particularly metadata on these hashtags. 

Can I query hashtag metadata? Thinking popularity and such =>  use the
rarcega variant to scrape out X posts for a hashtag and estimate
popularity. 

Use pseudo metrics like follower ratios, likes/comment ratios, length
of average comments => some mixture to get an engagement metric of
some sort for ranking value of a particular account 

Then build a distributed crawler with many tiny machines that read
from Celery Reddis queue (like $5 servers) and then write the output
to s3. 


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


GHs

  - https://github.com/rarcega/instagram-scraper (one mega
    InstagramScraper object)
    
  - ScriptSmith/insta-scrape
