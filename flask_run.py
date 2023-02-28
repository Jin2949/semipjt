#------------------------------------------------
# pip install Flask,  requests
#------------------------------------------------

from flask import Flask, session, render_template, make_response, jsonify, request, redirect, url_for
import cx_Oracle
import random


# 데이터프레임
import numpy as np
import pandas as pd

# 그래프그리기
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
import googlemaps
import geopandas as gpd
import chart_studio.plotly as ply
import chart_studio
import plotly.express as px
# import cufflinks as cf
import plotly.tools as tls
import plotly.graph_objs as go
import sklearn
from sklearn.preprocessing import StandardScaler
chart_studio.tools.set_credentials_file(username='hyungjin2949', api_key='3PFvNSDNm2fakf9xJ1UI')


#정규표현식
import re

#플라스크 및 데이터 관리
import requests
import json

# 크롤링 및 DB생성
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from youtubesearchpython import VideosSearch
from sqlalchemy import create_engine


app = Flask(__name__)
app.secret_key = "1111122222"


@app.route('/')
def index():
    # 중구 3월 주중평균
    junggu_geo = gpd.read_file('./datasets/junggu_geo.geojson')
    junggu_3mm = pd.read_csv('./datasets/버스중구3월.csv')
    junggu_3mm_dong_cnt_wd0 = junggu_3mm[junggu_3mm['wd'] == 0].groupby('dong_id')[['g_cnt']].sum().reset_index()
    junggu_3mm_dong_cnt_wd0['g_cnt_log'] = np.log1p(junggu_3mm_dong_cnt_wd0['g_cnt'])

    junggu_geo['adm_cd'] = junggu_geo['adm_cd'].astype(int)
    junggu_geo = pd.merge(junggu_geo, junggu_3mm_dong_cnt_wd0, how='inner', left_on='adm_cd', right_on='dong_id')
    junggu_geo['총이용객'] = junggu_3mm_dong_cnt_wd0['g_cnt'].astype(int).apply(lambda x: format(x, ','))
    junggu_geo['동이름'] = junggu_geo['temp'].apply(lambda x: x.split(' ')[-1])

    here = [37.560914, 126.990202]
    m1 = folium.Map(location=here, tiles="OpenStreetMap", zoom_start=13)

    folium.GeoJson(junggu_geo).add_to(m1)

    cp1 = folium.Choropleth(
        geo_data=junggu_geo,
        data=junggu_3mm_dong_cnt_wd0,
        columns=['dong_id', 'g_cnt_log'],
        fill_color='GnBu',
        key_on='feature.properties.adm_cd').add_to(m1)

    folium.GeoJsonTooltip(['동이름', '총이용객']).add_to(cp1.geojson)

    # ---------------------------------------------------
    # web browser에 보이기 위한 준비
    # m.get_root().width = "800px"
    # m.get_root().height = "600px"
    html_str1 = m1.get_root()._repr_html_()
    # ---------------------------------------------------

    # 중구 3월 주말평균
    junggu_geo = gpd.read_file('./datasets/junggu_geo.geojson')
    junggu_3mm_dong_cnt_wd1 = junggu_3mm[junggu_3mm['wd'] == 1].groupby('dong_id')[['g_cnt']].sum().reset_index()
    junggu_3mm_dong_cnt_wd1['g_cnt_log'] = np.log1p(junggu_3mm_dong_cnt_wd1['g_cnt'])

    junggu_geo['adm_cd'] = junggu_geo['adm_cd'].astype(int)
    junggu_geo = pd.merge(junggu_geo, junggu_3mm_dong_cnt_wd1, how='inner', left_on='adm_cd', right_on='dong_id')
    junggu_geo['총이용객'] = junggu_geo['g_cnt'].astype(int).apply(lambda x: format(x, ','))
    junggu_geo['동이름'] = junggu_geo['temp'].apply(lambda x: x.split(' ')[-1])

    here = [37.560914, 126.990202]
    m2 = folium.Map(location=here, tiles="OpenStreetMap", zoom_start=13)

    folium.GeoJson(junggu_geo).add_to(m2)

    cp2 = folium.Choropleth(
        geo_data=junggu_geo,
        data=junggu_3mm_dong_cnt_wd1,
        columns=['dong_id', 'g_cnt_log'],
        fill_color='YlOrRd',
        key_on='feature.properties.adm_cd').add_to(m2)
    folium.GeoJsonTooltip(['동이름', '총이용객']).add_to(cp2.geojson)

    # ---------------------------------------------------
    # web browser에 보이기 위한 준비
    # m.get_root().width = "800px"
    # m.get_root().height = "600px"
    html_str2 = m2.get_root()._repr_html_()
    # ---------------------------------------------------


    # 중구 인구
    서울인구 = pd.read_csv('./datasets/gu_dong_population_2022_03.csv', encoding='cp949')
    중구인구 = 서울인구[서울인구['구별'] == '중구']
    중구인구['소계'] = 중구인구['소계'].str.replace(',', '').astype('int')
    population_tot = 중구인구['소계'].sum()
    population_tot = format(population_tot, ',')

    # 중구 3월 버스승객수
    polpulation_bus = junggu_3mm['g_cnt'].sum()
    polpulation_bus = format(polpulation_bus, ',')

    # 날씨 데이터
    apikey = "473c1af10b279e7bfb41d61f2b74b7f0"
    city = "Seoul"
    lang = 'kr'  # 언어
    units = 'metric'  # 화씨 온도를 섭씨 온도로 변경
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units={units}"

    result = requests.get(api)
    result = json.loads(result.text)

    return render_template('index.html', KEY_MYDATA1=html_str1, KEY_MYDATA2=html_str2, weather=result, population_tot=population_tot,
                           polpulation_bus=polpulation_bus)



@app.route("/test")
def test():
    return render_template('test.html')

@app.route('/form_rest_text_text', methods=['GET', 'POST'])
def ajax():
    data = request.get_json()
    print(data)
    return jsonify(result="success", result2=data)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8989)