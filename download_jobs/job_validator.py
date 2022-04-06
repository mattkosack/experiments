import os
import time
import dotenv
import csv
from search_iterator import SearchIterator
from regulations_api import RegulationsAPI
from data_storage import DataStorage


class WorkGenerator:

    def __init__(self, api, datastorage):
        self.api = api
        self.datastorage = datastorage

    def download(self, endpoint):
        beginning_timestamp = '1972-01-01 00:00:00'
        f = open(f'missing_{endpoint}.csv', 'w')
        writer = csv.writer(f)
        writer.writerow(['job_id', 'job_url', 'job_type'])
        counter = 0
        for result in SearchIterator(self.api, endpoint, beginning_timestamp):
            if result == {}:
                continue
            for r in result['data']:
                if not self.datastorage.exists(r):
                    print(r['id'])
                    writer.writerow([r['id'], r['links']['self'], r['type']])
                counter += 1
        f.close()


def generate_work():
        # Gets an API key
        dotenv.load_dotenv()
        api = RegulationsAPI(os.getenv('API_KEY'))
        storage = DataStorage()
        generator = WorkGenerator(api, storage)

        # generator.download('dockets')
        generator.download('documents')
        # generator.download('comments')

if __name__ == '__main__':
    generate_work()
