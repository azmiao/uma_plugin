
def get_relation(r_data_list, uma_list):
    end_point = 0
    for each_group in r_data_list:
        group_list = each_group['成员'].split(', ')
        relation_point = 0
        for uma_name in uma_list:
            if uma_name in group_list:
                relation_point = int(each_group['relation_point'])
            else:
                relation_point = 0
                break
        if relation_point > 0:
            end_point += relation_point
    return end_point
