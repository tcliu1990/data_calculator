import csv
from bs4 import BeautifulSoup
from decimal import Decimal
import os

from heores_list import heroes_list  # keep your existing list


HTML_FOLDER = "html_results"  # folder where your downloaded html files are


def hero_to_filename(hero_name):
    return hero_name.lower().replace(' ', '-') + ".html"


def parse_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')


def counter_table():
    with open('disadvantage.csv', 'w', newline='', encoding='utf-8') as disadvantage_file:
        disadvantage_writer = csv.writer(disadvantage_file, delimiter=' ')
        disadvantage_writer.writerow([''] + heroes_list)

        for hero in heroes_list:
            filename = hero_to_filename(hero)
            filepath = os.path.join(HTML_FOLDER, filename)

            if not os.path.exists(filepath):
                print(f"missing file: {filename}")
                continue

            soup = parse_html_file(filepath)
            tables = soup.find_all('table')

            if len(tables) < 3:
                print(f"table not found for {hero}")
                continue

            rows = tables[2].find_all('tr')

            advantage_res = [hero] + [0] * len(heroes_list)

            for row in rows[1:]:
                cols = row.find_all('td')
                if len(cols) < 4:
                    continue

                name = cols[0].get('data-value', '').lower()

                if name not in heroes_list:
                    continue

                index = heroes_list.index(name) + 1

                try:
                    advantage = Decimal(cols[2]['data-value']).quantize(Decimal('.01'))
                    advantage_res[index] = str(advantage)
                except:
                    continue

            disadvantage_writer.writerow(advantage_res)
            print('finish ' + hero)


if __name__ == '__main__':
    counter_table()