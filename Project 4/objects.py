import numpy as np
import random
from transformation import *
from illumination import *
from classes import *
import constants
from texture import *

class Object:
    def __init__(self, file, V, pRef, i, mode=-1):
        fileName = "D files\\" + file + ".d.txt"
        self.rawPolys, self.rawVertices, self.polyNormals = transformation(
            fileName, V, pRef)
        # print("These are the polygons showing:", self.rawPolys)
        self.polygons = []
        self.vertices = []
        self.texture = loadTexture(constants.textureFile)

        # illumination model object
        self.i = i

        # mode: -1 constant, 0 Gouraud, 1 Phong
        self.mode = mode

        # immediately updates polygons
        self.getVertices()
        self.setVertices()
        self.backFaceCulling()
        self.setEdgesPolys()

    def getVertices(self):
        # update the vertices

        for i, vertex in enumerate(self.rawVertices):
            x = (vertex[0] + 1) / 2 * 1000
            y = (vertex[1] + 1) / 2 * 1000
            z = (vertex[2]) * 1000

            self.vertices.append(Vertex(i, np.array([x, y, z])))

    def setVertices(self):
        # print(self.rawPolys)

        for v in self.vertices:
            # print("For vertex:", v.number)
            normal = np.zeros(3)
            for i, p in enumerate(self.rawPolys):
                if v.number in p:
                    # print("Polygon:", p, "p.normal=", self.polyNormals[i])
                    normal += self.polyNormals[i]

            # print(normal)
            normal = unitVector(normal)
            v.normal = normal
            v.color = self.i.phongIllumination(self.texture, v.normal, constants.n)
            # print(
            # f"\nVertex {v.number} normal ={normal}\nVertex color={v.color}")

    def backFaceCulling(self):
        for k, poly in enumerate(self.rawPolys):
            # print(poly)
            if self.polyNormals[k][2] <= 0:
                p = Polygon(poly)
                p.normal = self.polyNormals[k]
                self.polygons.append(p)

    def setEdgesPolys(self):
        """
        This functions creates edges, polygons, and updates polygon.edges
        """

        # print("There are", len(self.polygons), "polygons")

        for p in self.polygons:
            # print("_________________________________________\n", poly)
            p_yMin = float('inf')
            p_yMax = float('-inf')

            for i in range(len(p.vertices)):

                edge = (p.vertices[i], p.vertices[i - 1])

                # Each edge = poly[i] and poly[i-1]
                v1 = self.vertices[edge[0]].coordinates
                v2 = self.vertices[edge[1]].coordinates
                ymax = int(max(v2[1], v1[1]))
                ymin = int(min(v2[1], v1[1]))

                # Only add edge if edge is not horizontal
                if ymax != ymin:
                    e = Edge(edge)

                    # Setting edge info

                    e.ymax = ymax
                    e.ymin = ymin

                    e.xmin = v1[0] if v1[1] < v2[1] else v2[0]
                    e.zmin = v1[2] if v1[1] < v2[1] else v2[2]

                    # Add the vertices in order of ascending y value
                    if v1[1] < v2[1]:
                        e.vertices = [self.vertices[edge[0]],
                                      self.vertices[edge[1]]]
                    else:
                        e.vertices = [self.vertices[edge[1]],
                                      self.vertices[edge[0]]]

                    e.slope = (v2[0] - v1[0]) / (v2[1] - v1[1])
                    e.zySlope = (v2[2] - v1[2]) / (v2[1] - v1[1])
                    # Handling ymax and ymin of the polygon
                    if e.ymax > p_yMax:
                        p_yMax = e.ymax
                    if e.ymin < p_yMin:
                        p_yMin = e.ymin

                    p.edges.append(e)  # non-horizontal edges only

            # Processing polygon
            p.ymax = p_yMax
            p.ymin = p_yMin
            p.sortEdges()

    def scanConversionConstant(self, image, depth):
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
                # print("yScan=", yScan)
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
                        # print("Edge slope:", edge.name, edge.slope)
                        edge.xmin += edge.slope
                        if edge.xmin >= 1000:
                            flag = False
                        edge.zmin += edge.zySlope

        return

    def scanConversionGouraud(self, image, depth):
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
                # print("yScan=", yScan)
                for e in p.edges:
                    if e.ymin == yScan:
                        AET.append(e)
                    elif e.ymin > yScan:
                        break

                AET.sort(key=lambda k: k.xmin)

                # printAET(AET)

                for i in range(len(AET) // 2):
                    # initialize the 2 edges
                    start = AET[i * 2]
                    end = AET[i * 2 + 1]

                    # Initialize z value
                    z = start.zmin
                    if start.xmin != end.xmin:
                        zx = (end.zmin - start.zmin) / \
                             (end.xmin - start.xmin)
                    else:
                        zx = 0

                    # Initialize l values
                    I1 = start.vertices[0].color  # I at ymin of start edge
                    I2 = start.vertices[1].color  # I at ymax of start edge
                    I3 = end.vertices[0].color  # I at ymin of end edge
                    I4 = end.vertices[1].color  # I at ymax of end edge

                    # I of left point (smaller)
                    Ia = I1 * (start.ymax - yScan) / (start.ymax - start.ymin) + \
                         I2 * (yScan - start.ymin) / (start.ymax - start.ymin)

                    # I of right point
                    Ib = I3 * (end.ymax - yScan) / (end.ymax - end.ymin) + \
                         I4 * (yScan - end.ymin) / (end.ymax - end.ymin)

                    for x in range(int(start.xmin), int(end.xmin)):
                        Ip = Ia * (end.xmin - x) / (end.xmin - start.xmin) + \
                             Ib * (x - start.xmin) / (end.xmin - start.xmin)

                        if changeBack(z, 1) < depth[x][yScan]:
                            depth[x][yScan] = changeBack(z, 1)
                            image[x][yScan] = Ip

                        z += zx

                yScan += 1

                for edge in AET:
                    if edge.ymax == yScan:
                        AET.remove(edge)
                    else:
                        # print("Edge slope:", edge.name, edge.slope)
                        edge.xmin += edge.slope
                        if edge.xmin >= 1000:
                            flag = False
                        edge.zmin += edge.zySlope

        return

    def scanConversionPhong(self, image, depth):
        def printAET(AET):
            print("Printing AET table:")
            for e in AET:
                print("Edge:", e.name)

        for p in self.polygons:
            # p.print()
            AET = []
            yScan = p.ymin
            flag = True

            while yScan < p.ymax and flag:
                # print("yScan=", yScan)
                for e in p.edges:
                    if e.ymin == yScan:
                        AET.append(e)
                    elif e.ymin > yScan:
                        break

                AET.sort(key=lambda k: k.xmin)

                # printAET(AET)

                for i in range(len(AET) // 2):
                    # initialize the 2 edges
                    start = AET[i * 2]
                    end = AET[i * 2 + 1]
                    # print(start.name, end.name)1

                    # Initialize z value
                    z = start.zmin
                    if start.xmin != end.xmin:
                        zx = (end.zmin - start.zmin) / \
                             (end.xmin - start.xmin)
                    else:
                        zx = 0

                    # Initialize normal values
                    n1 = start.vertices[0].normal  # n at ymin of start edge
                    n2 = start.vertices[1].normal  # n at ymax of start edge
                    n3 = end.vertices[0].normal  # n at ymin of end edge
                    n4 = end.vertices[1].normal  # n at ymax of end edge

                    # print(start.name, n1, n2, end.name, n3, n4)

                    # n of left point (smaller)
                    na = n1 * (start.ymax - yScan) / (start.ymax - start.ymin) + \
                         n2 * (yScan - start.ymin) / (start.ymax - start.ymin)
                    # na = unitVector(na)

                    # n of right point
                    nb = n3 * (end.ymax - yScan) / (end.ymax - end.ymin) + \
                         n4 * (yScan - end.ymin) / (end.ymax - end.ymin)
                    # print(start.name, na, end.name, nb)
                    # nb = unitVector(nb)

                    for x in range(int(start.xmin), int(end.xmin)):
                        np = na * (end.xmin - x) / (end.xmin - start.xmin) + \
                             nb * (x - start.xmin) / (end.xmin - start.xmin)
                        # print(np)
                        np = unitVector(np)

                        if changeBack(z, 1) < depth[x][yScan]:
                            depth[x][yScan] = changeBack(z, 1)
                            # u, v = textureMap(self.texture[0], self.texture[1],[x, yScan, z])
                            color = self.i.phongIllumination(self.texture, np, constants.n)
                            image[x][yScan] = color

                        z += zx

                yScan += 1

                for edge in AET:
                    if edge.ymax == yScan:
                        AET.remove(edge)
                    else:
                        # print("Edge slope:", edge.name, edge.slope)
                        edge.xmin += edge.slope
                        if edge.xmin >= 1000:
                            flag = False
                        edge.zmin += edge.zySlope

        return

    def color(self, image, depth):
        # Constant shading
        if self.mode == -1:
            print(f'In constant shading mode.')
            for p in self.polygons:
                p.color = self.i.phongIllumination(self.texture, p.normal, constants.n)
            self.scanConversionConstant(image, depth)
        # Gouraud shading
        elif self.mode == 0:
            print(f'In Gouraud shading mode.')
            self.scanConversionGouraud(image, depth)
        # Phong shading
        else:
            print(f'In Phong shading mode.')
            self.scanConversionPhong(image, depth)
