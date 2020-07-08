import cv2
import numpy as np


def background_color(image):
    unique_array, counts = np.unique(image, return_counts=True)
    return unique_array[counts.argmax()]


def skeletonize(image):
    done = False
    skeleton = image.copy()
    (h, w) = skeleton.shape
    background = background_color(skeleton)
    not_background = 255-background
    while not(done):
        done = True
        for x in range(h):
            for y in range(w):
                if skeleton[x, y] == background:
                    pass
                else:
                    r = l = t = b = -1
                    if x in range(1, h-1):
                        t = skeleton[x-1, y]
                        b = skeleton[x+1, y]
                    if y in range(1, w-1):
                        l = skeleton[x, y-1]
                        r = skeleton[x, y+1]

                    if r == l and r == background:
                        if t == b and r == t:
                            skeleton[x, y] = background
                        else:
                            continue
                    elif t == b and t == background:
                        continue
                    skeleton[x, y] = background
                    done = False
    return skeleton


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

    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    threshold = cv2.dilate(threshold, element)

    cv2.imshow("main", threshold)
    cv2.imwrite("thresh.png", threshold)
    skeleton = skeletonize(threshold)
    cv2.imshow("skel", skeleton)
    cv2.imwrite("skel.png", skeleton)
    cv2.waitKey(0)


image = cv2.imread("maze.png")
process_image(image)
