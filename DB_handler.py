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
    
    def signin(self,name,_id_,pwd,phoneNumber):
        informations = {
            "uname" : name,
            "pwd" : pwd,
            "phoneNumber" : phoneNumber,
        } 
        self.user_collection.insert_one(informations)


    # 질문 저장
    def card_info(self,title,content,status):
        informations = {
            "title" : title,
            "content" : content,
            "status" : status
        }
        self.post_collection.insert_one(informations)

    def uploadCard(self):
        results = list(self.post_collection.find({}))
        for result in results:
            result["_id"] = str(result["_id"] )
        return results
    
    def existing_card(self,info):
        return self.post_collection.find_one(info)

        

    def message_find_room(self,room):
        results = list(self.messages_collection.find({'room': room}))
        for result in results:
            result["_id"] = str(result["_id"])
        return results

    def message_insert(self,info):
        message_id = (self.messages_collection.insert_one(info)).inserted_id
        print(message_id)
        return message_id
    





        # if self.signin_verification(_id_):
            
        #     return True
        # else :
        #     return False
        
    # def signin_verification(self,uid):
    #     users = self.db.child("users").get().val()
    #     for i in users:
    #         if uid == i :
    #             return False
    #     return True

    # def login(self,uid,pwd):
    #         users = self.db.child("users").get().val()
    #         try : 
    #             userinfo = users[uid]
    #             if userinfo["pwd"] == pwd :
    #                 return True
    #             else :
    #                 return False 
    #         except :
    #             return False