import cv2
import mediapipe as mp


class faceDetector:
    
    def __init__(self, min_detection_confidence=0.5, model_selection=0):

        self.mp_face_detection = mp.solutions.mediapipe.python.solutions.face_detection
        self.face = self.mp_face_detection.FaceDetection(min_detection_confidence, model_selection)
        self.mp_draw = mp.solutions.mediapipe.python.solutions.drawing_utils

    def detect(self, img, draw=True, write=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.face.process(img_rgb)
        bboxs = []
        if self.results.detections:
            h, w, c = img.shape
            for id, detection in enumerate(self.results.detections):
                bbox_c = detection.location_data.relative_bounding_box
                bbox = int(bbox_c.xmin * w), int(bbox_c.ymin * h), int(bbox_c.width * w), int(bbox_c.height * h)
                bboxs.append((id, bbox, detection.score[0]))
                if draw:
                    cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 0), 2)
                    cv2.putText(img, f"{int(detection.score[0] * 100)}%", (bbox[0], bbox[1] - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        if write:
            cv2.imwrite("output/detected_output.jpg", img)
            print("face detection image saved!")

        return img, bboxs


def main():

    cap = cv2.VideoCapture(1)
    face_detector = faceDetector(min_detection_confidence=0.5)

    while True:
        success, img = cap.read()

        img, bboxs = face_detector.detect(img, write=False)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
