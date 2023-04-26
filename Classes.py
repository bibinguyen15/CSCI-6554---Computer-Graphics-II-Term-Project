import numpy as np
import random
from Project_2 import *


class Edge:
    def __init__(self, edge):
        self.name = edge
        self.ymax = 0
        self.ymin = 0
        self.xmin = 0  # x at ymin
        self.zmin = 0  # z at ymin
        self.slope = 0  # x over y
        self.zySlope = 0  # z over y

        # self.xintersect = 0

    def print(self):
        print("Edge:", self.name, "-- Slope=", self.slope)
        print("Y_max=", self.ymax, "- Y_min=",
              self.ymin, "- X_min=", self.xmin, "- Z_min=", self.zmin)


class Polygon:
    def __init__(self, poly):
        self.vertices = poly
        self.color = [random.random(), random.random(), random.random()]
        self.ymin = 0
        self.ymax = 0
        self.edges = []

        # all pixels inside this polygon (including vertex)
        self.pixelList = []
        self.screenPixel = []

    def printEdgeX(self):
        print("Xmin of all edges in polygon:", self.vertices)
        for e in self.edges:
            print("Edge:", e.name, "ymin=", e.ymin,
                  "x=", e.xmin, "zmin=", e.zmin, "ymax=", e.ymax)

    # Prints polygon information
    def print(self):

        print("\n+++++Polygon information+++++ \nVertices:", self.vertices, "total:",
              len(self.vertices), "vertices")
        for i, v in enumerate(self.vertices):
            print("Vertex:", i, ":", v)
        print("Color:", self.color)
        print("Edge table:", self.edges,
              "with a range from", self.ymin, "to", self.ymax)
        print("Pixel list:", self.pixelList)

    def sortEdges(self):
        self.edges.sort(key=lambda x: x.ymin)


class Object:
    def __init__(self, file):
        fileName = "D files\\" + file + ".d.txt"
        self.rawPolys, self.rawVertices = transformation(fileName)

        self.polygons = []
        self.vertices = []

        self.processVertices()
        self.setEdges()  # immediately updates polygons

    # update the vertices
    def processVertices(self):
        for vertex in self.rawVertices:
            x = (vertex[0] + 1) / 2 * 1000
            y = (vertex[1] + 1) / 2 * 1000
            z = (vertex[2]) * 1000

            self.vertices.append(np.array([x, y, z]))

    def setEdges(self):
        '''
        This functions creates edges, polygons, and updates polygon.edges
        '''

        print("There are", len(self.rawPolys), "polygons")

        for poly in self.rawPolys:
            print("_________________________________________\n", poly)

            p_yMin = float('inf')
            p_yMax = float('-inf')

            p = Polygon(poly)

            for i in range(len(poly)):

                edge = (poly[i], poly[i - 1])

                e = Edge(edge)
                print("Edge info:", edge)
                # Each edge = poly[i] and poly[i+1]
                v1 = self.vertices[edge[0]]
                v2 = self.vertices[edge[1]]
                print(edge[0], "=", v1, ",", edge[1], "=", v2)
                # Setting edge info
                e.slope = (v2[0] - v1[0]) / (v2[1] - v1[1])
                e.zySlope = (v2[2] - v1[2]) / (v2[1] - v1[1])
                e.ymax = int(max(v2[1], v1[1]))
                e.ymin = int(min(v2[1], v1[1]))
                e.xmin = v1[0] if v1[1] < v2[1] else v2[0]
                e.zmin = v1[2] if v1[1] < v2[1] else v2[2]

                # Handling vertex-scanline intersection
                # e.ymax -= 1

                # Handling ymax and ymin of the polygon
                if e.ymax > p_yMax:
                    p_yMax = e.ymax
                if e.ymin < p_yMin:
                    p_yMin = e.ymin

                e.print()
                # p.edges.append(e)

                if e.ymax != e.ymin:
                    p.edges.append(e)  # non horizontal edges only

            # Processing polygon
            p.ymax = p_yMax
            p.ymin = p_yMin
            p.sortEdges()

            # Adding polygon to list of polygons of object
            # p.print()
            self.polygons.append(p)

    def scanConversion(self, image, depth):
        def printAET(AET):
            print("Printing AET table:")
            for e in AET:
                print("Edge:", e.name, "x=", e.xmin)
        over = False
        # p = self.polygons[0]
        for p in self.polygons:
            # if True:
            print("\nIn scan conversion for:", p.vertices)

            p.print()
            AET = []
            yScan = p.ymin

            p.printEdgeX()

            for yScan in range(p.ymin, p.ymax + 1):
                print("yScan=", yScan)
                for e in p.edges:
                    if e.ymin == yScan:
                        AET.append(e)
                    elif e.ymin > yScan:
                        break

                AET.sort(key=lambda k: k.xmin)

                printAET(AET)

                for i in range(len(AET) // 2):

                    start = AET[i * 2]
                    end = AET[i * 2 + 1]
                    z = start.zmin
                    if start.xmin != end.xmin:
                        zx = (end.zmin - start.zmin) / \
                            (end.xmin - start.xmin)
                    else:
                        zx = 0

                    print("Start:", start.name, "x:", start.xmin)
                    print("End:", AET[i * 2 + 1].name,
                          "x:", AET[i * 2 + 1].xmin)

                    for x in range(int(start.xmin), int(end.xmin)):
                        if changeBack(z, 1) < depth[x][yScan]:
                            depth[x][yScan] = changeBack(z, 1)
                            image[x][yScan] = p.color

                        z += zx

                yScan += 1

                for edge in AET:
                    if edge.ymax == yScan:
                        AET.remove(edge)
                    else:
                        print("Edge slope:", edge.name, edge.slope)

                        edge.xmin += edge.slope
                        if edge.xmin >= 1000:

                            print(edge.name)
                            print(edge.name[0], "=", self.vertices[edge.name[0]],
                                  "-", edge.name[1], "=", self.vertices[edge.name[1]])
                            over = True
                        edge.zmin += edge.zySlope
                if over:
                    break

            print(p.edges)

        return


def changeBack(value, coordinate=0):
    # 0 if value is x or y
    if coordinate == 0:
        result = value / 1000 * 2 - 1
    else:
        result = value / 1000
    return result


'''
'''

# glClearColor(0.0, 0.0, 0.0, 0.0)
# glClear(GL_COLOR_BUFFER_BIT)

# house = Object("house")
# print("Here")
# image = np.zeros((1000, 1000, 3))
# depth = np.ones((1000, 1000))

# house.scanConversion(image, depth)

# coordinates = np.where(depth < 1)


# glBegin(GL_POINTS)
# for i in range(1000):
# for j in range(1000):
# if image[i][j]
# print(depth[i][j])
# glEnd()
# glFlush()

# for x in coordinates:
# if i == 3:
# break

# print(x)
# print(depth[x[0]][x[1]])
# i += 1

'''
test = np.ones((3, 2))

for i in range(2):
    test[i][1] = 0

pos = np.where(test < 1)

for x in pos:
    print(x[0], ",", x[1])
'''
