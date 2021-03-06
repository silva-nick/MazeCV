import cv2


class Graph:
    def __init__(self):
        self.v = 0
        self.adjacent = []
        self.vertices = []

    def add_vertex(self, x, y):
        self.v += 1
        self.adjacent.append([])
        self.vertices.append((x, y))

    def add_vertex_2(self, x, y, v_from):
        self.v += 1
        self.adjacent.append([])
        self.vertices.append((x, y))
        self.add_edge(len(adjacent)-1, v_from)

    def add_edge(self, v, w):
        self.adjacent[v].append(w)
        self.adjacent[w].append(v)

    def add_edge_points(self, v, w):
        v_pos = self.vertices.index(v)
        w_pos = self.vertices.index(w)
        self.adjacent[v_pos].append(w_pos)
        self.adjacent[w_pos].append(v_pos)

    def adj(self, v):
        return self.adjacent[v]

    def V(self):
        return self.v

    def draw_graph(self, img):
        for v in self.vertices:
            x, y = v
            img = cv2.circle(img, (x, y), radius=3,
                             color=(224, 55, 29), thickness=-1)
        self.draw_edges(img)
        return img

    def draw_edges(self, img):
        for v in self.vertices:
            for a in self.adj(self.vertices.index(v)):
                if a:
                    img = cv2.line(
                        img, self.vertices[a], v, (140, 245, 42), 1)
