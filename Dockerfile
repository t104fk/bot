FROM mhart/alpine-node

WORKDIR /src
ADD . .

ENV HUBOT_SLACK_TOKEN xoxb-17657069313-hBJBszmHDdChQAYcD1N8Xwkx

EXPOSE 3000
CMD ["./bin/hubot", "-a", "slack", "-n", "rinchan"]

