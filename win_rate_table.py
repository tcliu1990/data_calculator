import csv
import requests
from heores_list import normalize_hero_name, heroes_list
from bs4 import BeautifulSoup
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
cookie_string = {
    'cookie': '_tz=America/Toronto; _ga=GA1.2.1325744723.1637551614; __qca=P0-419533972-1637551614996; _hjSessionUser_2490228=eyJpZCI6ImJjYTlhNTg0LWUyZWItNTU0ZC1iZmZjLTA2MzJlMzc0MmMyMSIsImNyZWF0ZWQiOjE2Mzc1NTE2MTQ4MjgsImV4aXN0aW5nIjp0cnVlfQ==; __gads=ID=d23bb385aad022c0:T=1637551619:S=ALNI_MZe6MnHgAdv2IBZ7VXb5neg8ZhUxw; _ats=1639678200; __aaxsc=1; _gid=GA1.2.43480603.1641147794; _hjSession_2490228=eyJpZCI6ImEyMTBkODY3LTJmNTUtNDhkYi04ODgwLTM4NGE2MDIzZWZiYiIsImNyZWF0ZWQiOjE2NDE0Nzk3Mzk1MDl9; _hjIncludedInSessionSample=0; _hjAbsoluteSessionInProgress=0; _hi=1641479767183; aasd=4|1641479739861; FCNEC=[["AKsRol9RR6bm4MZMrd2pKEiSwEBMaDB3DyFENMemdC0Im8oluLWFkUseGKQ6VJQPzDccGBMqyx42M7aWcYw9g5P9mH0MXpg9Mot3vigysvt36mPeiiRN2gPIQtrVWD7Zjz1TQWyd2768v-CkUqz3jH9kAsWoM6YtNQ=="],null,[]]'}

with open('win_rate_table.csv', 'w', newline='') as win_rate_table:
    disadvantage_writer = csv.writer(win_rate_table, delimiter=' ')
    disadvantage_writer.writerow(['', ] + heroes_list)
    for hero in heroes_list:
        normalize_name = normalize_hero_name(hero)
        r = requests.get('https://www.dotabuff.com/heroes/{}/counters'.format(normalize_name), cookies=cookie_string,
                         headers=headers)
        sleep(2)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            rows = soup.find_all('table')[3].find_all('tr')
            winrate_res = [hero] + [0] * len(heroes_list)
            for row in rows[1:]:
                name = row.find_all('td')[0]['data-value'].lower()
                index = heroes_list.index(name) + 1
                winrate_res[index] = row.find_all('td')[3]['data-value']
            # winrate_writer.writerow(winrate_res)
            disadvantage_writer.writerow(winrate_res)
            print('finish ' + hero)
        else:
            print('unfinish ' + hero)
