import cv2
import face_detector as fd
import stitcher
import os

# TODO 1. Create stitcher class
# TODO 2. Try using stitcher to stitch several images together with both panorama mode and scan mode
# TODO 3. Implement opencv to capture images at an interval
# TODO 4. Calculate pixel apart of the players to get the distance and degree of turning for the robot
# TODO 5. Implement hand gestures

POSTPROCESSING = False

cap = cv2.VideoCapture(1)
file_directory = "C:/Users/Kridbhume Chammanard/Desktop/Robotic Project I"
image_directory = "C:/Users/Kridbhume Chammanard/Desktop/Robotic Project I/images"
img_path = "images/*.jpg"

for n in range(0, 5):
    success, img = cap.read()
    cv2.imshow(f"Image {n}", img)
    cv2.imwrite(f"images/image{n}.jpg", img)
    print(f"Image {n} saved!")
    cv2.waitKey(0) # Change delay according to interval

os.chdir(image_directory)
os.remove("image0.jpg")
os.chdir(file_directory)

image_stitcher = stitcher.Stitcher(img_path)
image_stitcher.stitch(postprocessing=POSTPROCESSING)

if POSTPROCESSING:
    stitched_img = cv2.imread("output/stitched_output_processed.jpg")
else:
    stitched_img = cv2.imread("output/stitched_output.jpg")

face_detector = fd.faceDetector(min_detection_confidence=0.5)
final_img, bboxs = face_detector.detect(stitched_img)
print(bboxs)

cv2.imshow("Final result", final_img)
cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()

