import cv2
import numpy as np


def background_color(image):
    unique_array, counts = np.unique(image, return_counts=True)
    return unique_array[counts.argmax()]


def skeleton(image):
    done = False
    (h, w) = image.shape
    background = background_color(image)
    not_background = 255-background
    while not(done):
        done = True
        for x in range(h):
            for y in range(w):
                if image[x, y] == background:
                    pass
                else:
                    if x > 0:
                        t = image[x-1, y]
                    elif x < h-1:
                        b = image[x+1, y]
                    if y > 0:
                        l = image[x, y-1]
                    elif y < w-1:
                        r = image[x, y+1]
                    if not(r == l and r == not_background):
                        image[x, y] = background


def custom_threshold(image, cutoff):
    (h, w) = image.shape
    for x in range(h):
        for y in range(w):
            if image[x, y] < cutoff:
                image[x, y] = 0
            else:
                image[x, y] = 255
    return image


def cv2_threshold(image):
    return cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 3)


def process_image(image):
    maze = image.copy()
    (h, w, d) = maze.shape
    # x = 120/w
    # maze = cv2.resize(maze, (120, int(x * h)))
    maze = cv2.cvtColor(maze, cv2.COLOR_BGR2GRAY)
    threshold = custom_threshold(maze, 100)
    cv2.imshow("main", threshold)
    skeleton = skeleton(threshold)
    cv2.imshow("skel", skeleton)
    cv2.waitKey(0)


image = cv2.imread("maze.png")
process_image(image)
