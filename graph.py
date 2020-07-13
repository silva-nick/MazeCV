class Graph:
    v = 0
    adj = [[]]
    vertices = [()]

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
