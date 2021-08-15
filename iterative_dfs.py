import cv2
import graph

class iddfs:
    def __init__(self, graph, start, target):
        self.marked = [False]*graph.V()
        self.vertexTo = [None]*graph.V()
        self.start = start
        self.graph = graph
        found = False
        depth = 0
        while not found and depth < 1000: # cutoff depth for unsolvable mazes
            if self.dfs(target, depth):
                return True
            depth += 1
        return False

    def dfs(self, root, target, depth):
        if root is target:
            return True
        if depth <= 0:
            return False
        for w in graph.adj(root):
            if not(self.marked[w]):
                self.marked[w] = True
                self.vertexTo[w] = root
                if self.dfs(w, target, depth-1):
                    return True

    def path_to(self, vertex):
        if not(self.marked[vertex]):
            raise ValueError(
                'BFS cannot find a solution. Make sure the image is correct.')
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
