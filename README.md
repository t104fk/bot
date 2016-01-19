# bot

This bot work on heroku and post to slack.  

## Setup
### Configuration
```sh
heroku addons:create redistogo:nano
heroku config:set HUBOT_SLACK_TOKEN=XXXXX
heroku config:add TZ=Asia/Tokyo
heroku config:set HUBOT_HEROKU_KEEPALIVE_URL=$(heroku apps:info -s  | grep web-url | cut -d= -f2)
heroku config:add HUBOT_HEROKU_WAKEUP_TIME=07:00
heroku config:add HUBOT_HEROKU_SLEEP_TIME=01:00
```
### Scheduler
If free, [Heroku app sleep 6 hours/day, and stopped](https://blog.heroku.com/archives/2015/5/7/new-dyno-types-public-beta#hobby-and-free-dynos).  
So, set scheduler to [awake heroku hubot](https://github.com/hubot-scripts/hubot-heroku-keepalive#waking-hubot-up).
```
Note:
  Even if you add config variable of TZ, Heroku Scheduler only run on UTC.
  So you have to add the proper UTC offset.
```
