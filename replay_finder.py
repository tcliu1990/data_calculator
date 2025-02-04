import requests
from time import sleep
from heores_list import normalize_hero_name, win_replay_finder_list, mid_replay_finder_list, spirit_list
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta

from counter_table import headers, cookie_string


def get_exist_replays():
    conn = sqlite3.connect('replay.db')
    cursor = conn.cursor()
    cursor.execute('select replay_id from replay where date > ?;', (datetime.now() - timedelta(days=4), ))
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return [value[0] for value in values]


def find_replay_mid_lane(exist_list):
    conn = sqlite3.connect('replay.db')
    cursor = conn.cursor()
    for hero in mid_replay_finder_list:
        normalize_name = normalize_hero_name(hero)
        for i in range(1, 5):
            r = requests.get('https://www.dotabuff.com/heroes/{}/guides?page={}'.format(normalize_name, i),
                             cookies=cookie_string,
                             headers=headers)
            sleep(1)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                rows = soup.find_all("div", {"class": "content-inner"})[0].find_all("div", {"class": "r-stats-grid"})
                for row in rows:
                    if row.find_all("i", {"class": "fa-lane-midlane"}):
                        match_id = row.find_all("a", string="View Match")[0]['href'].split('/')[2].split('?')[0]
                        if int(match_id) not in exist_list:
                            time = row.find_all('time')[0]['datetime']
                            detail_r = requests.get(
                                'https://www.dotabuff.com/matches/{}/'.format(match_id),
                                cookies=cookie_string,
                                headers=headers)
                            if detail_r.status_code == 200:
                                detail_soup = BeautifulSoup(detail_r.text, 'html.parser')
                                opp_hero = None
                                for tbody in detail_soup.find_all('div', {'class': 'team-results'})[0].find_all('tbody'):
                                    for detail_row in tbody.find_all('tr', {'class': 'col-hints'}):
                                        if detail_row.find_all('span', {'class': 'player-lane-text'})[0].find_all('acronym')[0].getText() == 'Middle':
                                            hero_name = detail_row.find_all('img', {'class': 'image-hero'})[0].parent['href'].split('/')[2]
                                            if hero_name != normalize_name:
                                                opp_hero = hero_name

                                print(
                                    r"insert into replay (replay_id, hero, opp_hero, date, watched) values ({}, {}, {}, {}, 0)".format(
                                        match_id, normalize_name, opp_hero, time,
                                    ))
                                try:
                                    cursor.execute(r"insert into replay (replay_id, hero, opp_hero, date, watched) values (?, ?, ?, ?, 0);",
                                                   (
                                                       match_id, normalize_name, opp_hero, time
                                                   ))
                                    conn.commit()
                                except sqlite3.IntegrityError:
                                    continue

    cursor.close()
    conn.close()
    print('finish find_replay_mid_lane')


def find_replay_win_mid_lane(exist_list):
    conn = sqlite3.connect('replay.db')
    cursor = conn.cursor()
    for hero in win_replay_finder_list:
        normalize_name = normalize_hero_name(hero)
        for i in range(1, 5):
            r = requests.get('https://www.dotabuff.com/heroes/{}/guides?page={}'.format(normalize_name, i),
                             cookies=cookie_string,
                             headers=headers)
            sleep(1)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                rows = soup.find_all("div", {"class": "content-inner"})[0].find_all("div", {"class": "r-stats-grid"})
                for row in rows:
                    if row.find_all("i", {"class": "fa-lane-midlane"}):
                        match_id = row.find_all("a", string="View Match")[0]['href'].split('/')[2].split('?')[0]
                        if int(match_id) not in exist_list:
                            detail_r = requests.get(
                                'https://www.dotabuff.com/matches/{}/'.format(match_id),
                                cookies=cookie_string,
                                headers=headers)
                            if detail_r.status_code == 200:
                                time = row.find_all('time')[0]['datetime']
                                detail_soup = BeautifulSoup(detail_r.text, 'html.parser')
                                opp_hero = None
                                flag = False
                                for tbody in detail_soup.find_all('div', {'class': 'team-results'})[0].find_all('tbody'):
                                    for detail_row in tbody.find_all('tr', {'class': 'col-hints'}):
                                        if detail_row.find_all('span', {'class': 'player-lane-text'})[0].find_all('acronym')[0].getText() == 'Middle':
                                            hero_name = detail_row.find_all('img', {'class': 'image-hero'})[0].parent['href'].split('/')[2]
                                            if hero_name == normalize_name:
                                                if detail_row.find_all('acronym', {'class': 'lane-outcome'})[0].getText() == 'won':
                                                    flag = True
                                            else:
                                                opp_hero = hero_name
                                if flag:
                                   print( r"insert into replay (replay_id, hero, opp_hero, date, watched) values ({}, {}, {}, {}, 0)".format(
                                        match_id, normalize_name, opp_hero, time
                                    ))
                                   try:
                                       cursor.execute(r"insert into replay (replay_id, hero, opp_hero, date, watched) values (?, ?, ?, ?, 0);", (
                                            match_id, normalize_name, opp_hero, time
                                        ))
                                       conn.commit()
                                   except sqlite3.IntegrityError:
                                       continue
                            else:
                                print('error on detail page')
                                return

            else:
                print('error on guide page')
                return
    cursor.close()
    conn.close()
    print('finish find_replay_win_mid_lane')


def find_replay_with_w_zeus(exist_list):
    conn = sqlite3.connect('replay.db')
    cursor = conn.cursor()
    for i in range(1, 5):
        r = requests.get('https://www.dotabuff.com/heroes/huskar/guides?page={}'.format(i),
                         cookies=cookie_string,
                         headers=headers)
        sleep(1)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            rows = soup.find_all("div", {"class": "content-inner"})[0].find_all("div", {"class": "r-stats-grid"})
            for row in rows:
                if row.find_all("i", {"class": "fa-lane-midlane"}) and \
                        row.find_all("div", {"class": "image-container-skill"})[4].findChild('img')['alt'] == 'Lightning Bolt':

                    match_id = row.find_all("a", string="View Match")[0]['href'].split('/')[2].split('?')[0]
                    if int(match_id) not in exist_list:
                        time = row.find_all('time')[0]['datetime']
                        detail_r = requests.get(
                            'https://www.dotabuff.com/matches/{}/'.format(match_id),
                            cookies=cookie_string,
                            headers=headers)
                        if detail_r.status_code == 200:
                            detail_soup = BeautifulSoup(detail_r.text, 'html.parser')
                            opp_hero = None
                            for tbody in detail_soup.find_all('div', {'class': 'team-results'})[0].find_all('tbody'):
                                for detail_row in tbody.find_all('tr', {'class': 'col-hints'}):
                                    if \
                                    detail_row.find_all('span', {'class': 'player-lane-text'})[0].find_all('acronym')[
                                        0].getText() == 'Middle':
                                        hero_name = \
                                        detail_row.find_all('img', {'class': 'image-hero'})[0].parent['href'].split(
                                            '/')[2]
                                        if hero_name != 'zeus':
                                            opp_hero = hero_name
                            print(
                                r"insert into replay (replay_id, hero, opp_hero, date, watched) values ({}, {}, {}, {}, 0)".format(
                                    match_id, 'zeus', opp_hero, time,
                                ))
                            cursor.execute(
                                r"insert into replay (replay_id, hero, opp_hero, date, watched) values (?, ?, ?, ?, 0);",
                                (
                                    match_id, 'zeus', opp_hero, time
                                ))
                            conn.commit()
                        cursor.close()
                        conn.close()
                        print('finish')


if __name__ == "__main__":
    exist = get_exist_replays()
    # print(exist)
    find_replay_mid_lane(exist)
    # find_replay_win_mid_lane(exist)
    # find_replay_with_w_zeus(exist)

