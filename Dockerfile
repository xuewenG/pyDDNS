FROM python:3.7.10-stretch
LABEL maintainer="xuewenG" \
  site="https://github.com/xuewenG/pyDDNS"

ENV MY_HOME=/root
RUN mkdir -p $MY_HOME
WORKDIR $MY_HOME

COPY requirements.txt $MY_HOME
RUN set -x \
  && pip install -r requirements.txt

COPY . $MY_HOME

CMD ["python", "-u", "/root/main.py"]
