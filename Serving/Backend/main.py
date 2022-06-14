from datetime import datetime
from imaplib import _Authenticator
from fastapi import FastAPI, UploadFile, File, Body, status, Depends, Form

from fastapi.responses import FileResponse, Response
from fastapi.requests import Request
from fastapi.param_functions import Depends
from fastapi.middleware.cors import CORSMiddleware

import os, secrets
from typing import Optional, List
from requests import Response
import uvicorn
from uuid import UUID, uuid4

from hanspell import spell_checker
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from urllib.parse import quote

## 내부 모듈 호출
from db.models import InputForm, InputFormDB, StoryInfo
from api.generate_text import generate_model
from cyclegan.inference import start_inference
from api.resize_image import resizing
from pymongo import MongoClient
import pymongo

import shutil
import base64


## DB 호출
my_client = MongoClient(host= "YOUR_HOSTNUM" , port= "YOUR_PORT" , username= "YOUR_USERNAME" , password= "YOUR_PASSWORD" )
app = FastAPI()
mydb = my_client["YOUR_DB_NAME"] # DB 이름
mycollection = mydb["YOUR_COLLECTION_NAME"] # Collection 이름



async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception :
        return Response("Internal server error", status_code=500)


app.middleware('http')(catch_exceptions_middleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {'message' : 'Hello'}
 
from cyclegan.inference import change_image
@app.post("/submit", response_description = "submit", tags=["결과"])
async def create_submit(author : str = Form(...), title : str = Form(...) , text : str = Form(...),file : Optional[UploadFile] = File(None)) :
    if mycollection.count():
        ind = mycollection.find_one(sort=[( '_id', pymongo.DESCENDING )])['ind']
    else : ind = 0
    ind +=1
    result = {}
    if not file :
        result ={}
        story_id =  uuid4().hex 
        result = {'ind' : ind, 'title': title, "author" : author , "text": text}
        result_ = {'ind' : ind, 'title': title, "author" : author , "text": text}
        try:
            mycollection.insert_one(result)
        except:
            print( "insert failed", sys.exc_info()[0])
        return result_
    else :
        file_ = file
        result ={}
        story_id = ""       
        UPLOAD_DIRECTORY = "./static/images/original/" # 업로드 이미지 저장 경로
        CHG_DIRECTORY = "./static/images/changed/" # 변경 이미지 저장 경로
        story_id = uuid4().hex	    
        org_file_name = ''.join([story_id,'.png'])
        chg_file_name =''.join([story_id,'.png']) 
        file_location = os.path.join(UPLOAD_DIRECTORY,org_file_name)

        tmp_pth = "./static/temp/"
        chg_file_location = os.path.join(tmp_pth, chg_file_name)

        # original image 저장
        with open(file_location, "wb+") as file_object:
	        file_object.write(file.file.read())
        file_object.close()	
        
        # temp폴더안 파일 모두 지우기 
        if os.path.exists("./static/temp/"):
            for fi in os.listdir("./static/temp/"):
                os.remove("./static/temp/" + fi)
        #original image temp로 커피
        shutil.copyfile(file_location,chg_file_location)
        resizing()
        # 이미지 변환 모델 cycle gan
        start_inference(story_id)
  

        org_file_url= UPLOAD_DIRECTORY+org_file_name
        chg_file_url = CHG_DIRECTORY + org_file_name

        result = { 'ind' : ind,'org_file_url' :org_file_url, 'chg_file_url': chg_file_url , 'title': title, "author" : author ,"text": text}
        result_ = { 'ind' : ind, 'org_file_url' :org_file_url, 'chg_file_url': chg_file_url , 'title': title, "author" : author ,"text": text}
        ###### chg_file_url을 base64 인코딩한 파일로 바꿈 ######
    
        with open(result_['chg_file_url'], 'rb') as f:
            base64image = base64.b64encode(f.read())
            f.close()
        try :
            mycollection.insert_one(result)
        except :
            print( "insert failed", sys.exc_info()[0])
        return {**result_, "chg_file_bs64" : base64image}

# 사용자 입력 맞춤법 검사
@app.post('/spellcheck', response_description = "dict 형식의 사용자 입력 문장 맞춤법 결과 반환", tags=["글"])
def spellcheck(data : str = Form(...)):
    checked_sentence = spell_checker.check(data)
    checked_sentence.as_dict()
    return checked_sentence[2]


# 문장 생성하기
@app.post('/predict',  tags=["글"])
def predict(result : str = Form(...), data : str = Form(...), sentence_count : int = Form(...) , temperature : float = Form(...), repetition : float = Form(...), grammar_check : bool = Form(...)):
    text_list =[]

    if grammar_check :
        data = spell_checker.check(data)[2]
        return generate_model(data, sentence_count, temperature, repetition)
    else :
        return generate_model(data, sentence_count, temperature, repetition)
    return dictionary


##전체 데이터 베이스 개수 return
@app.get('/tales', tags=["글"])
async def tales() :
    try :
        return mycollection.count()
    except :
        return print("DB Empty")

# 이야기 하나씩 가져오기
IMG_DIRECTORY = "./static/images/original/"
@app.get('/tales/{id}',  tags=["글"])
async def find_story(id : int ) :
    try:
        result ={}
        list_of_story =mycollection.find({'ind' : id})
        for story in list_of_story :
            result['author']= story['author']
            result['text'] =story['text']
            result['title']= story['title']
            result['chg_img_url'] = story.get('chg_file_url', None)

            if result['chg_img_url'] :
                with open(result['chg_img_url'], 'rb') as f:
                    base64image = base64.b64encode(f.read())
                f.close()
                return {**result, "chg_img_bs64" : base64image}
            
        if not result :
            return  {"message" : "No tale Num : " + str(id)} 
        else : return result
    except :
        return {"message" : "Something Wrong"} 
    return result

if __name__ == "__main__" :
	uvicorn.run('main:app', host = '0.0.0.0', port ="YOURPORT",  reload=True, workers =2)