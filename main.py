import cv2
import numpy as np

import skeletonize as sk
import graph
import bfs


def background_color(image):
    unique_array, counts = np.unique(image, return_counts=True)
    return unique_array[counts.argmax()]


def morph(image):
    elem = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    size = image.size
    last = image.copy()
    while(cv2.countNonZero(last) > size//2):
        last = cv2.erode(last, elem, iterations=1)

    return last


def maze_path(image):
    morphed = morph(image)
    morphed_flipped = cv2.bitwise_not(morphed)
    cv2.imshow("morphed", morphed_flipped)
    skel = sk.zhang_suen(morphed_flipped)
    return skel


def process_image(image):
    maze = image.copy()
    (h, w) = maze.shape
    if background_color(maze) == 0:
        maze = cv2.bitwise_not(maze)
    t, threshold = cv2.threshold(maze, 225, 255, cv2.THRESH_BINARY)
    cv2.imshow("threshold", threshold)

    path = maze_path(threshold.copy())
    #cv2.imshow("path", path)

    #skel = sk.zhang_suen(threshold)
    #skel = sk.skeletonize(path)
    #cv2.imshow("skeletonized", skel)
    return path


def make_graph(image):
    corners = cv2.goodFeaturesToTrack(image, 0, .05, 10)
    term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
    cv2.cornerSubPix(image, corners, (5, 5), (-1, -1), term)
    g = graph.Graph()
    for vertex in corners:
        g.add_vertex(int(round(vertex[0][0])), int(round(vertex[0][1])))
    return g

# image must be a path


def find_edges(image, graph):
    def neighbors(x, y):
        l, r, t, b = x-1, x+1, y-1, y+1
        return [(t, x, image[t, x]), (t, r, image[t, r]), (y, r, image[y, r]), (b, r, image[b, r]), (b, x, image[b, x]), (b, l, image[b, l]), (y, l, image[y][l]), (t, l, image[t][l])]

    vertices = graph.vertices
    (h, w) = image.shape
    start_min = max(w, h)
    end_max = min(w, h)
    start = end = None

    for vertex in vertices:
        if vertex[0] < start_min or vertex[1] < start_min:
            start_min = min(vertex[0], vertex[1])
            start = vertex
        elif vertex[0] > end_max or vertex[1] > end_max:
            end_max = max(vertex[0], vertex[1])
            end = vertex

    image = cv2.circle(image, (start[0], start[1]), radius=3,
                       color=(252, 71, 71), thickness=-1)
    image = cv2.circle(image, (end[0], end[1]), radius=3,
                       color=(252, 71, 71), thickness=-1)

    point_queue = [start]
    last_vertex = start
    while point_queue:
        point = point_queue.pop(0)
        nearby = neighbors(point[0], point[1])
        for n in nearby:
            if n[2] == 0:
                point_queue.append(n)
                v = (n[0], n[1])
                if v in vertices:
                    graph.add_edge(last_vertex, v)
                    last_vertex = v
                image.itemset((n[1], n[0]), 200)
    return graph.vertices.index(start), graph.vertices.index(end)


if __name__ == "__main__":
    img0 = cv2.imread('maze.png', 0)
    img1 = cv2.imread('color_maze.png', 0)
    img2 = cv2.imread('tc_maze.png', 0)

    final_image = process_image(img0)
    graph = make_graph(final_image)
    color = cv2.cvtColor(final_image, cv2.COLOR_GRAY2RGB)
    graph_img = graph.draw_graph(color)
    cv2.imshow("graph", graph_img)

    start, end = find_edges(final_image, graph)
    cv2.imshow("!", graph_img)
    #search = bfs.bfs(graph, start)
    #search.draw_path_to(graph_img, end)

    cv2.waitKey(0)
