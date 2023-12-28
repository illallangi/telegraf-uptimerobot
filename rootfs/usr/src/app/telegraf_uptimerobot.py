from typing import Dict
from click import STRING, command, option
from json import dumps
from yarl import URL

from telegraf_pyplug.main import print_influxdb_format
from requests import post as http_post

METRICNAMEDEF = "uptimerobot"
UPTIMEROBOTAPIURIDEF = "https://api.uptimerobot.com/v2"


@command()
@option("--metric-name", type=STRING, required=False, default=METRICNAMEDEF)
@option("--uptimerobot-api-key", envvar="UPTIMEROBOT_API_KEY", type=STRING)
@option(
    "--uptimerobot-api-url",
    envvar="UPTIMEROBOT_API_URL",
    type=STRING,
    default=UPTIMEROBOTAPIURIDEF,
)
@option(
    "--json",
    is_flag=True,
)
def cli(metric_name, uptimerobot_api_key, uptimerobot_api_url, json):

    uptimerobot_api_url = (
        uptimerobot_api_url
        if isinstance(uptimerobot_api_url, URL)
        else URL(uptimerobot_api_url)
    )

    if uptimerobot_api_key:
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache",
        }

        data = {
            "api_key": uptimerobot_api_key,
            "format": "json",
            "response_times": 1,  # Include response times
            "response_times_average": 15,  # 15 min intervals
            "response_times_limit": 16,  # return the last 4 hours - 4*4
        }

        r = http_post(
            uptimerobot_api_url / "getMonitors",
            headers=headers,
            data=data,
        )

        result = r.json()

        if result["stat"] != "ok":
            assert False, result["stat"]

        for monitor in result["monitors"]:
            if json:
                print(dumps(monitor))
                continue

            tags: Dict[str, str] = {
                "id": monitor["id"],
                "url": monitor["url"],
            }
            for responsetime in monitor.get("response_times", []):
                fields: Dict[str, float] = {"response_time": responsetime["value"]}

                print_influxdb_format(
                    measurement=metric_name,
                    tags=tags,
                    fields=fields,
                    nano_timestamp=int(responsetime["datetime"]) * 1000000000,
                )


if __name__ == "__main__":
    cli()
