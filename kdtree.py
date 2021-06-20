import cv2

class KDtree:
    def __init__(self):
        self.root = None
        self.n = 0

        super().__init__()

    def is_empty(self):
        return self.root == None

    def size(self):
        return self.size

    def insert(self, p):
        if self.is_empty():
            self.root = self.Node(p)
            self.n += 1
            return
        next = self.root
        horizontal = True
        while not(next == None):
            if next.point[0] == p[0] and next.point[1] == p[1]:
                return
            if horizontal:
                if p[0] < next.point[0]:
                    if next.ln != None:
                        next = next.ln
                    else:
                        next.ln = self.Node(p)
                        self.n += 1
                        return
                else:
                    if next.rn != None:
                        next = next.rn
                    else:
                        next.rn = self.Node(p)
                        self.n += 1
                        return
            else:
                if p[1] < next.point[1]:
                    if next.ln != None:
                        next = next.ln
                    else:
                        next.ln = self.Node(p)
                        self.n += 1
                        return
                else:
                    if next.rn != None:
                        next = next.rn
                    else:
                        next.rn = self.Node(p)
                        self.n += 1
                        return
            horizontal = not(horizontal)
        return

    def range(self, rect):
        if self.is_empty():
            return None
        in_range = []
        self.h_find_points(rect, self.root, in_range)
        return in_range

    def h_find_points(self, rect, node, q):
        if self.rect_contains(rect, node.point):
            q.append(node.point)
        if node.ln != None and rect[0] <= node.point[0]:
            self.v_find_points(rect, node.ln, q)
        if node.rn != None and rect[2] >= node.point[0]:
            self.v_find_points(rect, node.rn, q)

    def v_find_points(self, rect, node, q):
        if self.rect_contains(rect, node.point):
            q.append(node.point)
        if node.ln != None and rect[1] <= node.point[1]:
            self.h_find_points(rect, node.ln, q)
        if node.rn != None and rect[3] >= node.point[1]:
            self.h_find_points(rect, node.rn, q)

    def rect_contains(self, rect, p):
        if p[0] < rect[0]:
            return False
        if p[0] > rect[2]:
            return False
        if p[1] < rect[1]:
            return False
        if p[1] > rect[3]:
            return False
        return True

    def draw(self, image):
        (h, w, d) = image.shape
        points = self.range((0, 0, w, h))
        for p in points:
            image = cv2.circle(image, p, radius=1,
                               color=(255, 245, 135), thickness=-1)
        return image

    class Node:
        def __init__(self, point):
            self.point = point
            self.ln = None
            self.rn = None
            super().__init__()
