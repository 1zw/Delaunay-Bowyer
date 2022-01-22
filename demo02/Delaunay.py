# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 16:25:28 2022

@author: wily_elite

ref1:"https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm"
"""
import numpy as np
#判断两条边是否相同
def SharedEdge(line1, line2):
    if (line1[0] == line2[0] and line1[1] == line2[1]) or (line1[0] == line2[1] and line1[1] == line2[0]):
        return True
    return False
#顶点类
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #降低hash重复率
        self.hash = 71*x+7*y
    #类的方法重写
    def __add__(self, b):
        return Point(self.x + b.x, self.y + b.y)
    def __sub__(self, b):
        return Point(self.x - b.x, self.y - b.y)
    def __mul__(self, b):
        return Point(b * self.x, b * self.y)
    
    def __eq__(self,other):
        return self.x==other.x and self.y==other.y
    
    def __hash__(self):
        return hash(self.hash)
    __rmul__ = __mul__
    #判断是否在外接圆中
    def IsInCircumcircleOf(self, T):
        #T是一个三角形类，用a，b，c三个点分别做三角形的顶点
        a_x = T.v[0].x
        a_y = T.v[0].y
        b_x = T.v[1].x
        b_y = T.v[1].y
        c_x = T.v[2].x
        c_y = T.v[2].y
        #本点的坐标
        d_x = self.x
        d_y = self.y
        # 用行列式判断，如果下列行列式大于零，则点位于外圆内
        incircle = np.array([[a_x - d_x, a_y - d_y, (a_x - d_x) ** 2 + (a_y - d_y) ** 2],
                             [b_x - d_x, b_y - d_y, (b_x - d_x) ** 2 + (b_y - d_y) ** 2],
                             [c_x - d_x, c_y - d_y, (c_x - d_x) ** 2 + (c_y - d_y) ** 2]])
        #numpy库，矩阵求行列式（标量）
        if np.linalg.det(incircle) > 0:
            return True
        else:
            return False
#三角形类
class Triangle:
    #初始化函数
    def __init__(self, a, b, c):
        #用None占3个point位
        self.v = [None] * 3
        self.v[0] = a
        self.v[1] = b
        self.v[2] = c
        #edge属性表示三角形的每条表
        self.edges = [[self.v[0], self.v[1]],
                      [self.v[1], self.v[2]],
                      [self.v[2], self.v[0]]]
        
        self.neighbour = [None] * 3
    #判断某个点是否是三角形的顶点
    def HasVertex(self, point):
        if (self.v[0] == point) or (self.v[1] == point) or (self.v[2] == point):
            return True
        return False

        
class Delaunay_Triangulation:
    #用一个超三角形来初始化Delaunay列表
    def __init__(self, WIDTH, HEIGHT):
        self.triangulation = []
        #利用相似形原理获得三个顶点坐标
        self.SuperPointA = Point(-100, -100)
        self.SuperPointB = Point(2 * WIDTH + 100, -100)
        self.SuperPointC = Point(-100, 2 * HEIGHT + 100)
        superTriangle = Triangle(self.SuperPointA, self.SuperPointB, self.SuperPointC)
        self.triangulation.append(superTriangle)
    #Bowyer-Waston算法核心：向列表中增加点
    def AddPoint(self, p):
        #每次加点都定义一个坏三角列表，用于在添加完点之后删除
        bad_triangles = []
        for triangle in self.triangulation:
            # 检查给定的点是否在三角形的外圆内
            if p.IsInCircumcircleOf(triangle):
                # 如果在，将这个三角形添加到坏三角列表中
                bad_triangles.append(triangle)
        #定义凸包
        polygon = []
        #循环遍历所有的坏三角，构建出p点所在的凸包轮廓
        for current_triangle in bad_triangles:
            for this_edge in current_triangle.edges:
                isNeighbour = False
                for other_triangle in bad_triangles:
                    if current_triangle == other_triangle:
                        continue
                    for that_edge in other_triangle.edges:
                        if SharedEdge(this_edge, that_edge):
                            #检查这条边是否是两个三角形共有的，如果是，则不加入凸包
                            isNeighbour = True
                if not isNeighbour:
                    polygon.append(this_edge)

        #删除所有的坏三角关系
        for each_triangle in bad_triangles:
            self.triangulation.remove(each_triangle)

        #添加新的三角关系
        for each_edge in polygon:
            newTriangle = Triangle(each_edge[0], each_edge[1], p)
            self.triangulation.append(newTriangle)
    #删除超级三角形
    def Remove_Super_Triangles(self):
        onSuper = lambda triangle: triangle.HasVertex(self.SuperPointA) or triangle.HasVertex(self.SuperPointB) or triangle.HasVertex(self.SuperPointC)
        for triangle_new in self.triangulation[:]:
            if onSuper(triangle_new):
                self.triangulation.remove(triangle_new)
    #导出所有点的坐标和三角形索引
    def export(self):
        ps = [p for t in self.triangulation for p in t.v]
        x_s = [p.x for p in ps]
        y_s = [p.y for p in ps]
        ts = [(ps.index(t.v[0]), ps.index(t.v[1]), ps.index(t.v[2])) for t in self.triangulation]
        return x_s, y_s, ts
    #本属性可以不要，但是可以用来加速形成三角形
    def Find_Neighbours(self):
        # 函数来找到本Delaunay三角形的相邻Delaunay三角形
        for one in self.triangulation:
            edge = 0
            for this_edge in one.edges:
                edge = (edge + 1) % 3
                for other in self.triangulation:
                    if one == other:
                        continue
                    for that_edge in other.edges:
                        if SharedEdge(this_edge, that_edge):
                            one.neighbour[edge] = other
    
    def Get_Midpoint(self):
        #创建图
        total_midpoint = {}
        #判断本点是否看过，集合中不会出现重复元素
        seen = set()
        for one in self.triangulation:
            for this_edge in one.edges:
                #获得本边的中点
                mid = (this_edge[0]+this_edge[1])*0.5
                if mid not in seen:
                    #创建一个邻居中点列表
                    this_edge_neighbour = []
                    for other in self.triangulation:
                        if one == other:
                            #将本三角形中的非本边中点添加到三角形列表中
                            for lines in one.edges:
                                if not SharedEdge(lines,this_edge):
                                    lines_midpoint = (lines[0]+lines[1])*0.5
                                    this_edge_neighbour.append(lines_midpoint)
                            
                            continue
                        #判断是否是邻居三角形
                        isrepeat = False
                        for other_edge in other.edges:
                            if SharedEdge(this_edge,other_edge):
                                isrepeat = True
                        #如果是，将另外两条边添加到邻居列表中，不是的话，break到其它的三角形查找
                        if not isrepeat:
                               continue
                        else:
                            for other_edge in other.edges:
                                if not SharedEdge(other_edge,this_edge):
                                    lines_midpoint = (other_edge[0]+other_edge[1])*0.5
                                    this_edge_neighbour.append(lines_midpoint)
                            
                        #四个点肯定就满了，可以降低循环次数
                        if len(this_edge_neighbour) == 4:
                            break
                    seen.add(mid)
                    total_midpoint[mid] = this_edge_neighbour
        return total_midpoint
def MAP(data):
    this_map = np.zeros((len(data),len(data)))
    mid_points = list(data.keys())
    for points in mid_points:
        nei = data[points]
        for p in nei:
            this_map[mid_points.index(points)][mid_points.index(p)] = 1
    return this_map