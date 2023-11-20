import os
from dotenv import load_dotenv
from fastapi import FastAPI,Form,UploadFile,File
from pydantic import BaseModel
from mysql import connector as connector
import cv2
import numpy as np
import face_recognition

load_dotenv()

cnx = connector.connect(host = os.environ['HOST'],user=os.environ['USRNAME'],passwd=os.environ['PASSWD'],database=os.environ['DBNAME'])
print(cnx)
cursor = cnx.cursor()

class userModel(BaseModel):
    email : str
    name : str

data = None

app = FastAPI()

def connectDatabase():
    global cnx
    cnx = connector.connect(host = os.environ['HOST'],user=os.environ['USRNAME'],passwd=os.environ['PASSWD'],database=os.environ['DBNAME'])

def fetchAllData():
    global data
    cursor.execute("SELECT * FROM Users")
    data = cursor.fetchall()

fetchAllData()

def byteToCroppedImage(img:bytes):
    img = cv2.imdecode(np.asarray(bytearray(img),dtype="uint8"),cv2.IMREAD_COLOR)
    grey = cv2.cvtColor(img,cv2.COLOR_BGR2BGRA)
    classifier = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
    face = classifier.detectMultiScale(grey,1.1,4)[0]
    face = img[face[1]:face[1]+face[3],face[0]:face[0]+face[2]]
    face = np.array(cv2.imencode(".jpg",face)[1])
    return face.tobytes()

@app.post("/register")
def registerUser(image : bytes = File(),email : str = Form(), name : str = Form()):
    try:
        if not image or not email or not name: 
            raise Exception("Parameters not defined !")
        image = byteToCroppedImage(image)        
        sql_inset_query = """INSERT INTO Users (email,name,image) VALUES (%s,%s,%s)"""
        sql_insert_data = (email,name,image)
        result = cursor.execute(sql_inset_query,sql_insert_data)
        cnx.commit()
        fetchAllData()
        return {"status" : 200}
    except Exception as e:
        print(e)
        return {"status" : 300, "data" : e}

@app.post("/recognize")
def recognizeUser(image : bytes = File()):
    try:
        img = cv2.imdecode(np.asarray(bytearray(image),dtype="uint8"),cv2.IMREAD_COLOR)
        images = [cv2.imdecode(np.asarray(bytearray(e[2]),dtype="uint8"),cv2.IMREAD_COLOR) for e in data]
        result = [face_recognition.compare_faces([face_recognition.face_encodings(img)[0]],face_recognition.face_encodings(e)[0],tolerance=0.4)[0] for e in images]
        print(result)
        print([e[0] for e in data])
        index = result.index(True)
        user = {"email" : data[index][0],"name" : data[index][1]}
        return {"status" : 200,"data" : user}
    except Exception as e:
        print(e)
        return {"status" : 400,"data" : "Error occured....Try again !"}

@app.get("/users")
def getUsers():
    users = [{"email" : e[0],"name":e[1]} for e in data]
    return {"status" : 200,"data" : users}

@app.delete("/users")
def deleteUser(user : userModel):
    try:
        if(not cnx.is_connected()): 
            connectDatabase()
        query = """DELETE FROM Users WHERE email = %s"""
        params = (user.email,)
        result = cursor.execute(query,params)
        print(result)
        cnx.commit()
        fetchAllData()
        return {"status" : 200}
    except Exception as e:
        print(e)
        return {"status" : 600,"data" : str(e)}

@app.put("/users")
def updateUser(user : userModel):
    try:
        if(not cnx.is_connected()): 
            connectDatabase()
        query = """UPDATE Users SET name = %s WHERE email = %s"""
        params = (user.name,user.email)
        result = cursor.execute(query,params)
        print(result)
        cnx.commit()
        fetchAllData()
        return {"status" : 200}
    except Exception as e:
        print(e)
        return {"status" : 700,"data" : str(e)}