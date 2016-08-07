CronJob = require('cron').CronJob
skeblog = require('./skeblog')

# Description:
#   Daily job to scrape oya masana's SKE48 official blog
#   Each job will be executed every 15 minutes.
module.exports = (robot) ->
  robot.respond /skeblog get (.*)/i, (msg) ->
    member = msg.match[1]
    envelope = room: "C0HKD4CCQ"
    skeblog(robot, envelope, member)

  return

