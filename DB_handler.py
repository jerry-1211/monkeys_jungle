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

    def signin(self,name,_id_,pwd,phoneNumber):
        informations = {
            "uname" : name,
            "pwd" : pwd,
            "phoneNumber" : phoneNumber,
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