heroes_list = [
    'abaddon', 'alchemist', 'ancient apparition', 'anti-mage', 'arc warden',
    'axe', 

    'bane', 'batrider', 'beastmaster', 'bloodseeker', 'bounty hunter',
    'brewmaster', 'bristleback', 'broodmother',

    'centaur warrunner', 'chaos knight', 'chen', 'clinkz', 'clockwerk',
    'crystal maiden',

    'dark seer', 'dark willow', 'dawnbreaker', 'dazzle', 'death prophet',
    'disruptor', 'doom', 'dragon knight', 'drow ranger',

    'earth spirit', 'earthshaker', 'elder titan', 'ember spirit', 'enchantress',
    'enigma',

    'faceless void',

    'grimstroke', 'gyrocopter',

    'hoodwink', 'huskar',

    'invoker', 'io',

    'jakiro', 'juggernaut',

    'keeper of the light', 'kez', 'kunkka',

    'largo', 'legion commander', 'leshrac', 'lich', 'lifestealer', 'lina',
    'lion', 'lone druid', 'luna', 'lycan',

    'magnus', 'marci', 'mars', 'medusa', 'meepo',
    'mirana', 'monkey king', 'morphling', 'muerta',

    'naga siren', "nature's prophet", 'necrophos', 'night stalker', 'nyx assassin',

    'ogre magi', 'omniknight', 'oracle', 'outworld destroyer',

    'pangolier', 'phantom assassin', 'phantom lancer', 'phoenix', 'primal beast',
    'puck', 'pudge', 'pugna',

    'queen of pain',

    'razor', 'riki', 'ringmaster', 'rubick',

    'sand king', 'shadow demon', 'shadow fiend', 'shadow shaman', 'silencer',
    'skywrath mage', 'slardar', 'slark', 'snapfire', 'sniper',
    'spectre', 'spirit breaker', 'storm spirit', 'sven',

    'techies', 'templar assassin', 'terrorblade', 'tidehunter', 'timbersaw',
    'tinker', 'tiny', 'treant protector', 'troll warlord', 'tusk',

    'underlord', 'undying', 'ursa',

    'vengeful spirit', 'venomancer', 'viper', 'visage', 'void spirit',

    'warlock', 'weaver', 'windranger', 'winter wyvern', 'witch doctor',
    'wraith king',

    'zeus'
]

heroes_dict = {'亚巴顿': 'abaddon', '炼金': 'alchemist', '冰魂': 'ancient apparition', '敌法': 'anti-mage', 
               '电狗': 'arc warden', '斧王': 'axe', '班尼': 'bane', '蝙蝠': 'batrider', '兽王': 'beastmaster', 
               '血魔': 'bloodseeker', '赏金': 'bounty hunter', '酒仙': 'brewmaster', '钢背': 'bristleback', 
               '蜘蛛': 'broodmother', '人马': 'centaur warrunner', '混沌': 'chaos knight', '陈': 'chen', '克林克兹': 'clinkz', 
               '发条': 'clockwerk', '冰女': 'crystal maiden', '黑贤': 'dark seer', '仙女': 'dark willow', '大锤': 'dawnbreaker', 
               '戴泽': 'dazzle', 'dp': 'death prophet', '萨尔': 'disruptor', '末日': 'doom', '龙骑': 'dragon knight', 
               '小黑': 'drow ranger', '土猫': 'earth spirit', '小牛': 'earthshaker', '大牛': 'elder titan', 
               '火猫': 'ember spirit', '小鹿': 'enchantress', '谜团': 'enigma', '虚空': 'faceless void', '墨客': 'grimstroke', 
               '飞机': 'gyrocopter', '松鼠': 'hoodwink', '哈斯卡': 'huskar', '卡尔': 'invoker', 'io': 'io', '双头龙': 'jakiro', '剑圣': 'juggernaut', 
               '光法': 'keeper of the light', 'kez': 'kez', '船长': 'kunkka', '蛤蟆':'largo','军团': 'legion commander', '老鹿': 'leshrac', '巫妖': 'lich', 
               '小狗': 'lifestealer', '火女': 'lina', '莱恩': 'lion', '德鲁伊': 'lone druid', '露娜': 'luna', '狼人': 'lycan', '猛犸': 'magnus',
                 '马西': 'marci', 'mars': 'mars', '美杜莎': 'medusa', '米波': 'meepo', '白虎': 'mirana', '大圣': 'monkey king', '水人': 'morphling', 
                 '奶绿': 'muerta', '娜迦': 'naga siren', "先知": "nature's prophet", 'nec': 'necrophos', '夜魔': 'night stalker', 
                 '小强': 'nyx assassin', '蓝胖': 'ogre magi', '全能': 'omniknight', '神谕': 'oracle', '黑鸟': 'outworld destroyer', 
                 '滚滚': 'pangolier', '幻刺': 'phantom assassin', '猴子': 'phantom lancer', '凤凰': 'phoenix', '兽': 'primal beast',
                   '帕克': 'puck', '屠夫': 'pudge', '骨法': 'pugna', '女王': 'queen of pain', '电魂': 'razor', '力丸': 'riki', '小丑': 'ringmaster', 
                   '拉比克': 'rubick', '沙王': 'sand king', '毒狗': 'shadow demon', '影魔': 'shadow fiend', '萨满': 'shadow shaman', 
                   '沉默': 'silencer', '天怒': 'skywrath mage', '大鱼': 'slardar', '小鱼': 'slark', '奶奶': 'snapfire', '火枪': 'sniper', 
                   '幽鬼': 'spectre', '白牛': 'spirit breaker', '蓝猫': 'storm spirit', '流浪': 'sven', '炸弹': 'techies', 
                   '圣堂': 'templar assassin', 'tb': 'terrorblade', '潮汐': 'tidehunter', '伐木机': 'timbersaw', 'tk': 'tinker', 
                   '小小': 'tiny', '大树': 'treant protector', '巨魔': 'troll warlord', '海民': 'tusk', '屁股': 'underlord', '尸王': 'undying', 
                   '拍拍': 'ursa', '复仇': 'vengeful spirit', '剧毒': 'venomancer', '毒龙': 'viper', '维萨吉': 'visage', '紫猫': 'void spirit',
                   '术士': 'warlock', '蚂蚁': 'weaver', '风行': 'windranger', '冰龙': 'winter wyvern', '巫医': 'witch doctor', 
                   '骷髅王': 'wraith king', '宙斯': 'zeus'}

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
""