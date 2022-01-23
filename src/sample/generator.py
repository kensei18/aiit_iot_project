import csv
import datetime
import json
import pathlib
import random

from src.serialclient.main import read_csv


def generate_csv_today(limit=60, is_hip_left=None, is_back_left=None):
    now = datetime.datetime.now()

    with open(f"{pathlib.Path(__file__).parent.parent}/data/{now.strftime('%Y%m%d')}.csv", "w") as f:
        writer = csv.writer(f)

        for _ in range(limit):
            hip_min = 0
            hip_max = 1
            if is_hip_left is not None:
                if is_hip_left:
                    hip_min = 1
                else:
                    hip_max = 0

            back_min = 0
            back_max = 1
            if is_back_left is not None:
                if is_back_left:
                    back_min = 1
                else:
                    back_max = 0

            row = [random.randint(hip_min, hip_max), random.randint(back_min, back_max), now]
            writer.writerow(row)
            now += datetime.timedelta(minutes=1)


def generate_json_today(filename, limit=60, is_hip_left=None, is_back_left=None):
    generate_csv_today(limit, is_hip_left, is_back_left)
    data = read_csv()

    with open(f"{pathlib.Path(__file__).parent}/json/{filename}.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    generate_json_today("random", limit=200)
    generate_json_today("completely_left", limit=200, is_hip_left=True, is_back_left=True)
    generate_json_today("only_back_left", limit=200, is_hip_left=False, is_back_left=True)
    generate_json_today("sitting", limit=200, is_hip_left=False, is_back_left=False)
