import cv2
import graph

class astar:
    def __init__(self, graph, start):
        self.marked = [False]*graph.V()
        self.vertexTo = [None]*graph.V()
        self.start = start
        self.graph = graph
        queue = [start]
        self.marked[start] = True
        while len(queue) > 0:
            v = queue.pop(0)
            for w in graph.adj(v):
                if not(self.marked[w]):
                    queue.append(w)
                    self.marked[w] = True
                    self.vertexTo[w] = v

    def path_to(self, vertex):
        if not(self.marked[vertex]):
            raise ValueError(
                'A* cannot find a solution. Make sure the image is correct.')
        path = [vertex]
        while not(path[0] == self.start):
            path.insert(0, self.vertexTo[path[0]])
        return path

    def draw_path_to(self, img, end):
        path = self.path_to(end)
        for vertex in path:
            if not(vertex == self.start):
                img = cv2.line(
                    img, self.graph.vertices[self.vertexTo[vertex]], self.graph.vertices[vertex], (240, 228, 93), 2)

        return img
