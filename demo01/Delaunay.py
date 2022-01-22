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
    #类的方法重写
    def __add__(self, b):
        return Point(self.x + b.x, self.y + b.y)
    def __sub__(self, b):
        return Point(self.x - b.x, self.y - b.y)
    def __mul__(self, b):
        return Point(b * self.x, b * self.y)
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