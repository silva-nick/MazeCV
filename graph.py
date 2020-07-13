import cv2


class Graph:
    def __init__(self):
        self.v = 0
        self.adj = [[]]
        self.vertices = [()]

    def add_vertex(self, x, y):
        self.v += 1
        self.adj.append([])
        self.vertices.append((x, y))

    def add_vertex(self, x, y, v_from):
        self.v += 1
        self.adj.append([])
        self.vertices.append((x, y))
        self.add_edge(len(adj)-1, v_from)

    def add_edge(self, v, w):
        self.adj[v].append(w)
        self.adj[w].append(v)

    def adj(self, v):
        return adj[v]

    def vertices(self):
        return self.v

    def draw_graph(self, img):
        for x, y in self.vertices:
            img = cv2.circle(img, (y, x), radius=0,
                             color=(255, 245, 135), thickness=-1)
