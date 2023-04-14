FROM ghcr.io/illallangi/telegraf:v0.0.13
ENV INFLUXDB_DATABASE=uptimerobot

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY telegraf.conf /etc/telegraf/telegraf.conf

COPY ./telegraf_uptimerobot.py /usr/src/app/telegraf_uptimerobot.py
