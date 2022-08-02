import os
import json
import random

from hoshino import R

# =====可调整数据=====

# 最大抽卡抽数，即一井
max_gacha = 200
# UP概率（单位：千分之）
up_prob = 15
# 包括UP在内的三星概率（单位：千分之）
s3_prob = 30
# 二星概率（单位：千分之）
s2_prob = 180
# 一星概率（单位：千分之）
s1_prob = 790

# ===================

# 抽卡类
class Gacha(object):
    def __init__(self, pool_id, gacha_type, server = 'jp'):
        super().__init__()
        self.server = server
        # 卡池数据
        self.pool = self.get_pool(pool_id, server)
        self.result = {'up': [], 's3': [], 's2':[], 's1':[]}
        self.first_up = 999999
        self.up_prob = up_prob
        self.s3_prob = s3_prob
        self.s2_prob = s2_prob
        self.s1_prob = s1_prob
        # rank
        high_rank = '3' if gacha_type == 'uma' else 'SSR'
        mid_rank = '2' if gacha_type == 'uma' else 'SR'
        low_rank = '1' if gacha_type == 'uma' else 'R'
        # 角色/卡 列表
        self.up = self.pool[f'{gacha_type}_up'][high_rank]
        self.star3 = self.pool[f'other_{gacha_type}'][high_rank]
        self.star2 = self.pool[f'other_{gacha_type}'][mid_rank]
        self.star1 = self.pool[f'other_{gacha_type}'][low_rank]

    # 获取卡池信息
    def get_pool(self, pool_id, server):
        gacha_path = os.path.join(R.img('umamusume').path, 'uma_gacha')
        with open(os.path.join(gacha_path, 'uma_pool.json'), 'r', encoding='utf-8') as f:
            config = json.load(f)
        server_pool = config[server]
        if not pool_id:
            pool_id = list(server_pool.keys())[0]
        pool = server_pool[pool_id]
        return pool

    # 抽卡并整理数据
    def sort_result(self, i:int, first_up:int, result:dict, select:str = None):
        is_select = False
        if i % 10:
            chara, res_type = self.gacha_one(up_prob, s3_prob, s2_prob, s1_prob)
        # 十连保底
        else:
            chara, res_type = self.gacha_one(up_prob, s3_prob, s2_prob + s1_prob, 0)
        if res_type == 'up':
            result['up'].append(chara)
            first_up = min(i, first_up)
            # 想要的选择UP卡
            if chara == select: is_select = True
        else:
            result[res_type].append(chara)
        return first_up, result, is_select

    # 单抽
    def gacha_one(self, up_prob: int, s3_prob: int, s2_prob: int, s1_prob: int = None):
        pick = random.randint(1, s3_prob + s2_prob + s1_prob)
        if pick <= up_prob:
            return random.choice(self.up), 'up'
        elif pick <= s3_prob:
            return random.choice(self.star3), 's3'
        elif pick <= s2_prob + s3_prob:
            return random.choice(self.star2), 's2'
        else:
            return random.choice(self.star1), 's1'

    # 十连
    def gacha_ten(self, result, first_up):
        for i in range(1, 11, 1):
            first_up, result, _ = self.sort_result(i, first_up, result)
        first_up = 0 if first_up == 999999 else first_up
        return first_up, result

    # 天井，不算保底
    def gacha_tenjou(self, result, first_up):
        ten_gacha = max_gacha // 10
        for j in range(ten_gacha):
            for i in range(1, 11, 1):
                k = j * 10 + i
                first_up, result, _ = self.sort_result(k, first_up, result)
        first_up = 0 if first_up == 999999 else first_up
        return first_up, result

    # 单卡满破，即抽五张
    def gacha_full_singer(self, result, first_up):
        select_chart = random.choice(self.up)
        up_num, ten_num, exchange = 0, -1, 0
        while up_num < 5:
            ten_num += 1
            for i in range(1, 11, 1):
                k = ten_num * 10 + i
                first_up, result, is_select = self.sort_result(k, first_up, result, select_chart)
                if is_select: up_num += 1
            if ten_num and not ten_num % (max_gacha // 10):
                exchange += 1
                up_num += 1
        return select_chart, up_num, ten_num, exchange, first_up, result