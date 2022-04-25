from .config import *
import math

# 速度上限补正
async def judge_speed(speed_limit, site_type, feeling, situation):
    speed_limit_patch = speed_limit * feeling_bonus[feeling] - site_type_bonus[site_type][situation]['speed_limit']
    return speed_limit_patch

# 体力补正
async def judge_hp_bonus(run_type):
    hp_bonus = run_type_bonus[run_type]['hp_bonus']
    return hp_bonus

# 力量补正
async def judge_power(power, site_type, feeling, situation):
    power_patch = power * feeling_bonus[feeling] - site_type_bonus[site_type][situation]['power']
    return power_patch

# 根性补正
async def judge_determination(determination, feeling):
    determination_patch = determination * feeling_bonus[feeling]
    return determination_patch

# 智力补正
async def judge_intelligence(intelligence, feeling, run_adaptability):
    intelligence_patch = intelligence * feeling_bonus[feeling] * run_adaptability_bonus[run_adaptability]
    return intelligence_patch

# 基准速度
async def speed_standard(track_length):
    speed_standard_patch = 20 - (track_length - 2000) / 1000
    return speed_standard_patch

# 序盘体力消耗
async def cacul_begin_endurance(speed_standard_patch, run_type, intelligence_patch, power_patch, site_adaptability, \
    track_length, track_adaptability, site_type, situation):
    # 匀速速度
    uniform_speed = speed_standard_patch * (run_type_bonus[run_type]['speed_begin'] + \
        intelligence_patch * math.log(intelligence_patch / 10, 10) / 550000 - 0.00325 )
    # 残差加速度
    acceleration_difference = 0.0006 * ((500 * power_patch) ** 0.5) * run_type_bonus[run_type]['acceleration_begin'] \
        * site_adaptability_bonus[site_adaptability] * track_adaptability_bonus[track_adaptability]['acceleration']
    # 加速度
    acceleration = 24 + acceleration_difference
    # 加速耗时
    accelerate_time = (speed_standard_patch * 0.85 - 3) / acceleration + (uniform_speed - speed_standard_patch * 0.85) \
        / acceleration_difference
    # 加速阶段总距离
    acceleration_length = (uniform_speed + 3) / 2 * accelerate_time
    # 匀速耗时
    uniform_time = (track_length / 6 - acceleration_length) / uniform_speed
    # 加速耗体
    accelerate_endurance = 20 * hp_consume_bonus[site_type][situation] * ((((acceleration * (speed_standard_patch * 0.85 - 3)\
        / acceleration + uniform_speed - speed_standard_patch + 12) ** 3) - ((uniform_speed - speed_standard_patch + \
            12)** 3)) / (144 * 3 * acceleration) + (((acceleration_difference * (uniform_speed - speed_standard_patch * 0.85)\
        / acceleration_difference + uniform_speed - speed_standard_patch + 12) ** 3) - ((uniform_speed - speed_standard_patch + \
            12)** 3)) / (144 * 3 * acceleration_difference))
    # 匀速耗体
    uniform_endurance = 20 * hp_consume_bonus[site_type][situation] * ((uniform_speed - speed_standard_patch + 12) ** 2) \
        / 144 * uniform_time
    # 总耗体
    endurance = accelerate_endurance + uniform_endurance
    return endurance, uniform_speed

# 中盘体力消耗
async def cacul_middle_endurance(uniform_speed_tmp, speed_standard_patch, run_type, intelligence_patch, power_patch, site_adaptability, \
    track_length, track_adaptability, site_type, situation):
    # 匀速速度
    uniform_speed = speed_standard_patch * (run_type_bonus[run_type]['speed_middle'] + \
        intelligence_patch * math.log(intelligence_patch / 10, 10) / 550000 - 0.00325 )
    # 加速度
    if uniform_speed_tmp > uniform_speed:
        acceleration = -0.8
    else:
        acceleration = 0.0006 * ((500 * power_patch) ** 0.5) * run_type_bonus[run_type]['acceleration_middle'] \
            * site_adaptability_bonus[site_adaptability] * track_adaptability_bonus[track_adaptability]['acceleration']
    # 加速耗时
    accelerate_time = (uniform_speed - uniform_speed_tmp) / acceleration
    # 加速阶段总距离
    acceleration_length = (uniform_speed + uniform_speed_tmp) / 2 * accelerate_time
    # 匀速耗时
    uniform_time = (track_length / 2 - acceleration_length) / uniform_speed
    # 加速耗体
    accelerate_endurance = 20 * hp_consume_bonus[site_type][situation] * (((acceleration * accelerate_time + uniform_speed - \
        speed_standard_patch + 12) ** 3) - ((uniform_speed - speed_standard_patch + 12)** 3)) / (144 * 3 * acceleration)
    # 匀速耗体
    uniform_endurance = 20 * hp_consume_bonus[site_type][situation] * ((uniform_speed - speed_standard_patch + 12) ** 2) \
        / 144 * uniform_time
    # 总耗体
    endurance = accelerate_endurance + uniform_endurance
    return endurance, uniform_speed

# 终盘体力消耗
async def cacul_end_endurance(speed_limit_patch, uniform_speed_tmp, speed_standard_patch, run_type, intelligence_patch, power_patch, \
    site_adaptability, track_length, track_adaptability, site_type, situation, end_endurance_bonus):
    # 冲刺速度
    uniform_speed = speed_standard_patch * (run_type_bonus[run_type]['speed_end'] + intelligence_patch * \
        math.log(intelligence_patch / 10, 10) / 550000 - 0.00325 + 0.01) + ((speed_limit_patch / 500) ** 0.5) * \
        track_adaptability_bonus[track_adaptability]['speed_limit'] * 2
    # 加速度
    acceleration = 0.0006 * ((500 * power_patch) ** 0.5) * run_type_bonus[run_type]['acceleration_end'] \
        * site_adaptability_bonus[site_adaptability] * track_adaptability_bonus[track_adaptability]['acceleration']
    # 加速耗时
    accelerate_time = (uniform_speed - uniform_speed_tmp) / acceleration
    # 加速阶段总距离
    acceleration_length = (uniform_speed + uniform_speed_tmp) / 2 * accelerate_time
    # 冲刺耗时
    uniform_time = (track_length / 3 - acceleration_length) / uniform_speed
    # 加速耗体
    accelerate_endurance = 20 * hp_consume_bonus[site_type][situation] * (((acceleration * accelerate_time + uniform_speed - \
        speed_standard_patch + 12) ** 3) - ((uniform_speed - speed_standard_patch + 12)** 3)) / (144 * 3 * acceleration) \
        * end_endurance_bonus
    # 冲刺耗体
    uniform_endurance = 20 * hp_consume_bonus[site_type][situation] * ((uniform_speed - speed_standard_patch + 12) ** 2) \
        / 144 * uniform_time * end_endurance_bonus
    # 总耗体
    endurance = accelerate_endurance + uniform_endurance
    return endurance

# 总耐力需求
async def cacul_endurance(endurance_begin, endurance_middle, endurance_end, track_length, run_type):
    # 总体力需求
    endurance_tmp = endurance_begin + endurance_middle + endurance_end
    # 总耐力需求
    endurance = (endurance_tmp - track_length) / (0.8 * run_type_bonus[run_type]['hp_bonus'])
    return endurance

# 理论体力
async def theoretical_endurance(track_length, endurance_tmp, run_type):
    theoretical_hp = track_length + endurance_tmp * 0.8 * run_type_bonus[run_type]['hp_bonus']
    return theoretical_hp

# 回体技能折算耐力
async def cacul_skill_endu(stable_recover_level, hp, run_type):
    # 固有回耐量
    stable_recover_endu = 0.055 * stable_recover_bonus[stable_recover_level] * hp / run_type_bonus[run_type]['hp_bonus']
    # 单个普通回耐量
    common_recover_endu = 0.015 * hp / run_type_bonus[run_type]['hp_bonus']
    # 单个金回耐量
    upper_recover_endu = 0.055 * hp / run_type_bonus[run_type]['hp_bonus']
    return stable_recover_endu, common_recover_endu, upper_recover_endu

# 回体技能折算体力
async def cacul_skill(stable_recover_level, common_recover_num, upper_recover_num, theoretical_hp):
    # 固有回体量
    stable_recover = 0.055 * stable_recover_bonus[stable_recover_level] * theoretical_hp
    # 单个普通回体量
    common_recover_single = 0.015 * theoretical_hp
    # 全部普通回体量
    common_recover = common_recover_num * common_recover_single
    # 单个金回体量
    upper_recover_single = 0.055 * theoretical_hp
    # 全部金回体量
    upper_recover = upper_recover_num * upper_recover_single
    return stable_recover, common_recover_single, common_recover, upper_recover_single, upper_recover

# 算上技能后的总耐力
async def get_end_endurance(end_hp, track_length, run_type):
    end_endurance = (end_hp - track_length) / (0.8 * run_type_bonus[run_type]['hp_bonus'])
    return end_endurance