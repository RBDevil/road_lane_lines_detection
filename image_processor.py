import cv2
import numpy as np

def region_of_interest(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)
    image = cv2.bitwise_and(image, mask)
    return image

def draw_lines(image, line_vectors):
    lines_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

    for line in line_vectors:
        for x1, y1, x2, y2 in line:
            cv2.line(lines_image, (x1, y1), (x2, y2), (0, 255, 0), thickness=5)
    
    image = cv2.addWeighted(image, 0.8, lines_image, 1, 0.0)
    return image

def sort_lines_by_side(line_vectors):
    left_lines = []
    right_lines = []

    for line in line_vectors:
        for x1, y1, x2, y2 in line:
            a, b = create_line(x1, y1, x2, y2)
            if (a < 0):
                left_lines.append([a, b])
            else:
                if (a > 0):
                    right_lines.append([a, b])

    return left_lines, right_lines

def average_lines(line_vectors):
    sum_a = 0
    sum_b = 0

    for line in line_vectors:
        for a, b in line:
            sum_a += a
            sum_b += b

    count = len(line_vectors[0])
    if (count != 0):
        return sum_a / count, sum_b / count
    else:
        return 0, 0

def create_line(x1, y1, x2, y2):
    if (x2 != x1):
        a = (y2 - y1) / (x2 - x1)
        b = (x2 * y1 - x1 * y2) / (x2 - x1)
        return a, b
    else:
        return 0, 0

def get_points_from_line(a, b, image):
    height = image.shape[0]

    if (a != 0):
        y1 = height
        x1 = (y1 - b) / a

        y2 = height / 20 * 13
        x2 = (y2 - b) / a

        return [round(x1), round(y1), round(x2), round(y2)]

    else:
        return [0,0,0,0]

def create_line(x1, y1, x2, y2):
    if (x2 != x1):
        a = (y2 - y1) / (x2 - x1)
        b = (x2 * y1 - x1 * y2) / (x2 - x1)
        return a, b
    else:
        return 0, 0    

def process_image(image, previous_left_line, previous_right_line):
    original_image = np.copy(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (3, 3),cv2.BORDER_DEFAULT)
    image = cv2.Canny(image, 70, 140)

    height = image.shape[0]
    width = image.shape[1]

    region_of_interest_vertices = [
        (width/5, height), 
        (width*2/5, height/3*2),
        (width*3/5, height/3*2),
        (width - width*1/5, height)
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

    a, b = average_lines([left_lines])
    if (a != 0 and b != 0):
        previous_left_line = [a, b]
        left_line = get_points_from_line(a, b, image)
    else:
        left_line = get_points_from_line(previous_left_line[0], previous_left_line[1], image)
    
    a, b = average_lines([right_lines])
    if (a != 0 and b != 0):
        previous_right_line = [a, b]
        right_line = get_points_from_line(a, b, image)
    else:
        right_line = get_points_from_line(previous_right_line[0], previous_right_line[1], image)
    
    return draw_lines(original_image, [[left_line, right_line]]), previous_left_line, previous_right_line