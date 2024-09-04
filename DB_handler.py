import json
from datetime import datetime, timedelta
import os
import shutil
import pandas as pd
from bson import ObjectId

from pymongo import MongoClient


class DBModule :
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.db = client.monkeys
        self.user_collection = self.db.users  # 사용자 정보를 저장하는 컬렉션
        self.post_collection = self.db.posts  # 게시물 정보를 저장하는 컬렉션
        self.messages_collection = self.db.messages # 채팅 내역 저장
        
    def objectid_to_dict(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        raise TypeError("Object of type ObjectId is not JSON serializable")


    def signin(self,name,userId,pwd,phoneNumber,mbti,answerQ1,answerQ2,answerQ3,answerQ4,answerQ5,answerQ6,answerQ7,answerQ8,answerQ9,answerQ10):
        informations = {
            "uName" : name,
            "userId" : userId,
            "pwd" : pwd,
            "phoneNumber" : phoneNumber,
            "MBTI" : mbti,
            "q1" : answerQ1,
            "q2" : answerQ2,
            "q3" : answerQ3,
            "q4" : answerQ4,
            "q5" : answerQ5,
            "q6" : answerQ6,
            "q7" : answerQ7,
            "q8" : answerQ8,
            "q9" : answerQ9,
            "q10" : answerQ10,
        } 
        print(informations)
        self.user_collection.insert_one(informations)
    
    def findPassword(self, uid, upwd):
        uinfo = self.user_collection.find_one({'userId': uid})
        
        # 사용자 정보가 없는 경우
        if uinfo is None:
            return None  # 사용자 없음
        
        # 비밀번호가 일치하지 않는 경우
        if upwd != uinfo["pwd"]:
            return True  # 비밀번호 오류
        
        # 비밀번호가 일치하는 경우
        return False  # 인증 성공
    
    
    # 질문 저장
    def card_info(self,title,content,status, userId):
        informations = {
            "title" : title,
            "content" : content,
            "status" : status,
            "userId" : userId
            
            
        }
        self.post_collection.insert_one(informations)

    def uploadCard(self):
        results = list(self.post_collection.find({}))
        for result in results:
            result["_id"] = str(result["_id"] )
        return results
    
    def existing_card(self,info):
        return self.post_collection.find_one(info)

    # chat방에서 PID로 계시글 정보 가져오기 
    def get_post_info(self,pid):
        
        pid = ObjectId(pid)
        pinfo = self.post_collection.find_one({"_id":pid})
        
        info = {
            # "id" : pinfo["id"]
            "title" : pinfo["title"],
            "content" : pinfo["content"],
            "status" : pinfo["status"],
        }
        return info


    def message_find_room(self,room):
        results = list(self.messages_collection.find({'room': room}))
        for result in results:
            result["_id"] = str(result["_id"])
        return results

    def message_insert(self,info):
        message_id = (self.messages_collection.insert_one(info)).inserted_id
        print(message_id)
        return message_id

