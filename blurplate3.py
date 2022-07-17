import cv2

width = 900
height = 400
##hello to check
# load the image, resize it, and convert it to grayscale
image = cv2.imread("image1.jpg")
image = cv2.resize(image, (width, height))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("input",image)
# load the number plate detector
n_plate_detector = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

# detect the number plates in the grayscale image
detections = n_plate_detector.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=7)

# loop over the number plate bounding boxes
for blur in detections:
    # draw a rectangle around the number plate
    #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 2)
    #cv2.putText(image, "Number plate blured", (x - 20, y - 10),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 2)
    x, y, w, h=blur
    image[y:y+h,x:x+w]=cv2.GaussianBlur(image[y:y+h,x:x+w],(99,99),0)

    blured_plate  = image[y:y + h, x:x + w]
    # extract the number plate from the grayscale image
    number_plate = image[y:y + h, x:x + w]

    #cv2.imshow('number plate', number_plate)
    #cv2.imshow('blured plate',blured_plate)

cv2.imshow("result", image)
cv2.waitKey(0)
