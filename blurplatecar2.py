import cv2
import numpy
width=900
height=400
plate_cascade=cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
images=["image5.jpg",'image6.jpg']
for image_name in images:
    img=cv2.imread(image_name)
    img = cv2.resize(img, (width, height))
    cv2.imshow("input",img)
    plate = plate_cascade.detectMultiScale(img,scaleFactor=1.06,minNeighbors=7)
    for  blur in plate:
        x,y,w,h=blur

        img[y:y+h,x:x+w]=cv2.GaussianBlur(img[y:y+h,x:x+w],(99,99),0)
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imshow("output",img)

    cv2.waitKey(5000)
