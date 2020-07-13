import cv2
import argparse

image = cv2.imread("maze.png")
(h, w, d) = image.shape
#cv2.imshow("Test", image)
snip = image[0:24, 0:24]
#cv2.imshow("snip", snip)
resize = cv2.resize(image, (w//2, h//2))
#cv2.imshow("resize", resize)
gaussian_kernel = (11, 11)
blur = cv2.GaussianBlur(image, gaussian_kernel, 0)
#cv2.imshow("blur", blur)
output = image.copy()
cv2.line(output, (5, 50), (55, 50), (255, 0, 0), 3)
output[5, 100] = [0, 255, 0]
cv2.imshow("output", output)

#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="path to input image")
#args = vars(ap.parse_args())
#image = cv2.imread(args["image"])
#cv2.imshow("Test", image)

image = cv2.imread("maze.png")
color_image = cv2.imread("color_maze.png")
color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("ok", image)
thin_edge = cv2.Canny(image, 235, 10)
#cv2.imshow("ok2", thin_edge)

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
threshold = cv2.adaptiveThreshold(
    image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 5, 20)
#cv2.imshow("ok2", threshold)
cv2.waitKey(0)
