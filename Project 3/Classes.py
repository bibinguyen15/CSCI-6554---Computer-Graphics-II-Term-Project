import numpy as np
import random
from Project_3 import *


class Edge:
    def __init__(self, edge):
        self.name = edge
        self.ymax = 0
        self.ymin = 0
        self.xmin = 0  # x at ymin
        self.zmin = 0  # z at ymin
        self.slope = 0  # x over y
        self.zySlope = 0  # z over y

    def print(self):
        print("Edge:", self.name, "-- Slope=", self.slope)
        print("Y_max=", self.ymax, "- Y_min=",
              self.ymin, "- X_min=", self.xmin, "- Z_min=", self.zmin)


class Vertex:
    def __init__(self, coordinates, color, normal):
        self.coordinates = coordinates
        self.color = color
        self.normal = normal


class Polygon:
    def __init__(self, poly):
        self.vertices = poly
        self.color = [random.random(), random.random(), random.random()]
        self.ymin = 0
        self.ymax = 0
        self.edges = []
        self.normal = []

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

    def sortEdges(self):
        self.edges.sort(key=lambda x: x.ymin)


class Object:
    def __init__(self, file, cam, pRef):
        fileName = "D files\\" + file + ".d.txt"
        self.rawPolys, self.rawVertices, self.normals = transformation(
            fileName, cam, pRef)
        self.polygons = []
        self.vertices = []
        self.processVertices()
        self.setEdges()  # immediately updates polygons
        # mode: -1 constant, 0 Gouraud, 1 Phong
        self.mode = -1

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
            #print("_________________________________________\n", poly)
            p_yMin = float('inf')
            p_yMax = float('-inf')

            p = Polygon(poly)

            for i in range(len(poly)):

                edge = (poly[i], poly[i - 1])

                e = Edge(edge)

                # Each edge = poly[i] and poly[i+1]
                v1 = self.vertices[edge[0]]
                v2 = self.vertices[edge[1]]
                #print(edge[0], "=", v1, ",", edge[1], "=", v2)

                # Setting edge info
                e.slope = (v2[0] - v1[0]) / (v2[1] - v1[1])
                e.zySlope = (v2[2] - v1[2]) / (v2[1] - v1[1])
                e.ymax = int(max(v2[1], v1[1]))
                e.ymin = int(min(v2[1], v1[1]))
                e.xmin = v1[0] if v1[1] < v2[1] else v2[0]
                e.zmin = v1[2] if v1[1] < v2[1] else v2[2]

                # Handling ymax and ymin of the polygon
                if e.ymax > p_yMax:
                    p_yMax = e.ymax
                if e.ymin < p_yMin:
                    p_yMin = e.ymin

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

        for p in self.polygons:
            # p.print()
            AET = []
            yScan = p.ymin
            flag = True

            while yScan < p.ymax and flag:
                #print("yScan=", yScan)
                for e in p.edges:
                    if e.ymin == yScan:
                        AET.append(e)
                    elif e.ymin > yScan:
                        break

                AET.sort(key=lambda k: k.xmin)

                # printAET(AET)

                for i in range(len(AET) // 2):

                    start = AET[i * 2]
                    end = AET[i * 2 + 1]
                    z = start.zmin
                    if start.xmin != end.xmin:
                        zx = (end.zmin - start.zmin) / \
                            (end.xmin - start.xmin)
                    else:
                        zx = 0

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
                        #print("Edge slope:", edge.name, edge.slope)
                        edge.xmin += edge.slope
                        if edge.xmin >= 1000:
                            flag = False
                        edge.zmin += edge.zySlope

        return


def changeBack(value, coordinate=0):
    # 0 if value is x or y
    if coordinate == 0:
        result = value / 1000 * 2 - 1
    else:
        result = value / 1000
    return result

