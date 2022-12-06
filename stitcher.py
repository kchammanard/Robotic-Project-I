import cv2
import glob
import imutils
import numpy as np

PATH = "C:/Users/Kridbhume Chammanard/Desktop/Robotic Project I/images/*.jpg"


class Stitcher:

    def __init__(self, input_path):

        self.image_stitcher = cv2.Stitcher_create()  
        image_paths = glob.glob(input_path)
        self.images = []

        for image in image_paths:
            img = cv2.imread(image)
            #img = cv2.resize(img, (0, 0), fx = 0.1, fy = 0.1)
            self.images.append(img)
            # cv2.imshow("Image", img) # To display those images
            cv2.waitKey(0) # Wait until key press
    
    def stitch(self, postprocessing=True):

        self.error, self.stitched_img = self.image_stitcher.stitch(self.images)

        if not self.error:
            cv2.imwrite("output/stitched_output.jpg", self.stitched_img)
            cv2.imshow("Stitched Image", self.stitched_img)
            cv2.waitKey(0)
            print("Stitched image output saved!")

            if postprocessing:
                self.stitched_img = cv2.copyMakeBorder(self.stitched_img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))
                cv2.imshow("W/ border", self.stitched_img)
                cv2.waitKey(0)

                gray = cv2.cvtColor(self.stitched_img, cv2.COLOR_BGR2GRAY)
                thresh_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
                cv2.imshow("Threshold Image", thresh_img)
                cv2.waitKey(0)

                contours = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours = imutils.grab_contours(contours)
                area_of_interest = max(contours, key=cv2.contourArea)

                mask = np.zeros(thresh_img.shape, dtype="uint8")
                x, y, w, h = cv2.boundingRect(area_of_interest)
                cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

                min_rect = mask.copy()
                sub = mask.copy()

                while cv2.countNonZero(sub) > 0:
                    min_rect = cv2.erode(min_rect, None)
                    sub = cv2.subtract(min_rect, thresh_img)

                contours = cv2.findContours(min_rect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours = imutils.grab_contours(contours)
                area_of_interest = max(contours, key=cv2.contourArea)
                cv2.imshow("Min Rectangle", min_rect)
                cv2.waitKey(0)

                x, y, w, h = cv2.boundingRect(area_of_interest)
                self.stitched_img = self.stitched_img[y:y + h, x:x + w]

                cv2.imwrite("output/stitched_output_processed.jpg", self.stitched_img)
                cv2.imshow("Processed Image", self.stitched_img)
                cv2.waitKey(0)

        else:
            print("Image can't be stitched, not enough keypoints detected.")
        

            
def main():

    image_stitcher = Stitcher(PATH)
    image_stitcher.stitch(postprocessing=True)

if __name__ == "__main__":
    main()