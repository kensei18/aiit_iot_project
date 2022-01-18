import csv
import datetime
import logging
import os
import pathlib
import sys
import time
from typing import List

import serial
from dotenv import load_dotenv

load_dotenv()

PORT = os.environ["SERIAL_PORT"]
BAUDRATE = os.environ.get("SERIAL_BAUDRATE") or 9600
INTERVAL = os.environ.get("REQUEST_INTERVAL") or 60


def init_logger(name=None):
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)
    stdout_handler.addFilter(lambda r: r.levelno <= logging.INFO)

    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(formatter)

    logger = logging.getLogger(name=name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    return logger


def request(logger):
    logger.info("Serial communication is starting.")

    with serial.Serial(port=PORT, baudrate=BAUDRATE, timeout=1) as ser:
        try:
            time.sleep(2)
            one_minute_later = datetime.datetime.now()
            while True:
                if datetime.datetime.now() < one_minute_later:
                    time.sleep(1)
                    continue
                one_minute_later = datetime.datetime.now() + datetime.timedelta(seconds=INTERVAL)

                logger.debug("write")
                ser.write(b"1")
                counter = 0
                while counter < 50:
                    data = ser.readline().decode()
                    if data:
                        logger.info(f"data: {data}")
                        write_to_csv(data.split(','))
                        break
                    time.sleep(0.1)

        except KeyboardInterrupt:
            logger.debug("finish")

    logger.info("Serial connection was closed.")


def write_to_csv(data: list):
    now = datetime.datetime.now()
    data.append(now)
    with open(f"{pathlib.Path(__file__).parent.parent}/data/{now.strftime('%Y%m%d')}.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(data)


def read_csv(filedate: datetime.datetime = None) -> List[dict]:
    if filedate is None:
        filedate = datetime.datetime.now()

    try:
        with open(f"{pathlib.Path(__file__).parent.parent}/data/{filedate.strftime('%Y%m%d')}.csv", "r") as f:
            reader = csv.reader(f)
            return [{'hip': row[0], 'back': row[1], 'timestamp': row[2]} for row in reader]
    except FileNotFoundError:
        return []


if __name__ == '__main__':
    request(init_logger())
