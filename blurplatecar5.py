import cv2
import imutils
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'tesseract.exe'
image = cv2.imread('image6.jpg')
image = imutils.resize(image, width=600,height=600 )
cv2.imshow("original image", image)

#Converting the input image to greyscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("greyed image", gray_image)
gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
#cv2.imshow("smoothened image", gray_image)


edged = cv2.Canny(gray_image, 30, 200)
#cv2.imshow("edged image", edged)


cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
image1=image.copy()
cv2.drawContours(image1,cnts,-1,(0,255,0),3)
#cv2.imshow("contours",image1)

cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
screenCnt = None
image2 = image.copy()
cv2.drawContours(image2,cnts,-1,(0,255,0),3)
#cv2.imshow("Top 30 contours",image2)


i=7
for c in cnts:
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
    if len(approx) == 4:
        screenCnt = approx

    x,y,w,h = cv2.boundingRect(c)
    #cv2.imshow('plate',image[y:y+h,x:x+w])
    image[y:y+h,x:x+w]=cv2.GaussianBlur(image[y:y+h,x:x+w],(99,99),0)
    new_img=image[y:y+h,x:x+w]
    #cv2.imwrite('./'+str(i)+'.png',new_img)
    i+=1
    break
    #plate = pytesseract.image_to_string(new_img, lang='eng')

#cv2.imshow('plate',new_img)
#cv2.imshow('output',bluring)
cv2.imshow('result',image)
cv2.waitKey(0)