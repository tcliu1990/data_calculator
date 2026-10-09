import csv
from heores_list import heroes_list, mid_list, heroes_dict
from pprint import pprint


def normalize_input_hero(hero):
    return heroes_dict.get(hero, hero)


def load_matchup_table(path, delimiter):
    with open(path, 'r', encoding='utf-8') as matchup_file:
        reader = csv.reader(matchup_file, delimiter=delimiter)
        header = next(reader)
        rows = {row[0]: row for row in reader if row}
    return header, rows


def get_matchup_value(rows_by_hero, header, opponent, candidate):
    if opponent in rows_by_hero:
        return float(rows_by_hero[opponent][header.index(candidate)])

    if opponent in header and candidate in rows_by_hero:
        return -float(rows_by_hero[candidate][header.index(opponent)])

    return None


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
    header, rows_by_hero = load_matchup_table('disadvantage.csv', ' ')
    my_res = {}

    for candidate in header:
        if not candidate:
            continue

        disadvantage_list = []
        my_res[candidate] = 0

        for hero in opp_heroes:
            if not hero:
                continue

            opp_hero = normalize_input_hero(hero)
            if candidate not in header:
                continue

            # Dotabuff's table is directional. For "candidate counters opponent",
            # read the opponent row at the candidate column.
            disadvantage = get_matchup_value(rows_by_hero, header, opp_hero, candidate)
            if disadvantage is None:
                continue

            disadvantage_list.append({opp_hero: disadvantage})
            my_res[candidate] += disadvantage

        my_res[candidate] = [my_res[candidate], disadvantage_list]

    without_mid = {k: v for k, v in sorted(my_res.items(), key=lambda item: item[1][0], reverse=True) if v[0] > 0}

    return without_mid,

a = ["蓝胖", "术士", "血魔", "潮汐", '']

import json
# with open('result.json', 'w', encoding='utf-8') as f:
#     json.dump(disadvantage_calculate2(a, ['ursa', 'slardar', 'jakiro', 'shadow shaman'])[0], f, ensure_ascii=False, indent=2)

with open('result2.json', 'w', encoding='utf-8') as f:
    json.dump(disadvantage_calculate3(a, ), f, ensure_ascii=False, indent=2)

# print(disadvantage_calculate(a, ['ursa', 'slardar', 'earthshaker', 'shadow shaman'])[0])
# print(disadvantage_calculate2(a, ['mars', 'slardar', 'earthshaker', 'shadow shaman'])[0])
# print(disadvantage_calculate3(a, ['mars', 'slardar', 'earthshaker', 'shadow shaman'])[0])
