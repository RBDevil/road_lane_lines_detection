import matplotlib.pyplot as plt
import cv2
import image_processor

video = cv2.VideoCapture('dashcam_video4.mp4')

while(video.isOpened()):
    ret, frame = video.read()
    frame = image_processor.process_image(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()