FROM docker.io/library/python:3.10.4
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    XDG_CONFIG_HOME=/config \
    TELEGRAF_INTERVAL=300 \
    INFLUXDB_DATABASE=uptimerobot

RUN curl -s https://repos.influxdata.com/influxdb.key | apt-key add -
RUN echo "deb https://repos.influxdata.com/debian buster stable" > /etc/apt/sources.list.d/influxdb.list
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      telegraf=1.22.4-1 \
    && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY entrypoint.sh /entrypoint.sh
COPY telegraf.conf /etc/telegraf/telegraf.conf

COPY ./telegraf_uptimerobot.py /usr/src/app/telegraf_uptimerobot.py

ENTRYPOINT ["/entrypoint.sh"]
RUN chmod +x /entrypoint.sh
CMD ["/usr/bin/telegraf"]