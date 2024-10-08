import folium
import pandas as pd
from folium.plugins import MarkerCluster
from folium.plugins import MiniMap

raw = pd.read_excel('./data/starbucks_list.xlsx')

# 지도의 중간 위치를 '서울역'으로 잡는 것
seoul_station = [37.555946, 126.972317]
m = folium.Map(location = seoul_station, zoom_start = 13)

markercluster = MarkerCluster().add_to(m)

for i in raw.index:
    name = raw.loc[i, '매장명']
    lat = raw.loc[i, '위도']
    long = raw.loc[i, '경도']
    shop = raw.loc[i, '매장타입']
    folium.Marker([lat, long], tooltip = name, popup = shop).add_to(markercluster)
m.save('스타벅스지도_클러스터.html')

import folium
import pandas as pd
from folium.plugins import MarkerCluster
from folium.plugins import MiniMap

raw = pd.read_excel('./data/starbucks_list.xlsx')

seoul_station = [37.555946, 126.972317]
m = folium.Map(location = seoul_station, zoom_start = 13)

markercluster = MarkerCluster().add_to(m)

for i in raw.index:
    name = raw.loc[i, '매장명']
    lat = raw.loc[i, '위도']
    long = raw.loc[i, '경도']
    shop = raw.loc[i, '매장타입']
    folium.Marker([lat, long], tooltip = name, popup = shop).add_to(markercluster)

MiniMap().add_to(m)

m.save('스타벅스지도_클러스터2.html')

