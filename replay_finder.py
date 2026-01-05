import requests
from time import sleep
from heores_list import normalize_hero_name, win_replay_finder_list, mid_replay_finder_list, spirit_list
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
from hero_list import HERO_ID_MAP

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

guide_query = gql("""
query($heroId: Short!, $againstHeroId: Short!, $positionId: MatchPlayerPositionType!) {
  heroStats {
    guide(heroId: $heroId, againstHeroId: $againstHeroId, positionId: $positionId) {
      heroId
      guides {
        match {
          id
          startDateTime
          players {
            position
            hero { id }
          }
        }
      }
    }
  }
}
""")


match_detail_query = gql("""
query Match($matchId: Long!) {
    match(id: $matchId) {
        midLaneOutcome
        startDateTime
        players {
            isRadiant
            hero {
                id
            }
            lane
        }
    }
}
""")

match_ups = {
    'bristleback': ['pudge'],
    'batrider': ['outworld destroyer', 'death prophet', 'leshrac', "shadow fiend", 'sniper', 'viper', "monkey king"],
    'dazzle': ['batrider', 'outworld destroyer', 'death prophet', 'huskar', 'leshrac', "shadow fiend", 'sniper', 'viper'],
    # 'dawnbreaker': ['batrider', 'outworld destroyer', 'death prophet', 'huskar', 'leshrac', "shadow fiend", 'sniper', 'viper', 'magnus', 'earthshaker'],
    'enchantress': ['huskar', "shadow fiend", 'sniper', ],
    # 'marci': ['batrider', 'outworld destroyer', 'death prophet', 'huskar', 'leshrac', "shadow fiend", 'sniper', 'viper', 'magnus', 'earthshaker', "monkey king"],
    'leshrac': ['batrider', 'outworld destroyer', 'death prophet', 'huskar', 'dazzle', "shadow fiend", 'sniper', 'viper'],
    'marci': ['sniper'],
    'death prophet': ['batrider', 'outworld destroyer', 'huskar', 'leshrac', "shadow fiend", 'sniper', 'viper'],
    # "primal beast": ['batrider', 'outworld destroyer', 'death prophet', 'huskar', 'leshrac', "shadow fiend", 'sniper', 'viper'],
    "primal beast": ['sniper', ],
    "lina": ['batrider', "broodmother", 'outworld destroyer', 'death prophet', 'huskar', 'leshrac', 'necrophos', "shadow fiend", 'sniper', 'viper', "queen of pain",],
    "skywrath mage": ['batrider', "broodmother", 'outworld destroyer', 'death prophet', 'huskar', 'leshrac', 'necrophos', "shadow fiend", 'sniper', 'viper', "queen of pain",],
    "sniper": ['outworld destroyer', 'death prophet', 'huskar', 'leshrac', 'viper', "shadow fiend", "skywrath mage", "dragon knight" ],
    "broodmother": ['batrider', 'outworld destroyer', 'death prophet', 'huskar', 'razor', "shadow fiend", 'sniper', 'viper', "monkey king"],
    # "broodmother": ['sniper', 'viper', ],
    "puck": ["skywrath mage", "ember spirit", "void spirit", "pangolier", 'outworld destroyer'],
    # "viper": ["outworld destroyer"],
    "huskar": ["monkey king"],
    "slardar": ["monkey king"],
    "visage": ["sniper"],
}



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


def get_exist_replays():
    conn = sqlite3.connect('replay.db')
    cursor = conn.cursor()
    cursor.execute('select replay_id from replay where date > ?;', (datetime.now() - timedelta(days=15), ))
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return [value[0] for value in values]


def get_guide_matches(hero, opponent):
    """Query guide matches for a specific hero vs opponent."""
    guide_result = client.execute(
        guide_query,
        variable_values={
            "heroId": HERO_ID_MAP[hero],
            "againstHeroId": HERO_ID_MAP[opponent],
            "positionId": "POSITION_2",
        }
    )
    sleep(1)
    return deep_get(guide_result, ['heroStats', 'guide', 0, 'guides'])

def fetch_all_guides( hero, opponent):
    all_matches = []
    skip = 0
    take = 50

    while True:
        guide_result = client.execute(
            gql("""
            query($heroId: Short!, $againstHeroId: Short!, $positionId: MatchPlayerPositionType!, $skip: Int!, $take: Int!) {
              heroStats {
                guide(heroId: $heroId, againstHeroId: $againstHeroId, positionId: $positionId) {
                  heroId
                  guides(skip: $skip, take: $take) {
                    createdDateTime
                    match {
                      id
                      startDateTime
                      players {
                        position
                        hero { id }
                      }
                    }
                  }
                }
              }
            }
            """),
            variable_values={
                "heroId": HERO_ID_MAP[hero],
                "againstHeroId": HERO_ID_MAP[opponent],
                "positionId": "POSITION_2",
                "skip": skip,
                "take": take,
            },
        )

        guides = deep_get(guide_result, ['heroStats', 'guide', 0, 'guides'])
        sleep(1)
        if not guides:
            break
        all_matches.extend(guides)
        if len(guides) < take:
            break
        
        skip += take
       

    return all_matches



def get_match_detail(match_id):
    """Query detailed match info."""
    match_detail = client.execute(
        match_detail_query,
        variable_values={"matchId": match_id}
    )
    sleep(1)
    return deep_get(match_detail, ['match',])


def extract_mid_lane_match(matches, opponent_id, start_date=None):
    res = []
    """Find the match where the opponent played mid lane."""
    for match in matches:
        if start_date:
            if datetime.fromtimestamp(match['match']['startDateTime']) <= datetime.strptime(start_date , '%Y-%m-%d %H:%M:%S.%f'):
                continue
        players = deep_get(match, ['match', 'players'])
        for player in players:
            if player['hero']['id'] == opponent_id and player['position'] == 'POSITION_2':
                res.append(deep_get(match, ['match', 'id']))
                break
    return res


def hero_won_mid_lane(match_detail, hero_id):
    """Check if the given hero won the mid lane in this match."""
    for player in match_detail['players']:
        if player['hero']['id'] == hero_id:
            isRadiant = player['isRadiant']
            break
    else:
        return False  # Hero not found

    outcome = match_detail['midLaneOutcome']
    return (
        (outcome == 'RADIANT_VICTORY' and isRadiant) or
        (outcome == 'DIRE_VICTORY' and not isRadiant)
    )


def insert_replay(cursor, conn, match_id, hero, opponent, start):
    """Insert replay record into database."""
    try:
        cursor.execute(
            "INSERT INTO replay (replay_id, hero, opp_hero, date, watched) VALUES (?, ?, ?, ?, 0);",
            (match_id, hero, opponent, start)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass


def find_replay_mid_lane(exist_list):
    conn = sqlite3.connect('replay.db')
    cursor = conn.cursor()

    for hero in match_ups:
        for opponent in match_ups[hero]:
            matches = fetch_all_guides(hero, opponent)
            if not matches:
                continue
            target_matches = extract_mid_lane_match(matches, HERO_ID_MAP[opponent])
            for target_match in target_matches:
                if not target_match or int(target_match) in exist_list:
                    continue

                match_detail = get_match_detail(target_match)
                if hero_won_mid_lane(match_detail, HERO_ID_MAP[hero]):
                    start = datetime.fromtimestamp(match_detail['startDateTime'])
                    print(
                        f"insert into replay (replay_id, hero, opp_hero, date, watched) values ({target_match}, {hero}, {opponent}, {start}, 0)"
                    )
                    insert_replay(cursor, conn, target_match, hero, opponent, start)

    cursor.close()
    conn.close()
    print('finish find_replay_mid_lane')


def get_guide_matches_pair(hero, opponent):
    """Return both hero→opponent and opponent→hero guide match lists."""
    hero_vs_opponent = fetch_all_guides(hero, opponent)
    opponent_vs_hero = fetch_all_guides(opponent, hero)
    return hero_vs_opponent, opponent_vs_hero


def calculate_mid_lane_stats(start_date):
    results = {}
    for hero in match_ups:
         for opponent in match_ups[hero]:
            """Calculate win/loss/tie ratios for both hero→opponent and opponent→hero."""
            print(f'checking pair {hero}, {opponent}')
            hero_guides, opponent_guides = get_guide_matches_pair(hero, opponent)
            pair_result = {"win": 0, "lose": 0, "tie": 0}

            # Combine both directions for full coverage
            for target_hero, guides in [(opponent, hero_guides), (hero, opponent_guides)]:
                if not guides:
                    continue
                target_matches = extract_mid_lane_match(guides,  HERO_ID_MAP[target_hero], start_date)
                for match_id in target_matches:
                    match_detail = get_match_detail(match_id)
                    outcome = match_detail['midLaneOutcome']
                    hero_id = HERO_ID_MAP[hero]

                    if hero_won_mid_lane(match_detail, hero_id):
                        pair_result["win"] += 1
                    elif outcome in ['RADIANT_VICTORY', 'DIRE_VICTORY']:
                        pair_result["lose"] += 1
                    else:
                        pair_result["tie"] += 1

            total = sum(pair_result.values())
            if total > 0:
                results[(hero, opponent)] = pair_result

    return results

def save_mid_lane_stats(result_dict):
    conn = sqlite3.connect('replay.db')
    cursor = conn.cursor()
    today = datetime.now().today()
    

    for (hero, opponent), stats in result_dict.items():
        if stats['win'] or  stats['lose'] or stats['tie']:
            cursor.execute("""
                INSERT INTO mid_lane_stats  (hero, opponent, date, win, lose, tie)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (hero, opponent, today, stats['win'], stats['lose'], stats['tie']))
    conn.commit()
    conn.close()

def get_stats_start_date():
    conn = sqlite3.connect('replay.db')
    cursor = conn.cursor()
    cursor.execute('select date from mid_lane_stats order by date DESC limit 1;')
    value = cursor.fetchone()
    cursor.close()
    conn.close()
    if value:
        return value[0]


if __name__ == "__main__":
    try:
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
        )
        exist = get_exist_replays()
        find_replay_mid_lane(exist)

        start_date = get_stats_start_date()
        # start_date = None
        res = calculate_mid_lane_stats(start_date)
        print(res)
        save_mid_lane_stats(res)
        print('finish')
    finally:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)


