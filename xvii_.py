"""
# 동시구매 상품분석 실습

## **1. 환경 설정**

### 1.1 분서에 필요한 library 설치,호출 및 google drive 연결
"""

# 연관성분석(추천)  패키지 다운로드 및 설치
!pip install mlxtend --upgrade

## 1. 분석에 사용할 패키지 로딩
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import datetime as dt # 날짜를 다루기 위한 패키지

from mlxtend.preprocessing import TransactionEncoder # 구매 데이터를 연관성 분석을 위한 메트릭스 형태로 변환
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth # fpgrowth 는 mlxtend version: 0.20.0 이상에서 지원

# 구글드라이브에 있는 데이터셋 연결을 위한 구글드라이브 세팅
from google.colab import drive
drive.mount('/content/drive')

"""## **2. 데이터 불러오기 및 확인**

### 2.1 데이터 불러오기 및 확인
"""

data = pd.read_csv('/content/data.csv', encoding= 'unicode_escape')

data.head() # 처음 5개 데이터 확인

data.tail() # 마지막 5개 데이터 확인

# 각 컬럼(변수)의 유형 확인
data.info()

# 연속형 변수의 분포 확인
data.describe()

"""### 2.2 데이터형변환"""

# 데이터형변환 : 날짜 계산을 위해 InvoiceDate의 Data type을 object type -> datetime64 로 변환
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
data.info()

data.head()

"""## **3. Null값 확인 및 처리**

### 3.1 Null 값 확인
"""

# 3.1 Null 값이 있는 전체 case 수 확인
print(data.isnull().sum().sum())

data.isnull().sum()

# 혹시 "" 공란으로 비어 있는 값이 있나 확인
data[data['Description']=='']

"""#### CustomerID 가 Null 값인 거래의 구매 상품수량 분포 확인해보기"""

# CustomerID Null 값인과 정상 거래 트랜잭션 별 상품수 확인
data_null= data[data.CustomerID.isnull()].groupby('InvoiceNo')['StockCode'].count()
print(data_null)

# CustomerID Null 값의 구매상품 수량 분포 시각화확인
plt.hist(data_null)

"""#### CustomerID 가 Null 이 아닌(정상인) 거래의 구매 상품수량 분포 확인해보기

"""

data_notnull = data[data.CustomerID.notnull()].groupby('InvoiceNo')['StockCode'].count()
plt.hist(data_notnull)

"""### 3.2 Null 값 처리 (삭제) 및 확인"""

# Description NA 값 확인 및 처리
## 상품 정보를 확인할 수 있는 Description이 Null 인 것만 분석에서 제외
## 연관성 분석의 기준은 CustomerID 기준이 아니라 InvoiceNo 기준이라 CustomerID 값이 Null 인것도 사용함
data_na_treat = data[data.Description.notnull()]
data_na_treat.describe()

data_na_treat.head()

# Description의 Null 값이 모두 빠졌는지 확인
data_na_treat.isnull().sum()

"""## **4. 데이터 탐색 및 이상치 제거**

### 4.1 이상치 확인 및 제거

#### 음수값 확인 (환불 case)
"""

# Quantity 이상치 case 확인
data_na_treat[(data_na_treat.Quantity == 80995) | (data_na_treat.Quantity == -80995)]

# 음수 -> 환불 확인
data_na_treat[(data_na_treat.Quantity <= 0) & (data_na_treat.InvoiceNo.astype(str).str[0] == 'C')]

"""#### 음수값 제거"""

# 환불 데이터는 InvoiceNo 앞에 "C"로 표시 &  Quantity 값이 음수(-)
data_pur = data_na_treat[data_na_treat.InvoiceNo.astype(str).str[0] != 'C']
data_pur.describe()

"""#### 트랜젝션당 거래 상품수"""

# 분석 단위 확인을 위한 트랜잭션 당 구매 상품수 확인
data_pur.groupby('InvoiceNo')['StockCode'].count().describe()

#  유저별로 얼마나 많이 주문을 했나 ? 유저별 거래수
data_pur.groupby('CustomerID')['InvoiceNo'].nunique().describe()

# 유저별로 하루에 거래한 횟수
data_pur['dt'] = pd.to_datetime(data_pur['InvoiceDate']).dt.date
data_pur.groupby(['CustomerID','dt'])['InvoiceNo'].nunique().describe()

# 유저별로 확인
data_pur.groupby('CustomerID')['StockCode'].nunique().describe()

# InvoiceNo 단위로도 충분
data_invoice_cnt = data_pur.groupby('InvoiceNo').agg(
    n = ('StockCode','count'))
data_invoice_cnt.columns = ['n']
data_invoice_cnt

data_invoice_cnt.describe()

# 이상치 제거  (한번에 너무 많은 상품을 구매하는 InvoiceNo 제거 )
# 이상치 기준 탐색
fig, ax = plt.subplots()
ax.boxplot(data_invoice_cnt['n'])
#ax.set_ylim (0,100)

# 특정 분위수값  확인
np.percentile(data_invoice_cnt['n'], 95)

## data_invoice_cnt['n'].quantile(q=0.99)

data_invoice_cnt.mean()[0]

print(f"mean: {data_invoice_cnt.mean()[0]}, sd: {data_invoice_cnt.std()[0]}, \ntwo_sigma(상위 2.2%): {data_invoice_cnt.mean()[0]+2*data_invoice_cnt.std()[0]}, \nthree_sigma (상위0.1%): {data_invoice_cnt.mean()[0]+3*data_invoice_cnt.std()[0]}")

"""#### 트랜젝션당 거래 상품수 이상치제거"""

outlier_treat = data_invoice_cnt[(data_invoice_cnt.n >= 2)  & (data_invoice_cnt.n <= 120)]
pur_outlier_treat = pd.merge(outlier_treat, data_pur, how ='inner', on = 'InvoiceNo' )
pur_outlier_treat

"""### 4.2 데이터 탐색

#### 각 국가별 주문건수
"""

# 각 국가별 주문건수
invoce_product_cnt = pur_outlier_treat.groupby(['Country','InvoiceNo']).size()
invoce_product_cnt.groupby('Country').count().sort_values(ascending = False)

"""#### 각 국가별 가장 많은 거래에 포함된 상품 Top 5 비교  (직접해보기)"""

# pandas row 수를 모두 보여주기 옵션 (단, 느려질 수 있음)
pd.set_option('display.max_rows', None)

# 각 국가별 가장 많은 거래에 포함된 상품 Top 5 비교
## 1.국가별, 주문번호별, 상품명 만 있는 데이터 만들기
## 2. 국가별, 상품명 별로 groupby 요약하여 count 생성
## 3. 국가별, count 별로 rank 를 생성
## 4. rank 가 5위 안인것만 나라별, rank 별로 정렬하여 보기

pd.reset_option('display.max_rows')

"""## 5.데이터 변환 및 데이터 탐색

### 5.1 연관성 분석용 matrix 생성
"""

pur_by_tran = pur_outlier_treat[['InvoiceNo', 'Description']]

def toList(x):
    return list(set(x))

purchase_list = pur_by_tran.groupby('InvoiceNo')['Description'].apply(lambda x: toList(x)).reset_index()
purchase_list = list(purchase_list.Description)
purchase_list[:5]

te = TransactionEncoder()
te_ary = te.fit(purchase_list).transform(purchase_list)
df = pd.DataFrame(te_ary, columns=te.columns_)
df

"""### 5.2 EDA #####

"""

# 가장 많이 구매항 상품 top 10
fig, ax = plt.subplots()
pur_outlier_treat['Description'].value_counts().head(10).plot(ax=ax, kind='bar')

pur_outlier_treat['Description'].value_counts(normalize =True)#.plot(ax=ax, kind='bar')

"""## 6.모델링

### 6.1연관성 모델 생성

#### 전체 데이터 적용& APRIORI 알고리즘 적용
"""

# 연관성 분석 알고리즘 적용
freq_itemsets1 = fpgrowth(df, min_support = 0.01, max_len = 3, use_colnames = True)
## 옵션 최소 1% 이상 판매된 상품, 최대 길이 3개 까지 상품 조합을 했을 때 까지 고려, items 이름을 번호가 아닌 이름으로 표시

freq_itemsets1
## 1101개 상품 조합 (Rule) 생성

# 조건 변경 (최소 지지도 0.5% 이상, 상품 조하 5개 까지)
freq_itemsets2 = fpgrowth(df, min_support = 0.005, max_len = 5, use_colnames = True)
freq_itemsets2

"""### 6.2 생성된 연관성 규칙 확인  #####"""

## antecedents 선형변수 consequents 후행변수 -> 앞에꺼를 샀을 경우에 뒤에꺼를 살 확률
## 보통 리프트 중심으로 체크
rules_conf_20 = association_rules(freq_itemsets1, metric='confidence', min_threshold=0.5)
rules_conf_20.sort_values(['lift'],ascending = False).head(10)

rules.sort_values(['confidence'], ascending=False).head(10)

"""### 6.3 결과파일로 저장"""

# 결과 csv로 저장
df_csv = pd.DataFrame(rules_conf_20)
df_csv.to_csv('/content/drive/MyDrive/[러닝스푼즈] CRM 프로젝트/[러닝스푼즈] CRM 머신러닝 프로젝트 (공유ver.)/4주차/association_rule_result.csv',index=False)
