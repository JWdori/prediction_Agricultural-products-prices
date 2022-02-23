from sklearn.linear_model import LinearRegression, Ridge, Lasso
import os
import pickle
import pandas as pd
import numpy as np


reg = pickle.load(open(os.path.join('ridge/pkl_objects', 'reg.pkl'),'rb'))
reg_int= reg.intercept_
reg_coef=list(reg.coef_)
col=['유가', '농축수산물물가지수','농축수산물','연별수확량','연별재배면적','연별재배면적(전년)','양파물가지수','연별재배면적당수확량(전년)','양파수입']
reg= pd.DataFrame(reg_coef).T
reg.columns = col

#22년 기준
유가 = float(input('유가: '))
농축수산물물가지수 = float(input('농축수산물물가지수: '))
농축수산물 =float(input('농축수산물: '))
연별수확량 = float(input('연별수확량: '))
연별재배면적 = float(input('연별재배면적: '))
연별재배면적_전년 = 18461
양파물가지수 = float(input('양파물가지수: '))
연별재배면적당수확량_전년 = 85 
#1h당 반올림
양파수입 = np.log1p(float(input('양파수입: ')))

data = [유가, 농축수산물물가지수,농축수산물,연별수확량,연별재배면적,연별재배면적_전년,양파물가지수,연별재배면적당수확량_전년,양파수입]


배추가격 = 0
for i in range(9):
    배추가격 += data[i] * reg.iloc[0,i]
    
print('예상 배추 가격은',int(np.expm1(배추가격+reg_int)),'원 입니다.')