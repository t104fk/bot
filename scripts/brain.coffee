# Description:
#   Deal with hubot brain
module.exports = (robot) ->
  robot.respond /brain get (.*)/i, (msg) ->
    key = msg.match[1]
    value = robot.brain.get key
    unless value?
      msg.send "The key #{key} is not found＞＜"
    else
      msg.send value

  robot.respond /brain set (.*) (.*)/i, (msg) ->
    key = msg.match[1]
    value = msg.match[2]
    robot.brain.set key, value
    msg.send "The key #{key}, value #{value} have been set＞ω＜/"

  robot.respond /brain delete (.*)/i, (msg) ->
    key = msg.match[1]
    robot.brain.remove key
    msg.send "The key #{key} goes out＞ω＜/"

  return

