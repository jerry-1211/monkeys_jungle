import time
import datetime
import os
import cv2
import numpy as np

from flask import Flask,redirect,render_template,url_for,jsonify
from flask import request,flash,session,abort
from flask import Response, stream_with_context

from flask_socketio import SocketIO,emit,join_room, leave_room


from DB_handler import DBModule

app = Flask(__name__)
socketio = SocketIO(app)
DB = DBModule()

@socketio.on('connect', namespace='/card')
def connect():
    print('소켓 연결 완료!')

@socketio.on('disconnect', namespace='/card')
def disconnect():
    print('소켓 연결 실패...')

# ObjectId를 JSON으로 직렬화할 수 있도록 문자열로 변환하는 함수
def serialize_message(message):
    message['_id'] = str(message['_id'])  # ObjectId를 문자열로 변환
    return message

@app.route("/")
def index():
    return render_template("index.html")

# ------------------------------------------------------
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

# ------------------------------------------------------
@app.route("/card")
def card():
    
    #  jwt 조건문
    return render_template("card.html")

@app.route("/submit-card",methods=["POST"])
def submitCard():
    title = request.form["title"]
    status = request.form["status"]
    content = request.form["content"]

    existing_card = DB.existing_card({"title": title, "status": status, "content": content})
    if existing_card:
        return render_template("card.html")  # 카드가 이미 존재하는 경우 아무 작업도 수행하지 않음
    
    DB.card_info(title, content, status)
    return render_template("card.html")

    
@app.route('/upload-card', methods=['GET'])
def uploadCard():
    result = DB.uploadCard()
    return jsonify({'result': 'success', 'cards': result})


# ------------------------------------------------------
@socketio.on('leave')
def on_leave(data):
    """클라이언트가 방을 나갈 때 호출되는 함수."""
    username = data['user']
    room = data['room']
    leave_room(room)
    emit('status', {'msg': username + ' has left the room.'}, room=room)

@socketio.on('join')
def on_join(data):
    """클라이언트가 방에 참여할 때 호출되는 함수."""
    username = data['user']
    room = data['room']
    
    join_room(room)  # 클라이언트를 해당 방에 추가
    emit('status', {'msg': username + ' has entered the room.'}, room=room)

    # 방의 이전 메시지 가져오기
    previous_messages = DB.message_find_room(room)
    
    emit('previousMessages', previous_messages, room=request.sid)

@socketio.on('message')
def handle_message(data):
    """클라이언트가 메시지를 보낼 때 호출되는 함수."""
    room = data['room']
    user = data['user']
    message = data['message']
    
    information = {
        'room': room,
        'user': user,
        'message': message
    }
    
    # MongoDB에 메시지 저장
    message_id = DB.message_insert(information)

    # 메시지를 룸에 있는 모든 클라이언트에게 전송
    emit('message', {'user': user, 'message': message, '_id': str(message_id)}, room=room)

# post PID 서버에 저장 
pid_post = None
@app.route('/save-data', methods=['POST'])
def save_data():
    global pid_post
    pid_post = request.json.get('data')
    print("왜 안되는거냐고 ")
    print(pid_post)
    return '', 204

@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify({'data': pid_post})


# ------------------------------------------------------
@app.route('/chat')
def chat():
    return render_template("chat.html")


if __name__ == '__main__':    
    socketio.run(app,host="0.0.0.0", port=5000, debug=True)