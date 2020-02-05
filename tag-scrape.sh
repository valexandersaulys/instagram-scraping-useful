#!/bin/bash

# issue here: https://github.com/rarcega/instagram-scraper/pull/489
# running instagram-scraper==1.7.2

# commands not working
#      --retain-username \

.venv/bin/instagram-scraper wooliscruel --tag \
    --maximum 96 \
    --media-metadata \
    --media-types none \
    --comments \
    --destination wooliscruel.json
                            
