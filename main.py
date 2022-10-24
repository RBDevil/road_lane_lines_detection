import matplotlib.pyplot as plt
import cv2
import image_processor

video = cv2.VideoCapture('dashcam_video3.mp4')

previous_left_line = [0, 0]
previous_right_line = [0, 0]

while(video.isOpened()):
    ret, frame = video.read()
    frame, previous_left_line, previous_right_line = image_processor.process_image(
        frame, 
        previous_left_line, 
        previous_right_line
        )
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()