from bs4 import BeautifulSoup
from pprint import pprint

with open("test.html", 'r', encoding='utf-8') as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    table = soup.find_all('table')[3]
    rows = table.find_all('tr')
    print(rows[-1].find_all('td'))
    for i, x in enumerate(rows[-1].find_all('td')):
        try:
            print(x['data-value'])
        except KeyError:
            print(i)