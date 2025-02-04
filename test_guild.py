from bs4 import BeautifulSoup
from pprint import pprint

with open("test_guild.html", 'r', encoding='utf-8') as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    rows = soup.find_all("div", {"class": "content-inner"})[0].find_all("div", {"class": "r-stats-grid"})
    for row in rows:
        if row.find_all("i", {"class": "fa-lane-midlane"}):
            print(row.find_all("div", {"class": "image-container-skill"})[4].findChild('img')['alt'])
            time = row.find_all('time')[0]['datetime']
            pass
