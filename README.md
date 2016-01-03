# ske-blog-getter

This bot work on heroku and post to slack.  

## Setup
```sh
heroku addons:create redistogo:nano
heroku config:set HUBOT_SLACK_TOKEN=XXXXX
heroku config:add TZ=Asia/Tokyo
heroku config:set HUBOT_HEROKU_KEEPALIVE_URL=$(heroku apps:info -s  | grep web-url | cut -d= -f2)
```
