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


@app.route("/signin_done",methods=["POST"])
def signin_done():
    name = request.form.get("signin_name")
    userId = request.form.get("signin_id")
    pwd = request.form.get("signin_pwd")
    phoneNumber = request.form.get("signin_phoneNumber")
    q1 = request.form.get("signin_q1")
    q2 = request.form.get("signin_q2")
    q3 = request.form.get("signin_q3")
    q4 = request.form.get("signin_q4")
    q5 = request.form.get("signin_q5")
    q6 = request.form.get("signin_q6")
    q7 = request.form.get("signin_q7")
    q8 = request.form.get("signin_q8")
    q9 = request.form.get("signin_q9")
    q10 = request.form.get("signin_q10")
    DB.signin(name,userId,pwd,phoneNumber,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10)
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