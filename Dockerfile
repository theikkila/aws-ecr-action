FROM docker:19.03.4

RUN apk update \
  && apk upgrade \
  && apk add --no-cache --update python py-pip coreutils \
  && rm -rf /var/cache/apk/* \
  && pip install awscli \
  && apk --purge -v del py-pip

ADD entrypoint.py /entrypoint.py

RUN ["chmod", "+x", "/entrypoint.py"]

ENTRYPOINT ["/entrypoint.py"]