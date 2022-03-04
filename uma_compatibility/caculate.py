
def judge_name(name_tmp, f_data, replace_data):
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    for uma_name in name_list:
        other_name_list = list(replace_data[uma_name])
        cn_name = f_data[uma_name]['cn_name']
        if str(name_tmp) == str(cn_name) or str(name_tmp) in other_name_list:
            return cn_name
    return False

def get_relation(r_data_list, uma_list):
    end_point = 0
    for each_group in r_data_list:
        group_list = each_group['成员'].split(', ')
        for uma_name in uma_list:
            if uma_name in group_list:
                relation_point = int(each_group['relation_point'])
            else:
                relation_point = 0
                break
        if relation_point > 0:
            end_point += relation_point
    return end_point