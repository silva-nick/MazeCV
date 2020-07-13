import cv2
import graph


class bfs:
    def __init__(self, graph, start):
        self.marked = [None]*graph.vertices()
        self.edgeTo = [None]*graph.vertices()
        self.start = start
        self.graph = graph
        queue = []
        queue.append(start)
        self.marked[start] = True
        while queue:
            v = queue.pop(0)
            for w in graph.adj(v):
                if not(self.marked[w]):
                    queue.append(w)
                    self.marked[w] = True
                    self.edgeTo[w] = v

    def path_to(self, vertex):
        if not(self.marked[vertex]):
            return None
        path = [vertex]
        while not(path[len(path)-1] == self.start):
            path.insert(0, self.edgeTo[path[0]])
        return path

    def draw_path_to(self, img, end):
        path = self.path_to(end)
        for vertex in path:
            if not(vertex == self.start):
                img = cv2.line(
                    img, self.graph.vertices[self.edgeTo[vertex]], self.graph.vertices[vertex], (153, 192, 255), 2)

        return img
