# -*- encoding: utf-8 -*-
import consts

type = ''
first_primitive = ''
other_primitives = []
structural_words = []
relational_primitives = {}
relationalsimbol_primitives = {}
is_relational = False
is_relationalsimbol = False

is_first = True
relational_primitive_key = ''
relationalsimbol_primitive_key = ''


def init():
    global type, first_primitive, other_primitives, structural_words, \
        relational_primitives, relationalsimbol_primitives, \
        is_relational, is_relationalsimbol, is_first, \
        relational_primitive_ley, relationalsimbol_primitive_key
    type = ''
    first_primitive = ''
    other_primitives = []
    structural_words = []
    relational_primitives = {}
    relationalsimbol_primitives = {}
    is_relational = False
    is_relationalsimbol = False
    is_first = True
    relational_primitive_key = ''
    relationalsimbol_primitive_key = ''


def parse_detail(attr):
    global type, first_primitive, other_primitives, structural_words, \
        relational_primitives, relationalsimbol_primitives, \
        is_relational, is_relationalsimbol, is_first, \
        relational_primitive_key, relationalsimbol_primitive_key
    init()

    # 第一个字段为type，第二个字段为义原[]
    type = attr[0]
    detail = attr[1].split(',')
    for part in detail:
        if len(part) == 0:
            continue
        # 具体词
        if part.find('(') != -1 and part.find(')') != -1:
            part = part[1:-1]

        # 关系义原
        if part.find('=') != -1:
            is_relational = True
            is_relationalsimbol = False
            strs = part.split('=')
            relational_primitive_key = strs[0]
            if len(strs[1].split('|')) > 1:
                relational_primitive_value = strs[1].split('|')[1]
            else:
                relational_primitive_value = strs[1]
            add_relational_primitive(relational_primitive_key, relational_primitive_value)
            continue
        strs = part.split('|')
        primitive_type = get_primitive_type(strs[0])
        value = ''
        if len(strs) > 1:
            value = strs[1]
        if len(value) > 0 and (value.find(')') != -1 or value.find('}') != -1):
            value = value[0:-1]

        # 基本义原
        if primitive_type == 0:
            if is_relational:
                add_relational_primitive(relational_primitive_key, value)
                continue
            elif is_relationalsimbol:
                add_relationalsimbol_primitive(relationalsimbol_primitive_key, value)
                continue
            elif is_first:
                first_primitive = value;
                is_first = False
                continue
            else:
                other_primitives.append(value)
                continue
        # 关系义原
        elif primitive_type == 1:
            is_relationalsimbol = True
            is_relational = False
            relationalsimbol_primitive_key = strs[0][0]
            add_relationalsimbol_primitive(relationalsimbol_primitive_key, value)
        # 特殊义原
        elif primitive_type == 2:
            if len(value) > 0:
                structural_words.append(value)
            else:
                english = strs[0]
                if strs[0][0] == '{':
                    english = english[1:]
                if strs[0][-1] == '}':
                    english = english[0:-1]
                structural_words.append(english)
            continue
        else:
            print('type error!')


def add_relational_primitive(key, value):
    global relational_primitives
    if key in relational_primitives:
        relational_primitives[key].append(value)
    else:
        relational_primitives[key] = [value]


def add_relationalsimbol_primitive(key, value):
    global relationalsimbol_primitives
    if key in relationalsimbol_primitives:
        relationalsimbol_primitives[key].append(value)
    else:
        relationalsimbol_primitives[key] = [value]


#0为基本义原，1为关系义原，2为特殊义原
def get_primitive_type(value):
    first = value[0]
    if consts.RELATIONAL_SYMBOL.find(first) != -1:
        return 1
    elif consts.SPECIAL_SYMBOL.find(first) != -1:
        return 2
    else:
        return 0


def return_attr():
    global type, first_primitive, other_primitives, structural_words, relational_primitives, relationalsimbol_primitives
    dic = {}
    dic['type'] = type
    dic['first_primitive'] = first_primitive
    dic['other_primitives'] = other_primitives
    dic['structural_words'] = structural_words
    dic['relational_primitives'] = relational_primitives
    dic['relationalsimbol_primitives'] = relationalsimbol_primitives
    return dic
