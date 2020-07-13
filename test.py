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
                    continue
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


def neighbors(x, y, img):
    l, r, t, b = x-1, x+1, y-1, y+1
    return [img[t, x], img[t, r], img[y, r], img[b, r], img[b, x], img[b, l], img[y][l], img[t][l]]


def has_transitions(neighbors):
    n = neighbors + neighbors[0:1]
    tran = sum((a, b) == (255, 0) for a, b in zip(n, n[1:]))

    return tran == 1


def zhang_suen(img):
    (h, w) = img.shape
    remove = remove2 = [100]
    copy = img.copy()
    while remove or remove2:
        remove = []
        for y in range(1, h-1):
            for x in range(1, w-1):
                if copy[y][x] == 0:
                    n = neighbors(x, y, copy)
                    if (2 <= sum(n)//255 <= 6 and
                        has_transitions(n) and
                        n[2]*n[4]*n[6] == 0 and
                            n[0]*n[2]*n[4] == 0):
                        remove.append((x, y))
        for x, y in remove:
            copy.itemset((y, x), 255)

        remove2 = []
        for y in range(1, h-1):
            for x in range(1, w-1):
                if copy[y][x] == 0:
                    n = neighbors(x, y, copy)
                    if (2 <= sum(n)//255 <= 6 and
                        has_transitions(n) and
                        n[0]*n[4]*n[6] == 0 and
                            n[0]*n[2]*n[6] == 0):
                        remove2.append((x, y))
        for x, y in remove2:
            copy.itemset((y, x), 255)
    return copy


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
    (h, w) = maze.shape

    if background_color(maze) == 0:
        maze = cv2.bitwise_not(maze)

    #threshold = custom_threshold(maze, 150)
    t, threshold = cv2.threshold(maze, 225, 255, cv2.THRESH_BINARY)

    cv2.imshow("main", threshold)
    cv2.imwrite("thresh.png", threshold)

    skel = zhang_suen(threshold)
    #skel = skeletonize(threshold)
    cv2.imshow("skeletonized", skel)

    cv2.waitKey(0)


img0 = cv2.imread('test.png', 0)
img1 = cv2.imread('color_maze.png', 0)
img2 = cv2.imread('tc_maze.png', 0)
process_image(img0)
