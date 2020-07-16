import numpy as np
import cv2


def skeletonize(image):
    done = False
    skeleton = image.copy()
    (h, w) = skeleton.shape
    background = 255
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


def reverse_skeleton(image):
    done = False
    skeleton = image.copy()
    (h, w) = skeleton.shape
    background = 0
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


def zhang_suen(img):
    def has_transitions(neighbors):
        n = neighbors + neighbors[0:1]
        tran = sum((a, b) == (255, 0) for a, b in zip(n, n[1:]))
        return tran == 1

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
                        n[2]+n[4]+n[6] > 0 and
                            n[0]+n[2]+n[4] > 0):
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
                        n[0]+n[4]+n[6] > 0 and
                            n[0]+n[2]+n[6] > 0):
                        remove2.append((x, y))
        for x, y in remove2:
            copy.itemset((y, x), 255)
    return copy
