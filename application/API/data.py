from bson.objectid import ObjectId
import MetaTrader5 as mt5
import pandas as pd
import json

from . import TIME_CONST
from utils import utils
from utils import connections
from utils import date_and_time


def get_last_close_candle():
    connect = connections.to_mt()
    if not connect:
        return mt5.last_error()

    timestamp = date_and_time.formated("now", "timestamp") + TIME_CONST
    date_time = date_and_time.formated(timestamp, "datetime")

    data = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M5, date_time, 2)
    df = pd.DataFrame(data)
    df = df.assign(
        date_timestamp=df["time"].apply(
            lambda x: int(x)
        ),

        date_str=df["time"].apply(
            lambda x: str(date_and_time.formated(x, "%d/%m/%Y %H:%M:%S"))
        ),

        date_str_tickmill=df["time"].apply(
            lambda x: str(date_and_time.formated(x+3*60*60, "%d/%m/%Y %H:%M:%S"))
        )
    )
    df = df[["date_timestamp", "date_str", "date_str_tickmill", "open", "high", "low", "close"]]
    result = df.to_dict("records")[0]

    print('----------')
    print('check_duplicates')
    print(check_duplicates(result))
    print('----------')
    if not check_duplicates(result):
        return {}

    redis_data = []
    raw_redis_data = connections.to_redis().get('candle_avg')
    if not raw_redis_data:
        redis_data.append(result)
        _ = connections.to_redis().set('candle_avg', json.dumps(redis_data))
    else:
        redis_data = json.loads(raw_redis_data)
        redis_data.append(result)
        _ = connections.to_redis().set('candle_avg', json.dumps(redis_data))

    update_avg()
    _ = connections.to_mongo().data.close_candles.insert_one(result)
    print('----------')
    print('RESULT')
    print(result)
    print('----------')

    return df.to_dict("records")[0]


def update_avg():
    raw_avg = connections.to_redis().get('candle_avg')

    if raw_avg:
        avg = json.loads(raw_avg)

        df = pd.DataFrame(avg)
        df = df.sort_values(['date_timestamp'], ascending=False, ignore_index=True)
        df = df.head(20)

        const_avg_20 = utils.trunc(df['close'].mean(), 6)
        dict_avg = df.to_dict('records')

        _ = connections.to_redis().set('20_mov_avg', json.dumps(const_avg_20))
        _ = connections.to_redis().set('candle_avg', json.dumps(dict_avg))


def check_duplicates(data):
    actual_timestamp = data['date_timestamp']

    result_mongo = connections.to_mongo().data.close_candles.find_one({
        'date_timestamp': actual_timestamp
    })

    raw_result_redis = connections.to_redis().get('candle_avg')
    result_redis = json.loads(raw_result_redis) if raw_result_redis else ''

    if not result_mongo and not result_redis:
        return True

    for result in result_redis:
        if result['date_timestamp'] == actual_timestamp:
            return False

    if not result_mongo:
        return True
