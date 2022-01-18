import datetime
from typing import List, Optional

from fastapi import FastAPI, Query

from src.serialclient.main import read_csv

app = FastAPI()


@app.get("/latest")
async def read_latest_data(limit: Optional[int] = Query(60, description="取得したい件数")) -> List[dict]:
    data = read_csv()[-limit:]
    length = len(data)

    if length < limit:
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        yesterday_data = read_csv(yesterday)[-limit + length:]
        data = yesterday_data + data

    return data
