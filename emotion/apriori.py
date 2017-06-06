# -*- encoding: utf-8 -*-
import imp
import sys
import json
imp.reload(sys)

def apriori(D, minSup):
    '''频繁项集用keys表示，
    key表示项集中的某一项，
    cutKeys表示经过剪枝步的某k项集。
    C表示某k项集的每一项在事务数据库D中的支持计数
    '''

    C1 = {}  # 每个词出现的频数
    for T in D:
        for I in T:
            if I in C1:
                C1[I] += 1
            else:
                C1[I] = 1
    # print C1

    _keys1 = C1.keys()  # 获取index: 每个词
    keys1 = []
    for i in _keys1:
        keys1.append([i])

    n = len(D)  # 删去非频繁项集
    cutKeys1 = []
    for k in keys1[:]:
        if 1.*C1[k[0]] / n >= minSup:
            cutKeys1.append(k)
    cutKeys1.sort()

    keys = cutKeys1
    # print keys
    all_keys = []
    while keys != []:
        C = getC(D, keys)
        cutKeys = getCutKeys(keys, C, minSup, len(D))
        for key in cutKeys:
            all_keys.append(key)
        keys = aproiri_gen(cutKeys)
        # print keys

    return all_keys


def getC(D, keys):
    '''对keys中的每一个key进行计数'''
    C = []
    for key in keys:
        c = 0
        for T in D:
            have = True
            for k in key:
                if k not in T:
                    have = False
            if have:
                c += 1
        C.append(c)
    return C


def getCutKeys(keys, C, minSup, length):
    '''剪枝步'''
    for i, key in enumerate(keys):
        if float(C[i]) / length < minSup:
            keys.remove(key)
    return keys


def keyInT(key, T):
    '''判断项key是否在数据库中某一元组T中'''
    for k in key:
        if k not in T:
            return False
    return True


def aproiri_gen(keys1):
    '''连接步'''
    keys2 = []
    for k1 in keys1:
        for k2 in keys1:
            if k1 != k2:
                key = []
                for k in k1:
                    if k not in key:
                        key.append(k)
                for k in k2:
                    if k not in key:
                        key.append(k)
                key.sort()
                if key not in keys2:
                    keys2.append(key)
    return keys2


D = [['A', 'B', 'C', 'D'],
     ['B', 'C', 'E'],
     ['A', 'B', 'C', 'E'],
     ['B', 'D', 'E'],
     ['A', 'B', 'C', 'D']]


def fuck_wx_json():
    f = open('data/weibodata.json', encoding='utf-8')
    data = f.read()
    data = data.replace('“seg”','')
    f = open('data/data.json','w',encoding='utf-8')
    f.write(data)


def get_data_from_wx():
    f = open('data/wx.json', encoding='utf-8')
    data = json.load(f)

    global docs
    docs = []
    for item in data:
        seg = item['segresult']
        if seg == None: continue
        doc = seg.split(' ')
        doc.pop()
        docs.append(doc)
    return docs


def get_weibo_data():
    f = open('data/weibo.json',encoding='utf-8')
    data = json.load(f)

    docs = []
    for item in data:
        #print(item['-id'])
        sens = item['sentence']
        if type(sens) == dict:
            doc = sens['seg']
            if doc == '': continue
            doc = doc.split(' ')
            #print(doc)
            docs.append(doc)
        else:  # list: len > 1
            for sen in sens:
                doc = sen['seg']
                if doc == '': continue
                doc = doc.split(' ')
                #print(doc)
                docs.append(doc)
    print('初始情感簇：%d 个' % len(docs))
    return docs

docs = get_weibo_data()


if __name__ == '__main__':
    print(docs)
    F = apriori(docs, 0.02)
    print (len(F))
    print('frequent itemset:', F)
