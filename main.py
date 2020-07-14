import cv2
import numpy as np

import skeletonize
import graph
import bfs


def background_color(image):
    unique_array, counts = np.unique(image, return_counts=True)
    return unique_array[counts.argmax()]


def custom_threshold(image, cutoff):
    (h, w) = image.shape
    for x in range(h):
        for y in range(w):
            if image[x, y] < cutoff:
                image[x, y] = 0
            else:
                image[x, y] = 255
    return image


def process_image(image):
    maze = image.copy()
    (h, w) = maze.shape

    if background_color(maze) == 0:
        maze = cv2.bitwise_not(maze)

    #threshold = custom_threshold(maze, 150)
    t, threshold = cv2.threshold(maze, 225, 255, cv2.THRESH_BINARY)

    #skel = skeletonize.zhang_suen(threshold)
    skel = skeletonize.skeletonize(threshold)
    cv2.imshow("skeletonized", skel)
    return skel


def make_graph(image):
    corners = cv2.goodFeaturesToTrack(image, 0, .01, 15)
    term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
    cv2.cornerSubPix(image, corners, (5, 5), (-1, -1), term)
    g = graph.Graph()
    for vertex in corners:
        g.add_vertex(vertex[0][0], vertex[0][1])
    return g


if __name__ == "__main__":
    img0 = cv2.imread('maze.png', 0)
    img1 = cv2.imread('color_maze.png', 0)
    img2 = cv2.imread('tc_maze.png', 0)

    skel = process_image(img0)
    graph = make_graph(skel)
    color = cv2.cvtColor(skel, cv2.COLOR_GRAY2RGB)
    graph_img = graph.draw_graph(color)

    cv2.imshow("graph", graph_img)
    cv2.waitKey(0)
