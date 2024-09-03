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
        pass

    def signin(self,name,userId,pwd,phoneNumber,answerQ1,answerQ2,answerQ3,answerQ4,answerQ5,answerQ6,answerQ7,answerQ8,answerQ9,answerQ10,):
        informations = {
            "uName" : name,
            "userId" : userId,
            "pwd" : pwd,
            "phoneNumber" : phoneNumber,
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
        self.user_collection.insert_one(informations)




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