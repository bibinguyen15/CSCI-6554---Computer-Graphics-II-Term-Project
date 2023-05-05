import constants


class Edge:
    def __init__(self, edge, vertices=[]):
        self.name = edge
        self.vertices = []
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
    def __init__(self, number, coordinates, color=[], normal=[]):
        self.number = number
        self.coordinates = coordinates
        self.color = constants.color
        self.normal = normal


class Polygon:
    def __init__(self, poly):
        self.vertices = poly
        self.color = constants.color
        self.ymin = 0
        self.ymax = 0
        self.edges = []
        self.normal = []

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

