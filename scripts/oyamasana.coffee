client = require('cheerio-httpcli')
CronJob = require('cron').CronJob

BLOG_URL = 'http://www2.ske48.co.jp/blog_pc/detail/'

# Description:
#   Daily job to scrape oya masana's SKE48 official blog
#   Each job will be executed every 15 minutes.
module.exports = (robot) ->
  new CronJob('0 */15 * * * *', () ->
    member = 'oya_masana'
    client.fetch(BLOG_URL, writer: member).then((result) ->
      date = result.$('#sectionMain > .unitBlog > h3').text()

      # check the blog is already posted to slack
      key = 'current_' + member
      current = robot.brain.get key
      if date is current
        console.log 'The entry at ' + date + ', by ' + member +
          ' is already posted.'
        return

      blog = result.$('#sectionMain > .unitBlog > .box')
      title = blog.find('h3').text()
      img = /url\((.+)\)/.exec(blog.find('p').attr().style)[1]
      content = /<\/p>(.+)/.exec(blog.html().replace(/\r?\n/g, ''))[1]
      content = content.replace(/<br>/ig, '\n')

      envelope = room: "ske"
      robot.send envelope, bold(title) + '\n' +
        date + '\n' +
        img + '\n' +
        content

      # set posted date
      robot.brain.set key, date
    ).catch((err) ->
      console.log err
      return
    ).finally ->
      return
  , null, true, 'Asia/Tokyo')
  return

bold = (text) ->
  '*' + text + '*'
