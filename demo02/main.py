# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 17:01:56 2022

@author: wily_elite
"""
import random
import Delaunay as d
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.animation as animation
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
fig = plt.figure()
plt.triplot(tri.Triangulation(XS, YS, TS), 'bo-')
data = DT.Get_Midpoint()
#保证显示的数据集没有问题
mid_points = list(data.keys())
x = [p.x for p in mid_points]
y = [p.y for p in mid_points]
plt.scatter(x,y)
neighours = list(data.values())
random_point, = random.sample(mid_points,1)
image = []
seen = set()
ways = []
seen.add(random_point)
ways.append(random_point)
#DFS函数
def DFS(data,deepth,start_point):
    for w in data[start_point]:
        if deepth == 0 :
            x = [p.x for p in ways]
            y = [p.y for p in ways]
            im = plt.plot(x,y)
            image.append(im)
            return 
        if w not in seen:
            seen.add(w)
            ways.append(w)
            DFS(data,deepth-1,w)
            seen.remove(w)
            ways.pop() 
DFS(data,deepth=5,start_point=random_point)
#生成视频格式文件
image.extend(image)    
ani = animation.ArtistAnimation(fig, image, interval=500)
Writer = animation.writers['ffmpeg']  # 需安装ffmpeg
#设置fps为1来控制画面每一秒播放一张图
writer = Writer(fps=1, metadata=dict(artist='Me'), bitrate=1800)
ani.save("demo02.mp4",writer=writer)
