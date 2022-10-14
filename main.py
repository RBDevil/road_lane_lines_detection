import matplotlib.pylab as plt
import cv2
import numpy as np

image = cv2.imread('road.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.GaussianBlur(image, (3, 3),cv2.BORDER_DEFAULT)
image = cv2.Canny(image, 70, 140)
plt.imshow(image, cmap="gray", vmin=0, vmax=255)
plt.show()