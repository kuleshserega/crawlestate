import requests

from flask_settings import BASE_SCRAPYD_URL, RUN_SPIDER


def run_spiders():
    run_url = BASE_SCRAPYD_URL % RUN_SPIDER

    centadata_data = {"project": "crawlestate", "spider": "centadata"}
    requests.post(run_url, centadata_data)

    centadata_data = {"project": "crawlestate", "spider": "midlandici"}
    requests.post(run_url, centadata_data)


if __name__ == '__main__':
    run_spiders()
