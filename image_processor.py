from turtle import right
import cv2
import numpy as np
import matplotlib as plt

def region_of_interest(image, vertices):
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

def sort_lines_by_side(line_vectors):
    left_lines = []
    right_lines = []

    for line in line_vectors:
        for x1, y1, x2, y2 in line:
            vx = x1 - x2
            vy = y1 - y2
            print(vx, vy)
            if ((vx > 0 and vy > 0) or (vx < 0 and vy < 0)):
                left_lines.append([[x1, y1, x2, y2]])
            else:
                if ((vx < 0 and vy > 0) or (vx > 0 and vy < 0)):
                    right_lines.append([[x1, y1, x2, y2]])

    print('left lines:')
    print(left_lines)
    print('right_lines:')
    print(right_lines)
    return left_lines, right_lines

def average_lines(line_vectors):
    x1_sum = 0
    y1_sum = 0
    x2_sum = 0
    y2_sum = 0

    for line in line_vectors:
        for x1, y1, x2, y2 in line:
            x1_sum += x1
            y1_sum += y1
            x2_sum += x2
            y2_sum += y2

    if (len(line_vectors) != 0):
        x1_avg = round(x1_sum / len(line_vectors))
        y1_avg = round(y1_sum / len(line_vectors))
        x2_avg = round(x2_sum / len(line_vectors))
        y2_avg = round(y2_sum / len(line_vectors))
    else:
        return [[0,0,0,0]]
    return [[x1_avg, y1_avg, x2_avg, y2_avg]]

def process_image(image):
    original_image = np.copy(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (3, 3),cv2.BORDER_DEFAULT)
    image = cv2.Canny(image, 70, 140)

    height = image.shape[0]
    width = image.shape[1]

    region_of_interest_vertices = [
        (0 + width/6, height), 
        (width/2, height/3 * 2),
        (width - width/6, height)
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

    left_lines, right_lines = sort_lines_by_side(lines)
    left_line = average_lines(left_lines)
    right_line = average_lines(right_lines)

    return draw_lines(original_image, [left_line, right_line])
    #return draw_lines(original_image, lines)