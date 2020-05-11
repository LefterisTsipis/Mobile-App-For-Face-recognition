import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
import cv2
print('ok')
import os
import json
import mysql.connector
#from flask import Flask,request,Response 
import uuid
import time

def faceDetectionFirstLevel(test_img):
    gray_img= cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)
    face_haar_cascade=cv2.CascadeClassifier('DATA/haarcascades/haarcascade_frontalface_default.xml')
    faces=face_haar_cascade.detectMultiScale(gray_img,scaleFactor=1.45,minNeighbors=5)
    return faces,gray_img


def label_for_training_data(directory):
    faces=[]
    faceID=[]
 #path=4 paths,
 #subdirnames= the folders in the main directory,
 #filenames=the files in te folders 
    for path,subdirnames,filenames in os.walk(directory):
        for filename in filenames:
            if filename.startswith("."):
                print("skiping system file")
                continue
            id=os.path.basename(path)#0 or 1 the names of subfolders 
            img_path=os.path.join(path,filename)#DATA/lefteris_faces/trainingImages\0 + img.png
            print("img_path : ",img_path)# for example DATA/lefteris_faces/trainingImages\0\0.png
            print("id : ",id) #0
            test_img=cv2.imread(img_path)#read the image
            if test_img is None:#check the reading
                print("Image not loaded properly")
                continue
            if id!='0' and id!='1' and id!='2' and id!='3' and id!='4' and id!='5' and id!='6':
                print("errr")
                continue
            #facedetection retern the cordination and the image
            faces_rect,gray_img=faceDetectionFirstLevel(test_img)
            if len(faces_rect)!=1:
                continue
            (x,y,w,h)=faces_rect[0]#take the cordinations
            roi_gray=gray_img[y:y+w,x:x+h]#take the rigion of interest
            faces.append(roi_gray)#create the array of faces
            faceID.append(int(id))##create the array of IDs
    return faces,faceID


def train_classifier(faces,faceID):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()#create the model 
    face_recognizer.train(faces,np.array(faceID))#train the model 
    return face_recognizer#return the model 


def draw_rect(test_img,face):
    (x,y,w,h)=face
    cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=10)
    
def put_text(test_img,text,x,y):
    cv2.putText(test_img,text,(x+20,y+20),cv2.FONT_HERSHEY_DUPLEX,1,(255,0,0),1)

faces,faceID=label_for_training_data('DATA/lefteris_faces/trainingImages')   
face_recognizer= train_classifier(faces,faceID)  

def faceRecognize(faces_detected):
    test1_img,gray_img=faceDetectionFirstLevel(faces_detected)
    for face in test1_img:
        (x,y,w,h)=face
        roi_gray=gray_img[y:y+w, x:x+h]
        label,confidence=face_recognizer.predict(roi_gray)#predicting the label of given image
        print("confidence:",confidence)
        print("label:",label)
        if confidence>80:
            ImageBelonge='Alert'
            print('cannot recognize')
        else:
            if label==0:
                ImageBelonge='gregoris'
                print('the face belong to gregoris')
            if label==1 :
                ImageBelonge='lefteris'
                print('the face belong to lefteris') 
            if label==2 :
                ImageBelonge='Marios'
                print('the face belong to Marios') 
            if label==3:
                ImageBelonge='Chris'
                print('the face belong to Chris') 
            if label==4:
                ImageBelonge='Lena'
                print('the face belong to Maria')  
            if label==5:
                ImageBelonge='Argirw'
                print('the face belong to Argirw')  
            if label==6:
                ImageBelonge='Takis'
                print('the face belong to Takis')  
    
    return ImageBelonge           

def faceDetection(test_img):
    #test1_img,gray_img= faceDetectionFirstLevel(test_img)
    predicted_name=faceRecognize(test_img)
    predicted_name# take the name of the human whos belonge the face
    face_haar_cascade=cv2.CascadeClassifier('DATA/haarcascades/haarcascade_frontalface_default.xml')
    gray_img= cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)
    faces=face_haar_cascade.detectMultiScale(gray_img,scaleFactor=1.45,minNeighbors=5)
    for (x,y,w,h) in faces:
        img=cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=5)
    path_file=('C:/Users/LETERIS/Desktop/FaceRecognition/testData/%s.jpg'%uuid.uuid4().hex)
    path_file
    put_text(img,predicted_name,x,y)
    cv2.imwrite(path_file,img)
    return predicted_name,img

import mysql.connector


config = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1',
  'database': 'imageuploadapp',
  'raise_on_warnings': True
}


connection = mysql.connector.connect(**config)
print(connection)

cursor = connection.cursor()

query ="SELECT max(id) FROM image_info"
cursor.execute(query) 
result = cursor.fetchall()
last_image=result[0][0]
print(result[0][0])

sql = "SELECT path FROM image_info WHERE id = %s"
cursor.execute(sql, result[0])
myresult = cursor.fetchall()
print(myresult[0][0])

test1_img=cv2.imread(myresult[0][0])
test1_img=cv2.cvtColor(test1_img,cv2.COLOR_BGR2RGB)
plt.imshow(test1_img)
#test1_img=cv2.imread('DATA/lefteris_faces/trainingImages/0/58.jpg')
name,img=faceDetection(test1_img)
print(name)
plt.imshow(img)



if name=="gregoris":
    sql = "UPDATE image_info SET prediction = 'gregoris' WHERE id = %s"
    cursor.execute(sql,result[0])
    connection.commit()
    print(cursor.rowcount, "record(s) affected")
if name=="lefteris":
    sql = "UPDATE image_info SET prediction = 'lefteris' WHERE id = %s"
    cursor.execute(sql,result[0])
    connection.commit()
    print(cursor.rowcount, "record(s) affected")
if name=="Takis":
    sql = "UPDATE image_info SET prediction = 'Takis' WHERE id = %s"
    cursor.execute(sql,result[0])
    connection.commit()
    print(cursor.rowcount, "record(s) affected")    
if name=="Chris":
    sql = "UPDATE image_info SET prediction = 'Chris' WHERE id = %s"
    cursor.execute(sql,result[0])
    connection.commit()
    print(cursor.rowcount, "record(s) affected")
if name=="Lena":
    sql = "UPDATE image_info SET prediction = 'Lena' WHERE id = %s"
    cursor.execute(sql,result[0])
    connection.commit()
    print(cursor.rowcount, "record(s) affected")
if name=="Argirw":
    sql = "UPDATE image_info SET prediction = 'Argirw' WHERE id = %s"
    cursor.execute(sql,result[0])
    connection.commit()
    print(cursor.rowcount, "record(s) affected")
if name=="Marios":
    sql = "UPDATE image_info SET prediction = 'Marios' WHERE id = %s"
    cursor.execute(sql,result[0])
    connection.commit()
    print(cursor.rowcount, "record(s) affected")
x=3
flag=1
while x>0:
    connection = mysql.connector.connect(**config)
    print(connection)
    cursor = connection.cursor()
    new_query ="SELECT max(id) FROM image_info"
    cursor.execute(query) 
    result = cursor.fetchall()
    new_imamge=result[0][0]
        
    if new_imamge==last_image:
        flag=1
    if new_imamge!=last_image:
         flag=2
    if flag==1:
        time.sleep(2)
        print("wait for new image")
        print(new_imamge)
    if flag==2:
        sql = "SELECT path FROM image_info WHERE id = %s"
        cursor.execute(sql, result[0])
        myresult = cursor.fetchall()
        print(myresult[0][0])
        last_image=new_imamge
        flag=1
        test1_img=cv2.imread(myresult[0][0])
        test1_img=cv2.cvtColor(test1_img,cv2.COLOR_BGR2RGB)
        plt.imshow(test1_img)
        #test1_img=cv2.imread('DATA/lefteris_faces/trainingImages/0/58.jpg')
        name,img=faceDetection(test1_img)
        print(name)
        plt.imshow(img)
        if name=="gregoris":
            sql = "UPDATE image_info SET prediction = 'gregoris' WHERE id = %s"
            cursor.execute(sql,result[0])
            connection.commit()
            print(cursor.rowcount, "record(s) affected")
        if name=="lefteris":
            sql = "UPDATE image_info SET prediction = 'lefteris' WHERE id = %s"
            cursor.execute(sql,result[0])
            connection.commit()
            print(cursor.rowcount, "record(s) affected")
        if name=="Takis":
            sql = "UPDATE image_info SET prediction = 'Takis' WHERE id = %s"
            cursor.execute(sql,result[0])
            connection.commit()
            print(cursor.rowcount, "record(s) affected")    
        if name=="Chris":
            sql = "UPDATE image_info SET prediction = 'Chris' WHERE id = %s"
            cursor.execute(sql,result[0])
            connection.commit()
            print(cursor.rowcount, "record(s) affected")
        if name=="Lena":
            sql = "UPDATE image_info SET prediction = 'Lena' WHERE id = %s"
            cursor.execute(sql,result[0])
            connection.commit()
            print(cursor.rowcount, "record(s) affected")
        if name=="Argirw":
            sql = "UPDATE image_info SET prediction = 'Argirw' WHERE id = %s"
            cursor.execute(sql,result[0])
            connection.commit()
            print(cursor.rowcount, "record(s) affected")
        if name=="Marios":
            sql = "UPDATE image_info SET prediction = 'Marios' WHERE id = %s"
            cursor.execute(sql,result[0])
            connection.commit()
            print(cursor.rowcount, "record(s) affected")
        
   

      
        


    
