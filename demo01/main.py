# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 20:44:03 2022

@author: wily_elite
"""
import random
import Delaunay as d
import matplotlib.pyplot as plt
import matplotlib.tri as tri
#初始化参数
WIDTH = int(100)
HEIGHT = int(100)
#点的数量
n = 20
#随机生成n个点
xs = [random.randint(1, WIDTH - 1) for x in range(n)]
ys = [random.randint(1, HEIGHT - 1) for y in range(n)]
#初始化
DT = d.Delaunay_Triangulation(WIDTH, HEIGHT)
#AddPoint中使用Bowyer-Waston算法
for x, y in zip(xs, ys):
    DT.AddPoint(d.Point(x, y))
#删除外面的超级大三角形
DT.Remove_Super_Triangles()
#导出点集和三角形集
XS, YS, TS = DT.export()
#画图
plt.triplot(tri.Triangulation(XS, YS, TS), 'bo-')
plt.title('Delaunay triangle subdivision')
plt.show()
plt.savefig("demo01.png")
