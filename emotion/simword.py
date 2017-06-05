# -*- encoding: utf-8 -*-
import tree
import consts


def sim_word(attr1, attr2):
    if len(attr1['structural_words']) != len(attr2['structural_words']):
        return 0
    elif len(attr1['structural_words']) != 0 and len(attr2['structural_words']) != 0:
        return sim_list(attr1['structural_words'], attr2['structural_words'])
    elif len(attr1['structural_words']) == 0 and len(attr2['structural_words']) == 0:
        sim1 = sim_primitive(attr1['first_primitive'], attr2['first_primitive'])
        sim2 = sim_list(attr1['other_primitives'], attr2['other_primitives'])
        sim3 = sim_dic(attr1['relational_primitives'], attr2['relational_primitives'])
        sim4 = sim_dic(attr1['relationalsimbol_primitives'], attr2['relationalsimbol_primitives'])
        tmp = sim1
        sum = consts.BETA1 * tmp
        tmp *= sim2
        sum += consts.BETA2 * tmp
        tmp *= sim3
        sum += consts.BETA3 * tmp
        tmp *= sim4
        sum += consts.BETA4 * tmp
        return sum
    else:
        return 0.0


def sim_list(list1, list2):
    size_list1 = len(list1)
    size_list2 = len(list2)
    if size_list1 == 0 and size_list2 == 0:
        return 1
    size_big = size_list1 if size_list1 > size_list2 else size_list2
    size_small = size_list1 if size_list1 < size_list2 else size_list2
    count = 0
    sum = 0
    while count < size_small:
        max = 0
        rm_item1 = list1[0]
        rm_item2 = list2[0]
        for item1 in list1:
            for item2 in list2:
                sim = inner_simword(item1, item2)
                if sim > max:
                    rm_item1 = item1
                    rm_item2 = item2
                    max = sim
        sum += max
        list1.remove(rm_item1)
        list2.remove(rm_item2)
        count += 1
    return (sum + consts.DELTA * (size_big - size_small)) / size_big * 1.0


def sim_dic(dic1, dic2):
    size_dic1 = len(dic1)
    size_dic2 = len(dic2)
    if size_dic1 == 0 and size_dic2 == 0:
        return 1
    size_total = size_dic1 + size_dic2
    sim = 0
    count = 0
    for key1, value1 in dic1.items():
        if key1 in dic2:
            value2 = dic2[key1]
            sim = sim_list(value1, value2)
            count += 1
    return (sim + consts.DELTA * (size_total - 2 * count)) / (size_total - count)


def inner_simword(word1, word2):
    is_primitive1 = word1 in tree.primitive_id
    is_primitive2 = word2 in tree.primitive_id
    if is_primitive1 and is_primitive2:
        return sim_primitive(word1, word2)
    elif not is_primitive1 and not is_primitive2:
        if word1 == word2:
            return 1
        else:
            return 0
    return consts.GAMMA


def sim_primitive(primitive1, primitive2):
    dis = dis_primitive(primitive1, primitive2)
    return consts.ALPHA / (dis + consts.ALPHA)


def dis_primitive(primitive1, primitive2):
    list1 = get_parentid(primitive1)
    list2 = get_parentid(primitive2)
    if list1 != -1 and list2 != -1:
        for id in list1:
            if list2.count(id) > 0:
                index1 = list1.index(id)
                index2 = list2.index(id)
                return index1 + index2
    return consts.DEFAULT_PRIMITIVE_DIS


# 获取tree.py中的上层id列表
def get_parentid(primitive):
    if primitive in tree.primitive_id:
        self_id = tree.primitive_id[primitive]
        id_list = [self_id]
        while not is_top(self_id):
            self_id = tree.all_primitive[self_id][2]
            id_list.append(self_id)
        return id_list
    else:
        print('primitive no exist!')
        return -1


def is_top(self_id):
    return self_id == tree.all_primitive[self_id][2]
