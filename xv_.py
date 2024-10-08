"""
# 고객 세분화

## *1*. 환경 설정

### 1.1 분서에 필요한 library 호출 및 google drive 연결
"""

# 분석에 필요한 library 호출
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# google drive 연결
from google.colab import drive
drive.mount('/content/drive')

"""## *2*. 데이터 불러오기

### 2.1 데이터 불러오기 및 확인
"""

df_org = pd.read_csv('/content/data.csv',encoding='latin')
df_org.head() #데이터 확인

df_org.tail() #데이터 확인

df_org.info()

"""### 2.2 데이터 형변"""

# 문자열 변수를 datetime 으로 변환
# df_org['InvoiceDate'] = pd.DatetimeIndex(df_org['InvoiceDate'])
# df_org.info()

"""## 3.NULL 값 처리
### 3.1 NULL 값 확인
"""

# Null 값이 있는 전체 case 수 확인
df_org.isnull().sum().sum()

# Null 값의 비율
df_org.isnull().sum().sum() / df_org.shape[0]

# Null 값이 있는 변수 확인
df_org.isnull().sum()

"""### 3.2 NULL 값 처리 (삭제) 및 확인"""

df_na_treat =  df_org.dropna(axis = 0)

df_na_treat.isnull().sum().sum()

df_na_treat.shape

"""## *4*. 데이터탐색 및 이상치 제거

### 4.1 이상치 확인
"""

df_na_treat.describe()

# 이상치 케이스 확인
df_na_treat[(df_na_treat.Quantity == -80995) | (df_na_treat.Quantity == 80995) ]

# Quantity 이상치 case 확인
df_na_treat[df_na_treat.Quantity <= 0 ].count()

# 음수값으로 시작하는 case는 InvocieNo 가 'C' 로 시작 하는 경우와 case 가 동일함
df_na_treat['InvoiceNo'].str.startswith("C").value_counts()

df_na_treat[(df_na_treat.Quantity <= 0) & (df_na_treat.InvoiceNo.str.startswith("C"))].shape

# UnitPirce 가 가장 큰 값도 환불 case 임
df_na_treat[df_na_treat.UnitPrice == 38970]

df_na_treat[df_na_treat.UnitPrice == 0].head(10)

"""### 4.2 EDA

"""

# 연속형 변수의 대략적인 분포 확인

df_na_treat.describe()

sns.boxplot(df_na_treat['Quantity'])
plt.xlim(-10,200)
plt.show()

df_na_treat['Quantity'].quantile(q=0.99,  interpolation='nearest')

sns.distplot(df_na_treat['Quantity'], bins = 10000)
plt.xlim(-10,150)
plt.show()

"""#### UnitPrice"""

sns.boxplot(df_na_treat['UnitPrice'])

sns.boxplot(df_na_treat['UnitPrice'])
plt.xlim(-10,100)

sns.distplot(df_na_treat['UnitPrice'], hist = True, kde = False, rug = False, bins =10000)
plt.xlim(0,500)
plt.show()

#  어떤 데이터인지 case 확인
df_na_treat[df_na_treat.UnitPrice >= 1000]

# 값이 1000 이상인 case 갯수 확인
df_na_treat[df_na_treat.UnitPrice >= 1000].shape

"""#### InvoiceDate"""

print(pd.DatetimeIndex(df_na_treat['InvoiceDate']).min())
print(pd.DatetimeIndex(df_na_treat['InvoiceDate']).max())
print(pd.DatetimeIndex(df_na_treat['InvoiceDate']).to_period('D').value_counts().head(20))

pd.DatetimeIndex(df_na_treat['InvoiceDate']).to_period('M').value_counts()

df_na_treat['Country'].value_counts()
# df_na_treat['Country'].value_counts().sum()

"""#### InvoiceDate"""

df_na_treat

df_na_treat.groupby(['StockCode','Description']).size().sort_values(ascending=False).head(10)

df_na_treat.duplicated().sum()

"""### 4.3 데이터 cleansing
 1. 환불 제거
 2. 무료구매인건 제거  
 3. CustomerId NULL 제거
 4. 중복 데이터 제
"""

df_outlier_treat = df_na_treat[(df_na_treat.Quantity > 0) & (df_na_treat.UnitPrice != 0) & (~df_na_treat.CustomerID.isnull())]
df_outlier_treat = df_outlier_treat[~df_outlier_treat.duplicated()]
df_outlier_treat.shape

"""# *5*. 유저단위 스코어링을 위해 데이터 요약

### 5.1 Frequecy(구매 건수)생성
"""

# frequecy(구매 건수)계산을 위해 CustomerId, InvoiceNo 별로 요약
# df_na_treat.groupby(['StockCode','Description']).size().sort_values(ascending=False).head(10)

# temp_frequecy = df_outlier_treat.groupby(['CustomerID']).InvoiceNo.nunique()
temp_frequecy = df_outlier_treat.groupby(['CustomerID']).size()
temp_frequecy.head()
sns.distplot(temp_frequecy)

#
temp_frequecy.to_frame()
df_frequecy = temp_frequecy.reset_index().rename(columns = {'index' :'CustomerID'})
df_frequecy.columns = ['CustomerID','frequecy']
df_frequecy

"""## 5.2 Moneytery(유저별 구매금액) 생성

"""

temp = df_outlier_treat[['CustomerID','Quantity','UnitPrice']].copy()
temp['monitery'] = temp['Quantity'] * temp['UnitPrice']
temp_monitery = temp.groupby(['CustomerID']).monitery.sum()
temp_monitery.head()
sns.distplot(temp_monitery)

df_monitery = temp_monitery.to_frame()
df_monitery = df_monitery.reset_index().rename(columns = {'index' :'CustomerID'})
df_monitery

"""## 5.3 Recency (유저별 최근 거래) 생성
 - 오늘을 2011-12-10일 로 가정  
"""

temp2 = df_outlier_treat[['CustomerID','InvoiceDate']].copy()
temp2['today'] ="2011-12-10"

temp2['diff_days'] = (pd.to_datetime(temp2['today']) - pd.to_datetime(temp2['InvoiceDate'])).dt.days
recency = temp2.groupby('CustomerID').diff_days.min()
recency

df_recency = recency.to_frame()
df_recency = df_recency.reset_index().rename(columns = {'index' :'CustomerID', 'diff_days' :'recency'})
df_recency

rfm = pd.merge(df_frequecy, df_recency, how = 'inner', on ='CustomerID')

"""## 5.4 RFM 스코어 생성"""

# R,F,M 데이터 통합
RFM_data = pd.merge(rfm, df_monitery, how ='inner', on= 'CustomerID')
RFM_data

# 각 분위수별 값 설정 및 total 스코어 생성
RFM_data['fre_score'] = pd.qcut(RFM_data['frequecy'],4, labels =[1,2,3,4])
RFM_data['rec_score'] = pd.qcut(RFM_data['recency'],4, labels =[4,3,2,1]) # 최근성은 값이 낮을 수록 높은 점수를 받도록 순서를 바꿈
RFM_data['mon_score'] = pd.qcut(RFM_data['monitery'],4, labels =[1,2,3,4])
RFM_data['total_score'] = RFM_data['fre_score'].astype(int) + RFM_data['rec_score'].astype(int) + RFM_data['mon_score'].astype(int)
RFM_data.head(10)

# 데이터 분포 시각화
RFM_data['total_score'].value_counts().sort_index().plot(kind='bar')

"""## 5.5 RFM 축약"""

#  RFM 점수 상관분석
plt.figure(figsize =(8,8))
sns.heatmap(data = RFM_data[['frequecy','recency','monitery']].corr(),annot= True,
            fmt ='.1%', linewidths =.5, cmap='Blues')
plt.show()

# FM 모형의 분포 확인
df_count_pivot = RFM_data[['fre_score', 'mon_score']].value_counts(sort= False,normalize=True).sort_index().to_frame().unstack()
df_count_pivot

# FM 모형의 분포 시각화
sns.heatmap(df_count_pivot, annot= True, fmt ='.1%', linewidths =.5, cmap='Blues')

# 전체 데이터 수 확인
print(RFM_data.shape)
##  유저 4338명에 대해  8개 변수 생성
RFM_data.head()

# FM 스코어만 적용 하여 해당월 저장
FM_score = RFM_data[['CustomerID', 'frequecy', 'monitery', 'fre_score', 'mon_score']].copy()
FM_score['fre_score'] =FM_score['fre_score'].astype(int)
FM_score['mon_score'] =FM_score['mon_score'].astype(int)
FM_score['fm_score']= FM_score['fre_score'] + FM_score['mon_score']
FM_score['create_date'] =  '2012-01-01'  # 2011년 12월 기준 score 로 2012년 사용 목적 저장
FM_score.head()
