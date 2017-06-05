# -*- encoding: utf-8 -*-
import overlap
import apriori


def sim_clu(clu_a, clu_b):
    if type(clu_a) == int or type(clu_b) == int: return 0
    k = (len(clu_a) * len(clu_b)) / 2
    k = int(k)
    if k == 0: k = len(clu_a) * len(clu_b)
    sims = []
    for a in clu_a:
        for b in clu_b:
            sims.append(overlap.sim(a,b))
    sims.sort()
    sum = 0.0
    for i in range(k):
        sum += sims[-i-1]
    return 1. * sum / k


# 获取一堆情感簇的相似度矩阵
def get_mat(clusters):
    mat = []
    max_sim = row = col = 0

    for i in range(len(clusters)):
        mat.append([])
        for j in range(len(clusters)):
            mat[i].append(0)

    for i in range(len(clusters)):
        for j in range(len(clusters)):
            if i == j:
                mat[i][j] = 0
            else:
                mat[i][j] = mat[j][i] = sim_clu(clusters[i], clusters[j])
                if mat[i][j] > max_sim:
                    max_sim = mat[i][j]
                    row = i
                    col = j
    return mat, max_sim, row, col


#合并a, b两个情感簇
#合并其特征词，讲原本属于b的doc丢进a中
def merge(a, b):
    print('merge %d %d', a, b)
    for word in clusters[b]:
        if not word in clusters[a]:
            clusters[a].append(word)
    for i in range(len(docs)):
        if belong[i] == b:
            belong[i] = a
    clusters[b] = a


# 阈值为k，将cluster合并到还剩n个
def main(clusters, k, n):
    while True:
        mat, max_sim, row, col = get_mat(clusters)
        if max_sim < k:
            return clusters
        else:
            merge(row, col)


if __name__ == '__main__':
    docs = apriori.docs
    clusters = apriori.apriori(docs, 0.1)
    belong  = overlap.main(docs,clusters)
    result = main(clusters, 0.4, 6)
    for i in range(len(result)):
        if type(clusters[i]) == int:continue
        sum = 0
        for j in range(len(belong)):
            if belong[j] == i: sum += 1
        print(clusters[i], ' ', sum)
