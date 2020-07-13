import cv2
import numpy as np

import skeletonize


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

    skel = skeletonize.zhang_suen(threshold)
    #skel = skeletonize.skeletonize(threshold)
    cv2.imshow("skeletonized", skel)
    cv2.waitKey(0)
    return skel


def make_graph(image):
    corners = cv2.goodFeaturesToTrack(image, 0, 0.025, 3)


if __name__ == "__main__":
    img0 = cv2.imread('maze.png', 0)
    img1 = cv2.imread('color_maze.png', 0)
    img2 = cv2.imread('tc_maze.png', 0)
    skel = process_image(img0)
