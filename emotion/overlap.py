# -*- encoding: utf-8 -*-
import apriori
from getsim import get_sim
import chardet


# 计算两个词语语义相似度
# xb喵喵喵
def sim(f, t):
    return get_sim(f, t)


# 计算文档doc对聚类cluster的隶书度
def score(cluster, doc):
    ans = 0.0
    for t in doc:
        max_sim = 0.0
        for f in cluster:
            max_sim = sim(f, t)
            #print(max_sim)
        ans += max_sim
    return ans / len(doc)


# 去重重复情感簇，
# 实现方式为每个文档找到一个与之匹配度最大的情感度
# 返回belong[文档index] = 情感簇index
def main(docs, clusters):
    belong = {}

    for i in range(len(docs)):
        max_sco = 0.0
        bel = 0
        for j in range(len(clusters)):
            sco = score(clusters[j], docs[i])
            if sco > max_sco:
                max_sco = sco
                bel = j
        belong[i] = bel
        #print(docs[i], ' ', clusters[j])
    return belong


if __name__ == '__main__':

    docs = apriori.docs
    clusters = apriori.apriori(docs, 0.02)
    print(clusters)
    kk = main(docs, clusters)
    print(kk)
