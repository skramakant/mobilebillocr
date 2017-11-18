# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy
import cv2
import matplotlib 
import os
import pytesseract
from wand.image import Image
from PIL import Image as PI


# directory related info
inputDirPath = "C:/Users/Ramakant/AnacondaProjects/opencvocr/inputdata/"
preProcessDirPath = "C:/Users/Ramakant/AnacondaProjects/opencvocr/preprocessdata/"
outputDirPath = "C:/Users/Ramakant/AnacondaProjects/opencvocr/outputdata/"



# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
req_image = []
refPt = []
selectedReagon = []
cropping = False
path = 'C:/Users/Ramakant/AnacondaProjects/opencvocr/cropedImages/'
image=''
clone=''   

def input_files_to_process():
    global inputDirPath, image, clone, preProcessDirPath
    filelist = os.listdir(inputDirPath)
    for file in filelist:
        print(file)
        x = file.split(".")
        if(x[1] == "png" or x[1] == "jpg"):
            image = cv2.imread(inputDirPath+file)
            clone = image.copy()
            print("First")
            input("Press Enter to continue...")
            
        elif(x[1] == "pdf"):
            image_pdf = Image(filename= inputDirPath+file, resolution=150)
            image_jpg = image_pdf.convert('jpg')
            newfile=preProcessDirPath+x[0]+".jpg"
            image_jpg.save(filename=newfile)
            image = cv2.imread(newfile)
            clone = image.copy()
            input("Press Enter to continue...")
            


def convert_pdf_to_image(file):
    global req_image, image, clone, inputDirPath
    image_pdf = Image(filename="./billocr.pdf",resolution=400)
    image_jpeg = image_pdf.convert('png')
    image_jpeg.save(filename="billocr.png")
    image = cv2.imread("billocr.png")
    clone = image.copy()
# =============================================================================
#     for img in image_jpeg.sequence:
#         img_page = Image(image=img)
#         req_image.append(img_page.make_blob('jpeg'))
# =============================================================================
    

def coonect_sql_server(imagePath, imageData, imageName):
    import pyodbc 
    server = 'RAMAKANT-HP' 
    database = 'opencv' 
    username = 'RAMAKANT-HP\RAMAKANT' 
    password = 'ramakant' 
    #cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cnxn = pyodbc.connect(driver='{SQL Server Native Client 11.0}', 
                      host=server, database=database, trusted_connection='yes',
                      user=username, password=password)
    cursor = cnxn.cursor()
    query="select * from cropeddata"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row.imagePath + " \n" + row.imageData + " \n" + row.imageName)
        #print(row.name +' ' + row.age)
              
    cursor.execute("INSERT INTO cropeddata (imagePath,imageData,imageName) VALUES (?,?,?)",(imagePath,imageData,imageName))
    
    #cursor.execute(p)
    
    cnxn.commit()

def tesseract_ocr(filename):
    folderName = 'cropedImages';
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
    #print(pytesseract.image_to_string(PI.open('testocr.png')))
    filelist = os.listdir('./cropedImages/')
    
    print("############################################################")
    print(pytesseract.image_to_string(PI.open(folderName+'/'+filename)))
    print("############################################################")
    return pytesseract.image_to_string(PI.open(folderName+'/'+filename))
        
# =============================================================================
#     for file in filelist:
#         print("############################################################")
#         print(pytesseract.image_to_string(PI.open(folderName+'/'+file)))
#         print("############################################################")
#         return pytesseract.image_to_string(PI.open(folderName+'/'+file))
# =============================================================================
    
    
 
def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global selectedReagon, refPt, cropping
    
     # if the left mouse button was clicked, record the starting
	 # (x, y) coordinates and indicate that cropping is being
	 # performed
 
    if event == cv2.EVENT_LBUTTONDOWN and cropping == False:
        refPt = [(x, y)]
        cropping = True
 
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP and cropping == True:
        # record the ending (x, y) coordinates and indicate that
		 # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 0, 255),8)
        cv2.imshow("image",image)
        selectedReagon.append(refPt)
        refPt = []
        cropping = False
    
    elif event == cv2.EVENT_LBUTTONUP:
        cropping = False
        
    elif event == cv2.EVENT_MOUSEMOVE and cropping == True:
        cv2.rectangle(image,refPt[0],(x,y),(255,0,0),5)
        #cv2.imshow("image",image)
        
# =============================================================================
#     elif flags == cv2.EVENT_FLAG_CTRLKEY:
#         i = 0
#         for refPt in selectedReagon:
#             clone1 = clone.copy()
#             if len(refPt) == 2:
#                 roi = clone1[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
#                 cv2.imshow("ROI" + str(i), roi)
#                 cv2.waitKey(0)
#                 
#             i = i+1
# =============================================================================

      
#convert_pdf_to_image()
input_files_to_process()
    
#image = cv2.imread("testocr.png")
#clone = image.copy()

cv2.namedWindow("image",cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", 650, 750)          

cv2.setMouseCallback("image", click_and_crop)
#cv2.imshow("image",image)
# =============================================================================
# while True:
#     cv2.imshow("image",image)
#     if cv2.waitKey(20) & 0xFF == 27:
#         break;
# =============================================================================

# keep looping until the 'q' key is pressed
while True:

    # display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF
     
    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        
    	 image = clone.copy()
     
    # if the 'c' key is pressed, break from the loop
    if(key == ord("c")):
        i=0
        for refPt in selectedReagon:
            clone1 = clone.copy()
            if len(refPt) == 2:
                
                roi = clone1[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                creteFileName = "ROI" + str(i) + ".jpg"
                cv2.imwrite(os.path.join(path, creteFileName), roi)  
                imagePath = os.path.join(path, creteFileName)
                imageData = tesseract_ocr(creteFileName) 
                imageName = "billocr"
                
                coonect_sql_server(imagePath,imageData,imageName)
                #cv2.imshow("ROI" + str(i), roi)
                #cv2.waitKey(0)
            i=i+1
              
        break     
    if(key == ord("d")):
        break;

# if there are two reference points, then crop the region of interest
# from the image and display it
# =============================================================================
# for refPt in selectedReagon:
#     i = 0
#     clone1 = clone.copy()
#     if len(refPt) == 2:
#         roi = clone1[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
#         cv2.imshow("ROI" + str(i), roi)
#         i = i+1
#         cv2.waitKey(0)
# =============================================================================



     
cv2.waitKey(0)
cv2.destroyAllWindows()
# cv2.setMouseCallback("image", click_and_crop)