FROM alpine

COPY src /root
COPY .env /root

RUN apk --update add bash python3 transmission-daemon && rm -rf /var/cache/apk/*

RUN mkdir -p /root/downloads

RUN python3 -m pip install -r /root/requirements.txt

ENV START_TRANSMISSION_DAEMON=1

ENTRYPOINT ["/root/run.sh"]
