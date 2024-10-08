import folium
import pandas as pd

seoul_station = [37.555946, 126.972317]
m = folium.Map(location = seoul_station, zoom_start = 13)

m

raw = pd.read_excel('./data/starbucks_list.xlsx')
raw

for i in raw.index:
    name = raw.loc[i, '매장명']
    lat = raw.loc[i, '위도']
    long = raw.loc[i, '경도']
    shop = raw.loc[i, '매장타입']

    folium.Marker([lat, long], tooltip = name, popup = shop).add_to(m)
m.save('스타벅스지도.html')





