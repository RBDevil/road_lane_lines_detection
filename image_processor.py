import cv2
import numpy as np
import matplotlib as plt

def region_of_interest(image, vertices) :
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)
    image = cv2.bitwise_and(image, mask)
    return image

def draw_lines(image, line_vectors):
    lines_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

    for line in line_vectors:
        for x1, y1, x2, y2 in line:
            cv2.line(lines_image, (x1, y1), (x2, y2), (0, 255, 0), thickness=3)
    
    image = cv2.addWeighted(image, 0.8, lines_image, 1, 0.0)
    return image

def process_image(image):
    original_image = np.copy(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (3, 3),cv2.BORDER_DEFAULT)
    image = cv2.Canny(image, 70, 140)

    height = image.shape[0]
    width = image.shape[1]

    region_of_interest_vertices = [
        (0 + width/10, height), 
        (width/2, height/2),
        (width - width/10, height)
        ]

    canny_image = region_of_interest(image, 
    np.array([region_of_interest_vertices], np.int32)
    )

    lines = cv2.HoughLinesP(
        canny_image,
        rho=6,
        theta=np.pi/60,
        threshold=160,
        lines=np.array([]),
        minLineLength=40,
        maxLineGap=25
    )
    
    return draw_lines(original_image, lines)