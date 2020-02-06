#!/bin/bash

# issue here: https://github.com/rarcega/instagram-scraper/pull/489
# running instagram-scraper==1.7.2

# commands not working
#      --retain-username \

.venv/bin/instagram-scraper patagonia \
    --maximum 96 \
    --profile-metadata \
    --media-metadata \
    --media-types none \
    --comments 

# --destination patagonia.json


# for just getting the user profile info
# .venv/bin/instagram-scraper ashlynglasheen --media-types none -m 0 --profile-metadata
