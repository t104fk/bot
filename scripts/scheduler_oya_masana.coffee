CronJob = require('cron').CronJob
skeblog = require('./skeblog')

# Description:
#   Daily job to scrape oya masana's SKE48 official blog
#   Each job will be executed every 15 minutes.
module.exports = (robot) ->
  envelope = room: "C0HKD4CCQ"
  member = 'oya_masana'
  new CronJob('0 */1 * * * *', () ->
    skeblog(robot, envelope, member)
  , null, true, 'Asia/Tokyo')
  return

