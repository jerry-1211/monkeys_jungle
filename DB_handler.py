import json
from datetime import datetime, timedelta
import os
import shutil
import pandas as pd


from pymongo import MongoClient


class DBModule : 
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.db = client.monkeys
        self.user_collection = self.db.users

    def signin(self,name,userId,pwd,phoneNumber,mbti,answerQ1,answerQ2,answerQ3,answerQ4,answerQ5,answerQ6,answerQ7,answerQ8,answerQ9,answerQ10,):
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
