import time
import datetime
import os
import cv2
import numpy as np


from flask import Flask,redirect,render_template,url_for,jsonify
from flask import request,flash,session,abort
from flask import Response, stream_with_context


app = Flask(__name__)

@app.route("/")
def index():
    
    return render_template("index.html")



if __name__ == "__main__":
    app.run(port=5503,host="0.0.0.0",debug=True)