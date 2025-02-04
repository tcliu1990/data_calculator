import csv
import requests
from heores_list import normalize_hero_name, heroes_list
from bs4 import BeautifulSoup
from time import sleep
from decimal import Decimal
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
cookie_string = {
    'cookie': '_hjSessionUser_2490228=eyJpZCI6ImVlYzgxMThjLWY0OTYtNWRlOC1iZTZmLWE3MDg1YTYyNjAzNCIsImNyZWF0ZWQiOjE3MDAwMjQ0OTE5MDYsImV4aXN0aW5nIjp0cnVlfQ==; usprivacy=1Y--; _tz=America%2FToronto; _hi=1727796738009'
}


def counter_table():
    with open('disadvantage.csv', 'w', newline='') as disadvantage_file:
        disadvantage_writer = csv.writer(disadvantage_file, delimiter=' ')
        disadvantage_writer.writerow(['', ] + heroes_list)
        for hero in heroes_list:
            normalize_name = normalize_hero_name(hero)
            r = requests.get('https://www.dotabuff.com/heroes/{}/counters?date=month'.format(normalize_name), cookies=cookie_string,
                             headers=headers)
            sleep(2)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                rows = soup.find_all('table')[3].find_all('tr')
                winrate_res = advantage_res = [hero] + [0] * len(heroes_list)
                for row in rows[1:]:
                    name = row.find_all('td')[0]['data-value'].lower()
                    index = heroes_list.index(name) + 1
                    winrate_res[index] = str(Decimal(row.find_all('td')[3]['data-value']).quantize(Decimal('.01')))
                    advantage_res[index] = str(Decimal(row.find_all('td')[2]['data-value']).quantize(Decimal('.01')))
                # winrate_writer.writerow(winrate_res)
                disadvantage_writer.writerow(advantage_res)
                print('finish ' + hero)
            else:
                print('unfinish ' + hero)


if __name__ == '__main__':
    counter_table()