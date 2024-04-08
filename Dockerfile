FROM docker:19.03.4

RUN apk update
RUN apk upgrade
RUN apk add --no-cache --update python3 python py-pip coreutils curl
RUN rm -rf /var/cache/apk/*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
RUN apk --purge -v del py-pip

ADD run.py /run.py
ADD entrypoint.sh /entrypoint.sh

RUN ["chmod", "+x", "/entrypoint.sh"]

ENTRYPOINT ["/entrypoint.sh"]