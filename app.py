import os
import re #디렉토리 절대 경로
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from Models import db
from Models import User

from sklearn.linear_model import LinearRegression, Ridge, Lasso
import os
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
reg = pickle.load(open(os.path.join('ridge/pkl_objects', 'reg.pkl'),'rb'))
reg_int= reg.intercept_
reg_coef=list(reg.coef_)
col=['유가', '농축수산물물가지수','농축수산물','연별수확량','연별재배면적','연별재배면적(전년)','양파물가지수','연별재배면적당수확량(전년)','양파수입']
reg= pd.DataFrame(reg_coef).T
reg.columns = col


app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/', methods=['GET','POST'])
def data():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # 유가 = float(input('유가: '))
        # 농축수산물물가지수 = float(input('농축수산물물가지수: '))
        # 농축수산물 =float(input('농축수산물: '))
        # 연별수확량 = float(input('연별수확량: '))
        # 연별재배면적 = float(input('연별재배면적: '))
        연별재배면적_전년 = 18461
        # 양파물가지수 = float(input('양파물가지수: '))
        연별재배면적당수확량_전년 = 85 
        # #1h당 반올림
        # 양파수입 = np.log1p(float(input('양파수입: ')))
        유가 = request.form.get('유가')
        농축수산물물가지수 = request.form.get('농축수산물물가지수')
        농축수산물 = request.form.get('농축수산물')
        연별수확량 = request.form.get('연별수확량')
        연별재배면적 = request.form.get('연별재배면적')
        양파물가지수 = request.form.get('양파물가지수')
        양파수입1 = request.form.get('양파수입')
        print(양파수입1)
        양파수입 = np.log1p(int(양파수입1))
        data = [유가, 농축수산물물가지수,농축수산물,연별수확량,연별재배면적,연별재배면적_전년,양파물가지수,연별재배면적당수확량_전년,양파수입]
        배추가격 = 0
        if not(유가 and 농축수산물물가지수 and 농축수산물 and 연별재배면적 and 연별수확량 and 양파물가지수 and 양파수입):
            value = "?"
            return render_template("register.html",value=value)
        else:
            for i in range(9):
                배추가격 += float(data[i]) * reg.iloc[0,i]
            예상가격 = int(np.expm1(배추가격+reg_int))
            value  = 예상가격
            print(value )
        return render_template("register.html",value = value )

@app.route('/hello', methods=['GET','POST']) #GET(정보보기), POST(정보수정) 메서드 허용
def hello():
        userid = request.form.get('userid')
        email = request.form.get('email')
        password = request.form.get('password')
        password_2 = request.form.get('password')

        if not(userid and email and password and password_2):
            return "입력되지 않은 정보가 있습니다"
        elif password != password_2:
            return "비밀번호가 일치하지 않습니다"
        else:
            usertable=User() #user_table 클래스
            usertable.userid = userid
            usertable.email = email
            usertable.password = password
            
            db.session.add(usertable)
            db.session.commit()
            return "회원가입 성공"
        return render_template("hello.html")

if __name__ == "__main__":
#     #데이터베이스---------
#     basedir = os.path.abspath(os.path.dirname(__file__)) #현재 파일이 있는 디렉토리 절대 경로
#     dbfile = os.path.join(basedir, 'db.sqlite') #데이터베이스 파일을 만든다

#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
#     app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #사용자에게 정보 전달완료하면 teadown. 그 때마다 커밋=DB반영
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #추가 메모리를 사용하므로 꺼둔다

# #    db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장
#     db.init_app(app) #app설정값 초기화
#     db.app = app #Models.py에서 db를 가져와서 db.app에 app을 명시적으로 넣는다
#     db.create_all() #DB생성

    app.run(host="127.0.0.1", port=5000, debug=True)