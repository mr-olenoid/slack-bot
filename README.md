# salck-bot
Just random slack bot example with ability to deploy in docker.

Config file config.json should be placed in app dir.
```josn
{ "SLACK_BOT_TOKEN" : "", 
"SLACK_VERIFICATION_TOKEN" : "", 
"SLACK_SIGNING_SECRET" : "" }
```
Docker-compose example.
```yaml
version: '3.3'
services:
  slackbot:
    image: olenoid/slack-bot:latest
    networks:
     - traefik-public
    deploy:
      labels:
        traefik.docker.network: traefik-public
        traefik.enable: 'true'
        traefik.http.routers.slackbot.entrypoints: websecure
        traefik.http.routers.slackbot.rule: Host("bot.kube.in.ua")
        traefik.http.routers.slackbot.tls.certresolver: myresolver
        traefik.http.services.slackbot.loadbalancer.server.port: '80'
    configs:
      - source: bot_config
        target: /app/config.json

networks:
  traefik-public:
    external: true

configs:
  bot_config:
    external: true
```
