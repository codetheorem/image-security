from typing import Optional

from fastapi import FastAPI

from fastapi import FastAPI, File, UploadFile

from fastapi.middleware.cors import CORSMiddleware

import shutil

from fastapi.responses import FileResponse

import random
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii




app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

keyPair = RSA.generate(3072)
 
pubKey = keyPair.publickey()
print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
pubKeyPEM = pubKey.exportKey()
print(pubKeyPEM.decode('ascii'))
 
print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")
privKeyPEM = keyPair.exportKey()
print(privKeyPEM.decode('ascii'))

encryptor = PKCS1_OAEP.new(pubKey)

def encrypt(file):
 fo = open(file, "rb")
 image=fo.read()
 fo.close()
 image=bytearray(image)
 key=random.randint(0,256)
 for index,value in enumerate(image):
  image[index] = value^key
 encrypted = encryptor.encrypt(image)
 fo=open("enc.jpg","wb")
 imageRes="enc.jpg"
 fo.write(image)
 fo.close()
 return (key,imageRes)

def decrypt(key,file):
 key=int(key)
 fo = open(file, "rb")
 image=fo.read()
 fo.close()
 image=bytearray(image)
 for index , value in enumerate(image):
  image[index] = value^key
 fo=open("dec.jpg","wb")
 imageRes="dec.jpg"
 fo.write(image)
 fo.close()
 return imageRes




@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/fileencrypt")
async def fileencrypt(file: UploadFile = File(...)): 
        with open(file.filename, "wb") as buffer:
          shutil.copyfileobj(file.file, buffer)
        key,image=encrypt(file.filename)
        return {"name":file.filename,"key":key,"image":image}

@app.post("/filedecrypt")
async def filedecrypt(key,file: UploadFile = File(...)):
        with open(file.filename, "wb") as buffer:
          shutil.copyfileobj(file.file, buffer)
        image=decrypt(key,file.filename)
        return {"name":file.filename,"image":image}

@app.get("/return-encfile")
def return_file():
    return FileResponse("./enc.jpg",filename="enc.jpg")

@app.get("/return-decfile")
def return_file():
    return FileResponse("./dec.jpg",filename="dec.jpg")
