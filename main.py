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
    #cv2.imshow("morphed", morphed_flipped)
    skel = sk.zhang_suen(morphed_flipped)
    return skel


def process_image(image):
    maze = image.copy()
    (h, w) = maze.shape
    if background_color(maze) == 0:
        maze = cv2.bitwise_not(maze)
    t, threshold = cv2.threshold(maze, 225, 255, cv2.THRESH_BINARY)
    #cv2.imshow("threshold", threshold)

    path = maze_path(threshold.copy())
    #cv2.imshow("path", path)

    skel = sk.zhang_suen(threshold)
    #skel = sk.skeletonize(path)
    #cv2.imshow("skeletonized", skel)
    return path, skel


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
        output = []
        (h, w) = image.shape
        if x > 0:
            if image[y, l] == 0:
                output.append((y, l))
            if y > 0:
                if image[t, l] == 0:
                    output.append((t, l))
            if y < h-1:
                if image[b, l] == 0:
                    output.append((b, l))
        if x < w-1:
            if image[y, r] == 0:
                output.append((y, r))
            if y > 0:
                if image[t, r] == 0:
                    output.append((t, r))
            if y < h-1:
                if image[b, r] == 0:
                    output.append((b, r),)
        if y > 0:
            if image[t, x] == 0:
                output.append((t, x))
        if y < h-1:
            if image[b, x] == 0:
                output.append((b, x))
        return output

    vertices = graph.vertices
    (h, w) = image.shape
    start_min = max(w, h)
    end_max = 0
    start = end = None
    for vertex in vertices:
        if vertex[0] < start_min or vertex[1] < start_min:
            start_min = min(vertex[0], vertex[1])
            start = vertex
        elif vertex[0] > end_max or vertex[1] > end_max:
            end_max = max(vertex[0], vertex[1])
            end = vertex

    point_queue = [(start, start)]
    while len(point_queue) > 0:
        point, last_vertex = point_queue.pop(0)
        nearby = neighbors(point[0], point[1])
        for n in nearby:
            v = (n[1], n[0])
            if v in vertices:
                #print((point, last_vertex))
                graph.add_edge_points(last_vertex, v)
                last_vertex = v
                point_queue.append((v, last_vertex))
        for n in nearby:
            v = (n[1], n[0])
            if v not in vertices:
                point_queue.append((v, last_vertex))
            image.itemset((n[0], n[1]), 200)

    cv2.imshow("path", image)
    return vertices.index(start), vertices.index(end)


if __name__ == "__main__":
    img0 = cv2.imread('mazes/maze.png', 0)
    img1 = cv2.imread('mazes/color_maze.png', 0)
    img2 = cv2.imread('mazes/tc_maze.png', 0)

    path, maze = process_image(img0)
    maze = cv2.cvtColor(maze, cv2.COLOR_GRAY2RGB)
    graph = make_graph(path)
    color = cv2.cvtColor(path, cv2.COLOR_GRAY2RGB)
    start, end = find_edges(path, graph)
    graph_img = graph.draw_graph(color)

    graph_img = cv2.circle(graph_img, (graph.vertices[start][0], graph.vertices[start][1]), radius=3,
                           color=(252, 71, 71), thickness=-1)
    graph_img = cv2.circle(graph_img, (graph.vertices[end][0], graph.vertices[end][1]), radius=3,
                           color=(252, 71, 71), thickness=-1)

    cv2.imshow("graph", graph_img)

    search = bfs.bfs(graph, start)
    final_maze = search.draw_path_to(maze, end)
    cv2.imshow("solved maze", final_maze)
    cv2.imwrite("./solved/solved.jpg", final_maze)

    cv2.waitKey(0)
