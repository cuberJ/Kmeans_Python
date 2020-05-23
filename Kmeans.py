import math
import numpy as np
import matplotlib.pyplot as plt
import random
DataPath = "cluster.dat"
K = 7
COLOR = ["red", "yellow", "green", "black", "blue", "m", "c"]
MAXDIS = pow(2, 31)
Ans = {}
SSE = K*200
SSEs = []
def DisCount(x1, x2, y1, y2):  # 计算两点距离
    return math.sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2))

def CentralChoice(point, CentralPoint):  # 计算每个点归属到哪一个聚类中心
    MinDistance = MAXDIS
    MinPoint = 0
    for i in range(len(CentralPoint)):
        distance = DisCount(point[0], CentralPoint[i][0], point[1], CentralPoint[i][1])
        if(distance <= MinDistance):
            MinDistance = distance
            MinPoint = i
    return MinPoint

def KMeans(data, CentralPoint):  #传入np数据源和选定好的K个聚类中心
    for i in range(len(data)):
        MinCentral = CentralChoice(data[i], CentralPoint)
        Ans[CentralPoint[MinCentral]].append(data[i])

def CentralPointInit(data):  # 初始选择K个聚类中心
    CentralPoint = []
    for i in range(K):
        pos = random.randint(0, len(data)-1)
        point = data[pos]
        CentralPoint.append(point)
        Ans[point] = [point]
    return CentralPoint

def CentralPointUpdate(data):  # 更新K个聚类中心
    newCentrals = []
    isChange = 0
    for key in Ans.keys():  # 遍历每个聚类中心
        sumx = 0
        sumy = 0
        for j in Ans[key]:
            sumx += j[0]
            sumy += j[1]
        x = sumx / len(Ans[key])
        y = sumy / len(Ans[key])
        minDis = MAXDIS
        newCentral = key

        for j in Ans[key]:  # 遍历每个聚类中心所划分到的点
            if(DisCount(j[0], x, j[1], y) < minDis):
                newCentral = j
        if newCentral[0] != key[0] and newCentral[1] != key[1]:
            #print("发生了改变")
            #print(newCentral[0], key[0], newCentral[1], key[1])
            isChange = 1
        newCentrals.append(newCentral)
    Ans.clear()
    for i in newCentrals:
        Ans[i] = [i]
    return isChange, newCentrals

def SSECount():
    sumdis = 0
    for key in Ans.keys():
        dis = 0
        for j in Ans[key]:
            dis += DisCount(j[0], key[0], j[1], key[1])
        sumdis += dis
    SSEs.append(sumdis)
    return sumdis <= SSE

def FileRead():  #读取指定的数据文件进行分析
    data = np.loadtxt(DataPath, dtype=float)
    data = tuple(map(tuple, data))
    CentralPoint = CentralPointInit(data)
    while True:
        KMeans(data, CentralPoint)
        xs, ys = [], []
        for key in Ans.keys():
            x, y = [], []
            for i in Ans[key]:
                x.append(i[0])
                y.append(i[1])
            xs.append(x)
            ys.append(y)
        for center in range(K):
            plt.scatter(xs[center], ys[center], marker="+", color=COLOR[center])
        plt.ion()
        plt.pause(1)
        if SSECount() is True:
            break
        isChange, CentralPoint = CentralPointUpdate(data)
        if isChange == 0:
            break
    flag = ""
    for i in range(len(SSEs)-1):
        if(SSEs[i] < SSEs[i+1]):
            flag = "WRONG"
    print(SSEs, flag)

while True:
    FileRead()
    Ans.clear()
    SSEs.clear()
    plt.close()
    import time
    time.sleep(1)