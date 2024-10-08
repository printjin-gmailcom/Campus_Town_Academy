"""
# 고객 취향 군집화 실습

## **1. 환경 설정**

### 1.1 분서에 필요한 library 호출 및 google drive 연결
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from sklearn.cluster import KMeans

from google.colab import drive
drive.mount('/content/drive')

"""## **2. 데이터 불러오기**

### 2.1 데이터 불러오기 및 확인
"""

# 왼쪽 네비게이션바에서 \drive\Mydrive에 연결된 드라이브에서 data.csv 위치를 찾아서 "..."을 클릭하여 경로복사 후  pd.read_csv의 경로에 붙여넣기

## 원본 데이터 (5.2G)
#df_org = pd.read_csv('/content/2019-Oct.csv')

## 축약 데이터 (100M)
df_org = pd.read_csv('/content/2019-Oct_purchase.csv')
df_org.head()

df_org.tail()

df_org.info()

"""### 2.2 필요한 분석에 데이터 확인 및 선택"""

# event_type 별 값 확인
df_org['event_type'].value_counts()

# 데이터 용량이 너무커서 필요한 구매 데이터만 사용하기로함
df_org = df_org[df_org.event_type =="purchase"]

"""## **3. NULL 값 처리**

### 3.1 NULL 값 확인
"""

# Null 값이 있는 전체 case 수 확인
print(df_org.isnull().sum().sum())

# Null 값의 비율
df_org.isnull().sum().sum() / df_org.shape[0]

# Null 값이 있는 변수 확인 (null 값이 있는 컬럼이 2개 존재)

df_org.isnull().sum()

# 둘다 null 값인 항목확인 (38,388 건)
df_org[(df_org.category_code.isnull()) & (df_org.brand.isnull())]

# brand 값이 null 값인 건 확인
df_org[df_org.brand.isnull()]

"""
### 3.2 NULL 값 처리 (삭제) 및 확인"""

# 이후 브랜드명과 category 값을 기준으로 군집을 생성하고 확인하려고 함. 그렇기 때문에 두 값중 하나라도 null 값인 것은 삭제

df_na_treat =  df_org.dropna(axis = 0)

df_na_treat.isnull().sum().sum()

"""## **4. 데이터탐색 및 이상치 제거**

### 4.1 전체 데이터 확인
"""

# 전체 데이터 확인
df_na_treat.shape

# 연속형 변수의 분포 확인
df_na_treat.describe()
# price를 제외한 나머지는 의미가 없음

# 변수 type 확인
df_na_treat.info()

"""### 4.2 카테고리 데이터 데이터 확인 및 파생"""

# 카테고리 정보확인
df_na_treat.category_code.value_counts(normalize =True)
# 카테고리 텍스트로 들어오고 있으나 값이 "."을 기준으로 구분되어있음

# 카테고리 파싱 (카테고리 단위별로 변수화)
df_na_treat[['ctgr_lv1','ctgr_lv2','ctgr_lv3','ctgr_lv4']] = df_na_treat['category_code'].str.split('.',expand= True)
df_na_treat

# 대카테고리 값과 비율 확인
pd.concat([df_na_treat['ctgr_lv1'].value_counts(),df_na_treat['ctgr_lv1'].value_counts(normalize =True) ], axis = 1)

# 대카테고리 'electronics' 값 확인
pd.concat([df_na_treat.loc[df_na_treat.ctgr_lv1 =="electronics",['ctgr_lv2']].value_counts(),
          df_na_treat.loc[df_na_treat.ctgr_lv1 =="electronics",['ctgr_lv2']].value_counts(normalize=True)], axis= 1)

# 대카테고리 'electronics.smartphone' 값 확인
pd.concat([df_na_treat.loc[(df_na_treat.ctgr_lv1 =="electronics")&(df_na_treat.ctgr_lv2 =="smartphone") ,['brand']].value_counts(),
df_na_treat.loc[(df_na_treat.ctgr_lv1 =="electronics")&(df_na_treat.ctgr_lv2 =="smartphone") ,['brand']].value_counts(normalize=True)], axis = 1)

# 대카테고리 'appliances' 값 확인
pd.concat([df_na_treat.loc[df_na_treat.ctgr_lv1 =="appliances",['ctgr_lv2']].value_counts(),
          df_na_treat.loc[df_na_treat.ctgr_lv1 =="appliances",['ctgr_lv2']].value_counts(normalize=True)], axis= 1)

"""### 4.3 트랜잭션 단위 데이터 -> 유저단위 데이터로  변경 (각 row 별 다른 유저 정보로 )"""

# 유저별 구매 카운트 확인, 전략 카테고리 생성
user_by_ctgr_cnt = df_na_treat.groupby('user_id').agg(
    pur_cnt = ('event_time', 'count')
#   , cash_sum = ('price', 'sum')
)

# 유저별 전략 카테고리 값 요약
smartphone_samsung =  df_na_treat[(df_na_treat.ctgr_lv1 == 'electronics') & (df_na_treat.ctgr_lv2 == 'smartphone') & (df_na_treat.brand == 'samsung')].groupby('user_id')['brand'].count()
smartphone_apple =  df_na_treat[(df_na_treat.ctgr_lv1 == 'electronics') & (df_na_treat.ctgr_lv2 == 'smartphone') & (df_na_treat.brand == 'apple')].groupby('user_id')['brand'].count()
smartphone_ect =  df_na_treat[(df_na_treat.ctgr_lv1 == 'electronics') & (df_na_treat.ctgr_lv2 == 'smartphone') & ~(df_na_treat.brand == 'samsung') & ~(df_na_treat.brand == 'apple')].groupby('user_id')['brand'].count()
electronics = df_na_treat[(df_na_treat.ctgr_lv1 == 'electronics') & ~(df_na_treat.ctgr_lv2 == 'smartphone')].groupby('user_id')['brand'].count()
appliances = df_na_treat[(df_na_treat.ctgr_lv1 == 'appliances')].groupby('user_id')['brand'].count()
ect = df_na_treat[~((df_na_treat.ctgr_lv1 == 'electronics') | (df_na_treat.ctgr_lv1 == 'appliances'))].groupby('user_id')['brand'].count()

smartphone_apple.head()

# series 를 data frame 변경 및 카테고리 명 변경

smartphone_samsung = smartphone_samsung.to_frame().reset_index().rename(columns = {'brand':'smartphone_samsung'})
smartphone_apple = smartphone_apple.to_frame().reset_index().rename(columns = {'brand': 'smartphone_apple'})
smartphone_ect = smartphone_ect.to_frame().reset_index().rename(columns = {'brand' : 'smartphone_ect'})
electronics = electronics.to_frame().reset_index().rename(columns = {'brand': 'electronics'})
appliances = appliances.to_frame().reset_index().rename(columns ={'brand' : 'appliances'})
ect = ect.to_frame().reset_index().rename(columns = {'brand' :'etc'})

# 데이터 통합
user_by_ctgr_cnt = pd.merge(user_by_ctgr_cnt,smartphone_samsung, how ='left', on = 'user_id' )
user_by_ctgr_cnt = pd.merge(user_by_ctgr_cnt,smartphone_apple, how ='left', on = 'user_id' )
user_by_ctgr_cnt = pd.merge(user_by_ctgr_cnt,smartphone_ect, how ='left', on = 'user_id' )
user_by_ctgr_cnt = pd.merge(user_by_ctgr_cnt,electronics, how ='left', on = 'user_id' )
user_by_ctgr_cnt = pd.merge(user_by_ctgr_cnt,appliances, how ='left', on = 'user_id' )
user_by_ctgr_cnt = pd.merge(user_by_ctgr_cnt,ect, how ='left', on = 'user_id' )
user_by_ctgr_cnt.fillna(0,inplace= True)
user_by_ctgr_cnt.head()

"""### 4.4 이상치 확인"""

# 연속형 변수 분포 확인
user_by_ctgr_cnt.describe()

# 이상치 케이스 확인
user_by_ctgr_cnt[user_by_ctgr_cnt['pur_cnt']>= 100]

# box plot 으로 시각화
fig, ax = plt.subplots()
ax.boxplot(user_by_ctgr_cnt['pur_cnt'])
ax.set_ylim (0,20)
ax.set_xlabel('pur_cnt')

"""### 4.5 이상치 기준 정의"""

# 이상치 판단 기준

user_by_ctgr_cnt[user_by_ctgr_cnt['pur_cnt']>= 50]['user_id'].count()

print("표준편차 :", user_by_ctgr_cnt['pur_cnt'].std())
print("99분위수 :", user_by_ctgr_cnt['pur_cnt'].quantile(q =0.99), ", 대상자수 : ",user_by_ctgr_cnt[user_by_ctgr_cnt['pur_cnt']>= 14]['user_id'].count())
print("3시그마 :", (user_by_ctgr_cnt['pur_cnt'].mean()) + (user_by_ctgr_cnt['pur_cnt'].std()*3), ", 대상자수 : ",user_by_ctgr_cnt[user_by_ctgr_cnt['pur_cnt']>= 13]['user_id'].count())
print("6시그마 :", (user_by_ctgr_cnt['pur_cnt'].mean()) + (user_by_ctgr_cnt['pur_cnt'].std()*6), ", 대상자수 : ",user_by_ctgr_cnt[user_by_ctgr_cnt['pur_cnt']>= 23]['user_id'].count())

fig, ax = plt.subplots()
ax.boxplot([user_by_ctgr_cnt['smartphone_samsung'], user_by_ctgr_cnt['smartphone_apple'], user_by_ctgr_cnt['smartphone_ect'], user_by_ctgr_cnt['electronics'], user_by_ctgr_cnt['appliances'],user_by_ctgr_cnt['etc']])
ax.set_ylim (-1,20)
plt.show()

# 각 변수별 상관관계 확인
plt.figure(figsize =(8,8))
sns.heatmap(data = user_by_ctgr_cnt[['pur_cnt','smartphone_samsung','smartphone_apple','smartphone_ect','electronics','appliances','etc']].corr(),annot= True,
            fmt ='.1%', linewidths =.5, cmap='Blues')
plt.show()

# 각 전략 카테고리별 구매건수 확인
fig, ax = plt.subplots()
ax.boxplot([user_by_ctgr_cnt['smartphone_samsung'], user_by_ctgr_cnt['smartphone_apple'], user_by_ctgr_cnt['smartphone_ect'], user_by_ctgr_cnt['electronics'], user_by_ctgr_cnt['appliances'],user_by_ctgr_cnt['etc']])
ax.set_ylim (-1,20)
plt.show()

# 이상치 제거
df_train_data = user_by_ctgr_cnt[(user_by_ctgr_cnt.pur_cnt < 14)]
print(df_train_data.shape)
df_train_data.describe()

"""## **5. 군집화**

### 5.1 변수의 표준화
"""

df_train_data = df_train_data.reset_index()

# 변수 표준화
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(df_train_data.iloc[:,2:])
np_train_scaled = scaler.transform(df_train_data.iloc[:,2:])
np_train_scaled

"""### 5.2 군집화 알고리즘 적용 (k-means clustering)"""

kmeans = KMeans(n_clusters=5)
y_pred = kmeans.fit_predict(np_train_scaled)
kmeans.cluster_centers_

# 최적의 cluster 개수 찾기

kmeans_per_k = [KMeans(n_clusters=k).fit(np_train_scaled) for k in range(1, 11)]
inertias = [model.inertia_ for model in kmeans_per_k]

plt.figure(figsize=(8, 3.5))
plt.plot(range(1, 11), inertias, "bo-")
#plt.axis([1, 8.5, 0, 1300])
plt.show()

# silhouette_score (가능하면 pass, 오래걸림)

# from sklearn.metrics import silhouette_score
# silhouette_score(np_train_scaled, kmeans.labels_)

"""### 5.3 8개 군집생성 및 군집별 특성확인"""

# 8개 군집
kmeans = KMeans(n_clusters=8, random_state = 1111)
y_pred = kmeans.fit_predict(np_train_scaled)
kmeans.cluster_centers_
y_pred

pd.DataFrame(y_pred)
#pd.concat(df_train_data, pd.DataFrame(y_pred))
df_train_data['clst_k8'] = pd.Series(y_pred)
df_train_data.head()

# 각 군집별 비율 확인하기
round(df_train_data.groupby('clst_k8').user_id.count()/df_train_data.shape[0],3)

# 8개 클러스터 EDA
df_train_data.groupby('clst_k8').agg(
    uu = ('user_id','count'),
    avg_pur_cnt = ('pur_cnt','mean'),
    smartphone_samsung_avg = ('smartphone_samsung','mean'),
    smartphone_apple_avg = ('smartphone_apple','mean'),
    smartphone_ect_avg = ('smartphone_ect','mean'),
    electronics_avg = ('electronics','mean'),
    appliances_avg = ('appliances','mean'),
    etc_avg = ('etc','mean')
)
# + 군집비율 붙이기

"""- 0 군집 - 생활가전을 소량 구매 유저(16.0%)
- 1 군집 - 애플폰 다회(충성) 구매 유저 (3.2%)
- 2 군집 - 전자제품 (핸드폰 및 소형 가전제품) 단건 구매 유저(60.2%)
- 3 군집 - 기타 상품 소회 구매 유저 (12.3%)
- 4 군집 - 스마트폰을 제외한 소형 가전제품 다회 구매 유저 (1.9%)
- 5 군집 - 생활가전 다회 구매하며 삼성폰을 간간히 구매 유저 (0.8%)
- 6 군집 - 기타 스마트폰 다회 구매 유저 (1.9%)
- 7 군집 - 삼성폰을 다회(충성) 구매 유저 (3.6%)

### 5.4 4개 군집생성 및 군집별 특성확인
"""

# 4개 군집
kmeans = KMeans(n_clusters=4, random_state= 1111)
y_pred = kmeans.fit_predict(np_train_scaled)
kmeans.cluster_centers_
y_pred
df_train_data['clst_k4'] = pd.Series(y_pred)

# 각 군집별 비율 확인하기
df_train_data.groupby('clst_k4').user_id.count()/df_train_data.shape[0]

# 8개 클러스터 EDA
df_train_data.groupby('clst_k4').agg(
    uu = ('user_id','count'),
    avg_pur_cnt = ('pur_cnt','mean'),
    smartphone_samsung_avg = ('smartphone_samsung','mean'),
    smartphone_apple_avg = ('smartphone_apple','mean'),
    smartphone_ect_avg = ('smartphone_ect','mean'),
    electronics_avg = ('electronics','mean'),
    appliances_avg = ('appliances','mean'),
    etc_avg = ('etc','mean')
)

"""- 0 군집 - 생활 가전 단건 구매 유저 (16.6%)
- 1 군집 - 스마트폰 다회 구매 유저 (애플과 삼성 스마트폰 중심) 5.9%
- 2 군집 - 전자제품이 아닌 기타 제품 단건 구매 유저 (12.8%)
- 3 군집 - 휴대폰 및 소형가전만 단건 구매 유저 (64.6%)

---
"""
