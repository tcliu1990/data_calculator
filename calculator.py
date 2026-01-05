import csv
from heores_list import heroes_list, mid_list, heroes_dict
from pprint import pprint


def disadvantage_calculate(opp_heroes, my_heroes):
    with open('disadvantage.csv', 'r', encoding='utf-8') as disadvantage_file:
        reader = csv.reader(disadvantage_file, delimiter=' ')
        next(reader, None)
        my_res = {}
        opp_res = {}

        for row in reader:
            if row[0] in mid_list:
                disadvantage_list = []
                my_res[row[0]] = 0
                opp_res[row[0]] = 0
                for hero in opp_heroes:
                    index = heroes_list.index(hero) + 1
                    disadvantage = float(row[index])
                    disadvantage_list.append({hero: disadvantage})
                    my_res[row[0]] += disadvantage
                my_res[row[0]] = [my_res[row[0]], disadvantage_list]
                for hero in my_heroes:
                    index = heroes_list.index(hero) + 1
                    opp_res[row[0]] += float(row[index])
        without_mid = {k: v for k, v in sorted(my_res.items(), key=lambda item: item[1][0]) if v[0] < 0}

        opp_mid = {k: v for k, v in sorted(opp_res.items(), key=lambda item: item[1]) if k in mid_list and v < 0 }
    return without_mid, opp_mid,


def disadvantage_calculate2(opp_heroes, my_heroes):
    with open('disadvantage.csv', 'r', encoding='utf-8') as disadvantage_file:
        reader = csv.reader(disadvantage_file, delimiter=' ')
        data = list(reader)
        my_res = {}
        opp_res = {}

        for row in data[1:]:
            disadvantage_list = []
            my_res[row[0]] = 0
            opp_res[row[0]] = 0
            for hero in opp_heroes:
                hero = heroes_dict[hero]
                index = heroes_list.index(hero) + 1
                index2 = heroes_list.index(row[0]) + 1

                disadvantage = float(data[index][index2])
                disadvantage_list.append({hero: disadvantage})
                my_res[row[0]] += disadvantage
            my_res[row[0]] = [my_res[row[0]], disadvantage_list]
            for hero in my_heroes:
                index = heroes_list.index(hero) + 1
                opp_res[row[0]] += float(row[index])
        without_mid = {k: v for k, v in sorted(my_res.items(), reverse=True, key=lambda item: item[1][0]) if v[0] > 0}

        opp_mid = {k: v for k, v in sorted(opp_res.items(), key=lambda item: item[1]) if k in mid_list and v < 0 }
    return without_mid, opp_mid,


def disadvantage_calculate3(opp_heroes):
    with open('win_rate_table.csv', 'r', encoding='utf-8') as disadvantage_file:
        reader = csv.reader(disadvantage_file, delimiter=',')
        next(reader, None)
        my_res = {}
        opp_res = {}

        for row in reader:
            disadvantage_list = []
            my_res[row[0]] = 0
            opp_res[row[0]] = 0
            for hero in opp_heroes:
                if not hero:
                    continue
                hero = heroes_dict[hero]
                index = heroes_list.index(hero) + 1
                disadvantage = float(row[index])
                disadvantage_list.append({hero: disadvantage})
                my_res[row[0]] += disadvantage
            my_res[row[0]] = [my_res[row[0]], disadvantage_list]
        without_mid = {k: v for k, v in sorted(my_res.items(), key=lambda item: item[1][0], reverse=True) if v[0] > 0}

    return without_mid,

a = ["幽鬼", "军团", "火枪", "骨法", '']

import json
# with open('result.json', 'w', encoding='utf-8') as f:
#     json.dump(disadvantage_calculate2(a, ['ursa', 'slardar', 'jakiro', 'shadow shaman'])[0], f, ensure_ascii=False, indent=2)

with open('result2.json', 'w', encoding='utf-8') as f:
    json.dump(disadvantage_calculate3(a, ), f, ensure_ascii=False, indent=2)

# print(disadvantage_calculate(a, ['ursa', 'slardar', 'earthshaker', 'shadow shaman'])[0])
# print(disadvantage_calculate2(a, ['mars', 'slardar', 'earthshaker', 'shadow shaman'])[0])
# print(disadvantage_calculate3(a, ['mars', 'slardar', 'earthshaker', 'shadow shaman'])[0])
