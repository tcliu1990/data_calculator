from heores_list import normalize_hero_name, win_replay_finder_list, mid_replay_finder_list
import requests
from counter_table import headers, cookie_string

r1 = requests.get('https://www.dotabuff.com/matches/6636748519/', cookies=cookie_string, headers=headers)
print(r1.text)