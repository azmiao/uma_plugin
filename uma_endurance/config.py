feeling_bonus = {
    '绝好调': 1.04,
    '好调': 1.02,
    '普通': 1,
    '不调': 0.98,
    '绝不调': 0.96
}

site_type_bonus ={
    '芝':{
        '良': {
            'speed_limit': 0,
            'power': 0
        },
        '稍重': {
            'speed_limit': 0,
            'power': 50
        },
        '重': {
            'speed_limit': 0,
            'power': 50
        },
        '不良': {
            'speed_limit': 50,
            'power': 50
        }
    },
    '泥地':{
        '良': {
            'speed_limit': 0,
            'power': 100
        },
        '稍重': {
            'speed_limit': 0,
            'power': 50
        },
        '重': {
            'speed_limit': 0,
            'power': 100
        },
        '不良': {
            'speed_limit': 50,
            'power': 100
        }
    }
}

run_type_bonus = {
    '逃马': {
        'hp_bonus': 0.95,
        'speed_begin': 1,
        'speed_middle': 0.98,
        'speed_end': 0.962,
        'acceleration_begin': 1,
        'acceleration_middle': 1,
        'acceleration_end': 0.996
    },
    '先马': {
        'hp_bonus': 0.89,
        'speed_begin': 0.978,
        'speed_middle': 0.991,
        'speed_end': 0.975,
        'acceleration_begin': 0.985,
        'acceleration_middle': 1,
        'acceleration_end': 0.996
    },
    '差马': {
        'hp_bonus': 1,
        'speed_begin': 0.938,
        'speed_middle': 0.998,
        'speed_end': 0.994,
        'acceleration_begin': 0.975,
        'acceleration_middle': 1,
        'acceleration_end': 1
    },
    '追马': {
        'hp_bonus': 0.995,
        'speed_begin': 0.931,
        'speed_middle': 1,
        'speed_end': 1,
        'acceleration_begin': 0.945,
        'acceleration_middle': 1,
        'acceleration_end': 0.997
    },
}

run_adaptability_bonus = {
    'S': 1.1,
    'A': 1,
    'B': 0.85,
    'C': 0.75,
    'D': 0.6,
    'E': 0.4,
    'F': 0.2,
    'G': 0.1
}

site_adaptability_bonus = {
    'S': 1.05,
    'A': 1,
    'B': 0.9,
    'C': 0.8,
    'D': 0.7,
    'E': 0.5,
    'F': 0.3,
    'G': 0.1
}

track_adaptability_bonus = {
    'S': {
        'speed_limit': 1.05,
        'acceleration': 1
    },
    'A': {
        'speed_limit': 1,
        'acceleration': 1
    },
    'B': {
        'speed_limit': 0.9,
        'acceleration': 1
    },
    'C': {
        'speed_limit': 0.8,
        'acceleration': 1
    },
    'D': {
        'speed_limit': 0.6,
        'acceleration': 1
    },
    'E': {
        'speed_limit': 0.4,
        'acceleration': 0.6
    },
    'F': {
        'speed_limit': 0.2,
        'acceleration': 0.5
    },
    'G': {
        'speed_limit': 0.1,
        'acceleration': 0.4
    }
}

hp_consume_bonus = {
    '芝':{
        '良': 1,
        '稍重': 1,
        '重': 1.02,
        '不良': 1.02
    },
    '泥地':{
        '良': 1,
        '稍重': 1,
        '重': 1.01,
        '不良': 1.02
    }
}

stable_recover_bonus = {
    0: 0,
    1: 1,
    2: 1.02,
    3: 1.04,
    4: 1.06,
    5: 1.08,
    6: 1.1
}