import time
import datetime
import os
import cv2
import numpy as np


from flask import Flask,redirect,render_template,url_for,jsonify
from flask import request,flash,session,abort
from flask import Response, stream_with_context


from DB_handler import DBModule

app = Flask(__name__)
DB = DBModule()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")


@app.route("/signin_done",methods=["GET"])
def signin_done():
    name = request.args.get("signin_name")
    uid = request.args.get("signin_id")
    pwd = request.args.get("signin_pwd")
    phoneNumber = request.args.get("signin_phoneNumber")
    DB.signin(name,uid,pwd,phoneNumber)
    return redirect(url_for("login"))
    

@app.route("/login")
def login():
    
    #  jwt 조건문
    return render_template("login.html")

@app.route("/login_done")
def login_done():
    uid = request.args.get("signin_id")
    pwd = request.args.get("signin_pwd")


    #  jwt 조건문
    
    return render_template("login.html")







if __name__ == "__main__":
    app.run(port=5503,host="0.0.0.0",debug=True)