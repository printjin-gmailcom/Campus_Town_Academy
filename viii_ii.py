import pandas as pd

raw = pd.read_excel('./data/삼성전자블루스카이.xlsx', thousands = ',')
raw.info()

raw['price'].hist()

import matplotlib
from matplotlib import font_manager, rc
import platform
import matplotlib.pyplot as plt
import seaborn as sns


if platform.system() == 'Windows':
# 윈도우인 경우
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
else:
# Mac 인 경우
    rc('font', family='AppleGothic')

matplotlib.rcParams['axes.unicode_minus'] = False
#그래프에서 마이너스 기호가 표시되도록 하는 설정입니다.

import seaborn as sns

sns.boxplot(data = raw, x = 'mall', y = 'price')

len(raw['mall'].unique())

raw['mall'].value_counts()

raw['mall'].value_counts().head().index



cond = [True, False, True, True, ,,,,]
raw[cond]



topmall = raw['mall'].value_counts().head().index
topmall

cond = []
for mall in raw ['mall']:
    check = mall in topmall
    cond.append(check)
raw[cond]



cond = raw['mall'].isin(topmall)
raw[cond]



sns.boxplot(data = raw[cond], x = 'mall', y = 'price')

