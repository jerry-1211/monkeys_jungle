import time
import datetime
import os
import cv2
import numpy as np
import jwt


from flask import Flask,redirect,render_template,url_for,jsonify, make_response
from flask import request,flash,session,abort
from flask import Response, stream_with_context

from flask_socketio import SocketIO,emit,join_room, leave_room

from DB_handler import DBModule

app = Flask(__name__)
app.config['SECRET_KEY'] = 'monkeysJungle'
socketio = SocketIO(app)
DB = DBModule()


@app.route("/")
def index():
    token = request.cookies.get('token')
    user_data = verify_token(token) if token else None
    return render_template("index.html", logged_in=bool(user_data))

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/login")
def login():
    token = request.cookies.get('token')
    user_data = verify_token(token) if token else None
    return render_template("login.html", logged_in=bool(user_data))

@app.route("/signin_done",methods=["POST"])
def signin_done():
    name = request.form.get("signin_name")
    userId = request.form.get("signin_id")
    pwd = request.form.get("signin_pwd")
    phoneNumber = request.form.get("signin_phoneNumber")
    mbti = request.form.get("signin_mbti")
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
    DB.signin(name,userId,pwd,phoneNumber,mbti,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10)
    return redirect(url_for("login"))
    
# 토큰 검증을 위한 데코레이터
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert': 'Token missing'}), 403

        try:
            # payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print("############################################")
            # print(payload)
            print("############################################")
        except :
            return jsonify({'Alert': 'Missing'}), 403
        return func(*args, **kwargs)
    return decorated

# JWT 토큰 생성 함수
def generate_token(user_id):
    token = jwt.encode({
        'user': user_id,
        # 토큰 만료 시간 설정
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return token

@app.route("/login_done", methods=['POST'])
def login_done():
    
    username = request.form.get('login_id')
    password = request.form.get('login_pwd')
    
    # None 체크 추가
    if username is None or password is None:
        return jsonify({'Alert': '아이디, 비밀번호를 입력하세요.'}), 400
    
    # 입력하지 않았을때
    if not username or not password:
        return jsonify({'Alert': '아이디,비밀번호를 입력하세요.'}), 400
    
    # 비밀번호 관련
    valid_state = DB.findPassword(username,password)
    
    # 사용자 정보가 없는 경우 처리
    if valid_state is None:
        return jsonify({'Alert': '사용자 정보가 없습니다.'}), 404
    
    # 비밀번호 오류인 경우 처리
    if valid_state:
        return jsonify({'Alert': '비밀번호 오류입니다.'}), 401    
    
    # 토큰 생성
    token = generate_token(username)
    print(token)
    
    # 응답을 생성하고 쿠키에 토큰을 저장
    response = make_response(redirect(url_for('index')))
    response.set_cookie('token', token)
    
    return response

def verify_token(token):
    # JWT 토큰을 검증하고 유효성을 확인하는 함수.
    if not token:
        return None, {'Alert': '권한이 없습니다.'}, 403

    try:
        # Bearer 토큰 형식인 경우 'Bearer '를 제거
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        
        # JWT 디코딩
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return data, None, None
    except jwt.ExpiredSignatureError:
        return None, {'Alert': '권한이 없습니다.'}, 403
    except jwt.InvalidTokenError:
        return None, {'Alert': '유효하지 않습니다.'}, 403

@app.route('/protected', methods=['GET'])
def protected():
    # Authorization 헤더에서 토큰 가져오기
    token = request.headers.get('Authorization')
    
    # 토큰 검증
    data, error_response, status_code = verify_token(token)
    
    if error_response:
        return jsonify(error_response), status_code

    # 성공적인 인증 후 응답
    return jsonify({'message': 'This is a protected route.', 'user': data['user']}), 200

@app.route("/logout")
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('token', '', expires=0)  # 쿠키에서 토큰 삭제
    return response


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


@app.route("/card")
def card():
    token = request.cookies.get('token')
    user_data = verify_token(token) if token else None
    
    if not(user_data) : 
        flash('로그인 후 이용 부탁드립니다 !')
        return redirect(url_for('index'))  
    return render_template("card.html", logged_in=bool(user_data))

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
    print(pid_post)
    return '', 204

@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify({'data': pid_post})


# ------------------------------------------------------

"""제림 계시글 정보 업로드 중"""
@app.route('/chat')
def chat():
    return redirect(url_for('chat_user'))

@app.route('/chat_user')
def chat_user():
    token = request.cookies.get('token')
    user_data = verify_token(token)     
    username = user_data[0]["user"]
 
    info = DB.get_post_info(pid_post)
    return render_template("chat.html",
        username=username, logged_in=bool(user_data),
        info = info 
        )



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# @app.route("/get_userinfo", methods=["POST"])
# def giveUserInfo():
#     userId = request.form['id_give']
#     print(userId)

#     if userId == informations["userId"]:
#         return jsonify({"result":"success", "userInfo": informations})
#     else:
#         return jsonify({"result":"failed"})

# @app.route('/banana', methods=['POST'])
# def incrementBanana():
#     # # 클라이언트로부터 받은 토큰을 디코딩하여 유저 정보를 알아냄

#     # 
#     # id_receive = request.form['id_give'] # 
#     # user = db.users.find_one({'myID': id_receive}) #프로필의 유저

#     # # 해당 documents의 likes를 새로운 변수에 받아 1 증가시킨다.
#     # tempBanana = user['bananas'] + 1

#     # # 증가시킨 변수로 다시 셋팅
#     # db.users.update_one({'myID': id_receive}, {'$set': {'bananas': tempBanana}})
#     return jsonify({'result': 'success'})



if __name__ == '__main__':
    socketio.run(app,host="0.0.0.0", port=5000, debug=True)


