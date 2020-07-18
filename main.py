import cv2
import numpy as np
import argparse

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


def crop(image):
    (h, w) = image.shape
    while cv2.countNonZero(image[0]) == w:
        image = np.delete(image, (0), axis=0)
        h += -1
    while cv2.countNonZero(image[h-1]) == w:
        image = np.delete(image, (h-1), axis=0)
        h += -1
    while cv2.countNonZero(image[:, 0]) == h:
        image = np.delete(image, (0), axis=1)
        w += -1
    while cv2.countNonZero(image[:, w-1]) == h:
        image = np.delete(image, (w-1), axis=1)
        w += -1
    return image


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
        print("changing background color")
        maze = cv2.bitwise_not(maze)
    t, threshold = cv2.threshold(maze, 210, 255, cv2.THRESH_BINARY)
    #cv2.imshow("threshold", threshold)

    morphed = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, (1, 1))

    cropped = crop(morphed.copy())

    path = maze_path(cropped.copy())
    #cv2.imshow("path", path)

    skel = sk.zhang_suen(cropped)
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
    def neighbors(x, y, color):
        l, r, t, b = x-1, x+1, y-1, y+1
        output = []
        (h, w) = image.shape
        if x > 0:
            if image[y, l] == color:
                output.append((y, l))
            if y > 0:
                if image[t, l] == color:
                    output.append((t, l))
            if y < h-1:
                if image[b, l] == color:
                    output.append((b, l))
        if x < w-1:
            if image[y, r] == color:
                output.append((y, r))
            if y > 0:
                if image[t, r] == color:
                    output.append((t, r))
            if y < h-1:
                if image[b, r] == color:
                    output.append((b, r),)
        if y > 0:
            if image[t, x] == color:
                output.append((t, x))
        if y < h-1:
            if image[b, x] == color:
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
        nearby = neighbors(point[0], point[1], 0)

        white_nearby = neighbors(point[0], point[1], 255)
        for n in white_nearby:
            v = (n[1], n[0])
            if v in vertices:
                graph.add_edge_points(last_vertex, v)
                last_vertex = v
                image.itemset(n, 10)
            else:
                image.itemset(n, 200)

        for n in nearby:
            v = (n[1], n[0])
            if v in vertices:
                #print((point, last_vertex))
                graph.add_edge_points(last_vertex, v)
                last_vertex = v
                point_queue.append((v, last_vertex))
                if(130 <= v[0] <= 199 and v[1] > 100):
                    True == True
                    #cv2.imshow("path"+str(v), image)
                image.itemset(n, 10)
        for n in nearby:
            v = (n[1], n[0])
            if v not in vertices:
                point_queue.append((v, last_vertex))
                image.itemset(n, 200)

    cv2.imshow("path", image)
    return vertices.index(start), vertices.index(end)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Maze solver using computer vision')
    parser.add_argument("-i", action="store",
                        dest="image_name", help="name of the image")
    parser.add_argument("-s", action="store", dest="search_algo",
                        help="name of search algorithm: bfs...")
    cmd_in = parser.parse_args()

    image = cv2.imread('mazes/{}'.format(cmd_in.image_name), 0)

    path, maze = process_image(image)
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
    cv2.imwrite(
        "./solved/{}_solved.jpg".format(cmd_in.image_name.split(".")[0]), final_maze)

    cv2.waitKey(0)
