from PIL import Image as imageMain
from PIL.Image import Image
import cv2
import numpy
import pytesseract
images=["image1.jpg","image3.jpg","image4.jpg"]
for image_name in images:
    imagecv=cv2.imread(image_name)
    imagecv = cv2.resize(imagecv, (900, 500))

    #imagepil=imageMain.open(imagepath)
    #imagecv=cv2.cvtColor(numpy.array(imagepil),cv2.COLOR_BGR2RGB)
    #cv2.imshow('originalimage',imagecv)
    ##contour detection work
    gray=cv2.cvtColor(imagecv,cv2.COLOR_BGR2GRAY)
    #cv2.imshow('grayscaled',gray)

    bilateral=cv2.bilateralFilter(gray,11,17,17)
    #cv2.imshow('after bilateralfilter',bilateral)
    blur=cv2.GaussianBlur(bilateral,(5,5),0)
    #cv2.imshow('after gausian blur',blur)

    edged=cv2.Canny(blur,170,200)
    #cv2.imshow('after canny edge',edged)
    contours,hierarchy=cv2.findContours(edged,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours,key=cv2.contourArea,reverse=True)[:30]
    tempContours1=cv2.drawContours(imagecv.copy(),contours,-1,(255,0,0),2)
    #cv2.imshow('Detected contours',tempContours1)


    rectanglecontours=[]
    for contour in contours:
      perimeter=cv2.arcLength(contour,True)
      approximationaccuracy=0.018*perimeter
      approximation=cv2.approxPolyDP(contour,approximationaccuracy,True)
      if len(approximation)==4:
        rectanglecontours.append(contour)
    platecontour=rectanglecontours[0]
    tempContours2=cv2.drawContours(imagecv.copy(),[platecontour],-1,(255,0,0),2)
    #cv2.imshow('detected plate contour',tempContours2)
    x,y,w,h=cv2.boundingRect(platecontour)
    plateImage=imagecv[y:y+h,x:x+w]
    #cv2.imshow('plate original',plateImage)
    plateImageBlur=cv2.GaussianBlur(plateImage,(99,99),0)
    #cv2.imshow('plate blured',plateImageBlur)
    def findmostoccurring(cvimage)->(int,int,int):
        width,height,channels=cvimage.shape
        colorCount={}
        for y in range(0,height):
            for x in range(0,width):
                BGR=(int(cvimage[x,y,0]),int(cvimage[x,y,1]),int(cvimage[x,y,2]))
                if BGR in colorCount:
                    colorCount[BGR]+=1
                else:
                    colorCount[BGR]=1
        maxcount=0
        maxBGR=(0,0,0)
        for BGR in colorCount:
            count=colorCount[BGR]
            if count>maxcount:
                maxcount=count
                maxBGR=BGR
        return maxBGR


    platebackgroundcolor=findmostoccurring(plateImageBlur)
    tempContours3=cv2.drawContours(imagecv.copy(),[platecontour],-1,platebackgroundcolor,-1)
    cv2.imshow('original image',imagecv)
    cv2.imshow('result',tempContours3)

    #Text Recognition
    #text = pytesseract.image_to_string(bilateral)
    #Draw License Plate and write the Text
    #image = cv2.rectangle(imagecv, (x,y), (x+w,y+h), (0,0,255), 3)
    #image = cv2.putText(imagecv, text, (x-100,y-50), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,255,0), 6, cv2.LINE_AA)

    #print("License Plate :", text)

    #cv2.imshow("License Plate Detection",image)
    cv2.waitKey(5000)
