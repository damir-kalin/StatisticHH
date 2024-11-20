import os
import requests
from datetime import datetime, timedelta
from sys import argv
from dotenv import load_dotenv

import logging

load_dotenv()
HOST = os.getenv('API_HOST')
PORT = os.getenv('API_PORT')
URL = f"http://{HOST}:{PORT}/pipline"

file_log = logging.FileHandler(f'/app/logs/{datetime.now().strftime("%d-%m-%Y_%H:%M:%S")} incr_job.log')
console_out = logging.StreamHandler()
logger = logging.getLogger(__name__)
FORMAT = '[%(asctime)s | %(levelname)s]: %(message)s'
logging.basicConfig(handlers=(file_log, console_out), level=logging.INFO, format=FORMAT)

def main():
    logger.info("Start pipline.")
    params = {}
    if len(argv) > 1:
        params = {"dt":argv[1]}
    logger.info(params)
    requests.post(url=URL, params=params)
    logger.info('Pipline success.')

if __name__ == '__main__':
    main()