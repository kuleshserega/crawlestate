import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from flask_settings import BASE_SCRAPYD_URL, RUN_SPIDER

spyder_name = sys.argv[1]


def run_spiders(name='centadata'):
    run_url = BASE_SCRAPYD_URL % RUN_SPIDER

    centadata_data = {"project": "crawlestate", "spider": name}
    requests.post(run_url, centadata_data)


if __name__ == '__main__':
    run_spiders(spyder_name)
