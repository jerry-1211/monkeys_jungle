import time
import datetime
import os
import cv2
import numpy as np
import jwt


from flask import Flask,redirect,render_template,url_for,jsonify, make_response
from flask import request,flash,session,abort
from flask import Response, stream_with_context


from DB_handler import DBModule

app = Flask(__name__)
app.config['SECRET_KEY'] = 'monkeysJungle'
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


if __name__ == "__main__":
    app.run(port=5503,host="0.0.0.0",debug=True)