FROM docker:19.03.4

RUN apk update \
  && apk upgrade \
  && apk add --no-cache --update python3 python py-pip coreutils \
  && rm -rf /var/cache/apk/* \
  && pip install awscli \
  && apk --purge -v del py-pip

ADD run.py /run.py
ADD entrypoint.sh /entrypoint.sh

RUN ["chmod", "+x", "/entrypoint.sh"]

ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]