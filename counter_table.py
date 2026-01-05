import csv
import requests
from heores_list import normalize_hero_name, heroes_list
from bs4 import BeautifulSoup
from time import sleep
from decimal import Decimal
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
cookie_string = {
    'cookie': 'tz=America%2FToronto; _ga=GA1.2.789783132.1731727206; _cc_id=6b2c880241e93960de67d3de7695794a; __gads=ID=6063621df9ab9d50:T=1731727212:RT=1731730433:S=ALNI_Mavl_EeXrtU372a4LzKmcqv9u_HEA; __gpi=UID=00000f963474e753:T=1731727212:RT=1731730433:S=ALNI_MYZ5HcNkoQDb_BkLwJdwrLZ1ms8hA; usprivacy=1---; _ga_PT3JLZNXYV=GS2.2.s1751558286$o2$g0$t1751558286$j60$l0$h0; _hi=1751850326349'
}


def counter_table():
    with open('disadvantage.csv', 'w', newline='') as disadvantage_file:
        disadvantage_writer = csv.writer(disadvantage_file, delimiter=' ')
        disadvantage_writer.writerow(['', ] + heroes_list)
        for hero in heroes_list:
            normalize_name = normalize_hero_name(hero)
            r = requests.get('https://www.dotabuff.com/heroes/{}/counters?date=patch_7.39'.format(normalize_name), cookies=cookie_string,
                             headers=headers)
            sleep(2)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                rows = soup.find_all('table')[2].find_all('tr')
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