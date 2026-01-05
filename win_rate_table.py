from time import sleep
from heores_list import normalize_hero_name, win_replay_finder_list, mid_replay_finder_list, spirit_list
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
from hero_list import HERO_ID_MAP, ID_HERO_MAP

from counter_table import headers, cookie_string
import ctypes

# 防止系统休眠 + 屏幕关闭
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

from time import sleep
from heores_list import normalize_hero_name, win_replay_finder_list, mid_replay_finder_list, spirit_list
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
from hero_list import HERO_ID_MAP
import csv
from heores_list import heroes_list

from counter_table import headers, cookie_string
import ctypes

# 防止系统休眠 + 屏幕关闭
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002


headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiOTcxMTM5YTctNzQxZi00NDA2LTg1OGMtMzM0MTYwNmM3NGJkIiwiU3RlYW1JZCI6IjE3MzY5NDc5NyIsIkFQSVVzZXIiOiJ0cnVlIiwibmJmIjoxNzYwNjE2NTgyLCJleHAiOjE3OTIxNTI1ODIsImlhdCI6MTc2MDYxNjU4MiwiaXNzIjoiaHR0cHM6Ly9hcGkuc3RyYXR6LmNvbSJ9.F2V_4jcZgUiCkVaTcJdhXqCAc-XF36wiMY-De50s7Qc",
           'Content-Type': 'application/json',
           "User-Agent": "STRATZ_API",  # try replacing STRATZ_API with a browser UA,
           "Accept": "*",
           }
transport = RequestsHTTPTransport(
    url="https://api.stratz.com/graphql",
    headers=headers,
    verify=True,
    retries=3,
)
client = Client(transport=transport, fetch_schema_from_transport=False)

def deep_get(d, path, default=None):
    for key in path:
        if isinstance(d, dict):
            d = d.get(key)
        elif isinstance(d, list) and isinstance(key, int):
            if len(d) > key:
                d = d[key]
            else:
                return default
        else:
            return default
    return d


match_up_query = gql("""
    query ($heroId: Short!, $take:Int! ) {
        heroStats {
            matchUp(heroId: $heroId, take:$take){
                vs {
                    heroId2
                    synergy
            }      
            }         
        }
    }
    """)

def get_match_up(hero,):
    """Query guide matches for a specific hero vs opponent."""
    guide_result = client.execute(
        match_up_query,
        variable_values={
            "heroId": HERO_ID_MAP[hero],
            'take': 150
        }
    )
    sleep(1)
    return deep_get(guide_result, ['heroStats', 'matchUp', 0, 'vs'])


def run():
    with open('win_rate_table.csv', 'w', newline='') as win_rate_table:
        disadvantage_writer = csv.writer(win_rate_table, delimiter=',')
        disadvantage_writer.writerow(['', ] + heroes_list)
        for hero in heroes_list:
            results = get_match_up(hero)
            winrate_res = [hero] + [0] * len(heroes_list)
            for res in results:
                index = heroes_list.index(ID_HERO_MAP[res['heroId2']]) + 1
                winrate_res[index] = res['synergy']

            disadvantage_writer.writerow(winrate_res)
            print('finish ' + hero)


if __name__=='__main__':
    run()
                