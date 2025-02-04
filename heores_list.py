heroes_list = ['abaddon', 'alchemist', 'ancient apparition', 'anti-mage', 'arc warden', 'axe', 'bane', 'batrider',
               'beastmaster', 'bloodseeker', 'bounty hunter', 'brewmaster', 'bristleback', 'broodmother',
               'centaur warrunner', 'chaos knight', 'chen', 'clinkz', 'clockwerk', 'crystal maiden', 'dark seer',
               'dark willow', 'dawnbreaker', 'dazzle', 'death prophet', 'disruptor', 'doom', 'dragon knight',
               'drow ranger', 'earth spirit', 'earthshaker', 'elder titan', 'ember spirit', 'enchantress', 'enigma',
               'faceless void', 'grimstroke', 'gyrocopter', 'hoodwink', 'huskar', 'invoker', 'io', 'jakiro',
               'juggernaut', 'keeper of the light', 'kez','kunkka', 'legion commander', 'leshrac', 'lich', 'lifestealer',
               'lina', 'lion', 'lone druid', 'luna', 'lycan', 'magnus', 'marci', 'mars', 'medusa', 'muerta', 'meepo', 'mirana',
               'monkey king', 'morphling', 'naga siren', "nature's prophet", 'necrophos', 'night stalker',
               'nyx assassin', 'ogre magi', 'omniknight', 'oracle', 'outworld destroyer', 'pangolier',
               'phantom assassin', 'phantom lancer', 'phoenix', 'primal beast', 'puck', 'pudge', 'pugna', 'queen of pain', 'razor',
               'riki', 'ringmaster', 'rubick', 'sand king', 'shadow demon', 'shadow fiend', 'shadow shaman', 'silencer',
               'skywrath mage', 'slardar', 'slark', 'snapfire', 'sniper', 'spectre', 'spirit breaker', 'storm spirit',
               'sven', 'techies', 'templar assassin', 'terrorblade', 'tidehunter', 'timbersaw', 'tinker', 'tiny',
               'treant protector', 'troll warlord', 'tusk', 'underlord', 'undying', 'ursa', 'vengeful spirit',
               'venomancer', 'viper', 'visage', 'void spirit', 'warlock', 'weaver', 'windranger', 'winter wyvern',
               'witch doctor', 'wraith king', 'zeus']

mid_list = ['batrider', 'bloodseeker', 'bounty hunter', 'bristleback', 'broodmother', 'dawnbreaker', 'death prophet', 'dragon knight',
            'ember spirit', 'enchantress', 'huskar', 'invoker', 'kunkka', 'legion commander', 'leshrac', 'lina', "nature's prophet"
            'mars', 'pugna', 'necrophos', 'night stalker', 'outworld destroyer', 'pangolier', 'primal beast', 'pudge', 'puck', 'queen of pain', 'razor', 'riki',
            'shadow fiend', 'storm spirit',  'sniper', 'silencer', 'tiny', 'viper', 'visage', 'void spirit', 'windranger', 'tinker'
            'winter wyvern', 'zeus'
            ]

strong_lane_heor_list = ['batrider', 'bloodseeker', ]

# win_replay_finder_list = ['batrider', 'broodmother',  'huskar', 'leshrac', 'lina','primal beast',  'razor','shadow fiend', 'sniper', 'tinker', 'visage',  'zeus']
win_replay_finder_list = ['leshrac', 'puck', 'ember spirit', 'storm spirit', 'void spirit', 'pangolier']

mid_replay_finder_list = ['bristleback',  'dawnbreaker', 'enchantress', 'legion commander', 'mars', 'silencer',
                           'riki', 'winter wyvern', ]

spirit_list = ['puck', 'ember spirit', 'storm spirit', 'void spirit', 'pangolier']


def normalize_hero_name(name):
    return name.replace(' ', '-').replace("'", '').lower()
