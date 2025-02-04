from bs4 import BeautifulSoup
from pprint import pprint

with open("test_match.html", 'r', encoding='utf-8') as fp:
    res = []
    soup = BeautifulSoup(fp, 'html.parser')
    for tbody in soup.find_all('div', {'class': 'team-results'})[0].find_all('tbody'):
        for row in tbody.find_all('tr', {'class': 'col-hints'}):
            print(row.find_all('span', {'class': 'player-lane-text'})[0].find_all('acronym'))
            # if row.find_all('img', {'class': 'image-hero'})[0].parent['href'].split('/')[2] == 'batrider':

            pass