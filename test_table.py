import csv
from heores_list import heroes_list, mid_list


def test_table(hero1, hero2):
    with open('disadvantage.csv', 'r', encoding='utf-8') as disadvantage_file:
        reader = csv.reader(disadvantage_file, delimiter=' ')
        data = list(reader)
        index = heroes_list.index(hero1) + 1
        index2 = heroes_list.index(hero2) + 1
        return data[index][index2]


print(test_table('batrider', 'silencer'))

def disadvantage_calculate2(opp_heroes, my_heroes):
    with open('disadvantage.csv', 'r', encoding='utf-8') as disadvantage_file:
        reader = csv.reader(disadvantage_file, delimiter=' ')
        data = list(reader)
        my_res = {}
        opp_res = {}

        for row in data[1:]:
            if row[0] in mid_list:
                disadvantage_list = []
                my_res[row[0]] = 0
                opp_res[row[0]] = 0
                for hero in opp_heroes:
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
