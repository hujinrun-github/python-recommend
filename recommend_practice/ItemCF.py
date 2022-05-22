#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：recommendSystem 
@File    ：itemCF.py
@Author  ：hujinrun
@Date    ：2022/1/9 8:56 下午 
'''
import math
from operator import  itemgetter
def ItemCF(train,K, Nitem):
    """
    :params: train, 训练数据集
    :params: K topK的物品数
    :params: N, 超参数，设置取TopN推荐物品数目
    :return: GetRecommendation, 推荐接口函数
    """
    # 1.构建倒排
    # 2.计算召回和正样本的数量
    # 3.计算打分
    # train : user->items
    N = dict() # 统计每个用户消费过的作品数
    C = dict() # 统计两个用户共同消费过的作品数
    for user,items in train.items():
        for item in items:
            if item not in (N,C):
                N[item] = 0
                C[item] = dict()
            N[item] += 1
            for otheritem in items:
                if item == otheritem:
                    continue
                if otheritem not in C[item]:
                    C[item][otheritem] = 0
                C[item][otheritem] += 1
    # 计算相似度
    W = dict()
    for item, otheritems in C.items():
        if item not in W:
            W[item] = dict()
        for otheritem, relative in otheritems.items():
            W[item][otheritem] = relative/math.sqrt(N[item]*N[otheritem])
    # 获取推荐结果
    def GetRecommendation(user):
        rank = dict()
        interacted_items = train[user]
        # 选出相似度最高的topK个物品
        for item in interacted_items:
            for j, wj in sorted(W[item].items(), key=itemgetter(1), reverse=True)[0:K]:
                if j in interacted_items:
                    continue
                if j not in rank:
                    rank[j] = 0
                rank[j] += wj
        recs = list(sorted(rank.items(), key=lambda x: x[1], reverse=True))[:Nitem]
        return recs
    return GetRecommendation
