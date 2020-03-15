FROM alpine

COPY src /root
COPY .env /root/.env

RUN apk --update add python3 transmission-daemon && rm -rf /var/cache/apk/*

ENTRYPOINT ["/root/run.sh"]
