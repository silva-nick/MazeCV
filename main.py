import cv2
import numpy as np

import skeletonize
import graph
import bfs


def background_color(image):
    unique_array, counts = np.unique(image, return_counts=True)
    return unique_array[counts.argmax()]


def morph(image):
    elem = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    cropped = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    eroded = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    for i in range(4):
        eroded = cv2.erode(image, elem, iterations=1)
        temp = cv2.dilate(eroded, elem, iterations=1)
        temp = cv2.subtract(image, temp)
        cropped = cv2.bitwise_or(cropped, temp)
        image = eroded.copy()
    cv2.imshow("morphed", image)
    return image


def maze_path(image):
    image = morph(image)
    image = cv2.bitwise_not(image)
    return image


def process_image(image):
    maze = image.copy()
    (h, w) = maze.shape
    if background_color(maze) == 0:
        maze = cv2.bitwise_not(maze)

    t, threshold = cv2.threshold(maze, 225, 255, cv2.THRESH_BINARY)
    cv2.imshow("main", threshold)
    maze = maze_path(threshold.copy())

    #skel = skeletonize.zhang_suen(threshold)
    skel = skeletonize.skeletonize(threshold)
    cv2.imshow("skeletonized", skel)
    return skel


def make_graph(image):
    corners = cv2.goodFeaturesToTrack(image, 0, .05, 15)
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

    final_image = process_image(img1)
    graph = make_graph(final_image)
    color = cv2.cvtColor(final_image, cv2.COLOR_GRAY2RGB)
    graph_img = graph.draw_graph(color)

    cv2.imshow("graph", graph_img)
    cv2.waitKey(0)
