#------------------------------------------------
# pip install Flask,  requests
#------------------------------------------------

from flask import Flask, session, render_template, make_response, jsonify, request, redirect, url_for
import cx_Oracle
import random

app = Flask(__name__)
app.secret_key = "1111122222"


@app.route('/')
def index():
    # session['MY_TEL_SESSION'] = tel
    # session.pop('MY_TEL_SESSION')
    return render_template('index.html')

@app.route('/form_get', methods=['GET'])
def form_get():
    id = request.args.get("userid")
    pw = request.args.get("userpw")
    print("id:", id)
    print("pw:", pw)
    return render_template('result.html', KEY_MYDATA=[id, pw])
    # ------------html---------
    # {{KEY_MYDATA[0]}}
    # {{KEY_MYDATA[1]}}

@app.route('/form_post', methods=['POST'])
def form_post():
    id = request.form.get("userid")
    pw = request.form.get("userpw")
    var_list_dict = [{"KID": id, "KPW": pw},
                     {"KID": "kim", "KPW": 111},
                     {"KID": "park", "KPW": 222}]

    return render_template('result.html', KEY_MYDATA=var_list_dict)


@app.route('/form_rest_text_text', methods=['POST'])
def form_rest_text_text():
    id = request.form.get("userid")
    print("id:", id)
    return "나 서버야 내가 줄께"

@app.route('/form_rest_json_text', methods=['POST'])
def form_rest_json_text():
    dic = request.get_json()
    print(dic)
    return "나 서버야 내가 줄께"


@app.route('/form_rest_json_json', methods=['POST'])
def form_rest_json_json():
    dic = request.get_json()
    print(dic)
    return jsonify( {"msg" : "나 서버야 내가 줄께"} )

@app.route('/form_rest_uri/<prm1>/<prm2>', methods=['POST'])
def form_rest_uri(prm1, prm2):
    print(prm1, prm2)
    return "나 서버야 내가 줄께"



import pandas as pd
import numpy as np
import folium
from folium import plugins
import re
import googlemaps
import pprint

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import re
import pprint

import folium
from folium.plugins import MarkerCluster
import googlemaps
import geopandas as gpd

import requests
import json


@app.route("/map")
def map():
    bus_time_table = pd.read_csv('./datasets/bus_time_table.csv', encoding='cp949', sep=',', parse_dates=['기준_날짜'])
    del_idx = bus_time_table[bus_time_table.isna().values == True].index
    bus_time_table = bus_time_table.drop(del_idx, axis=0)



    bus = pd.DataFrame()
    bus['busdate'] = bus_time_table['기준_날짜']
    bus['yy'] = bus_time_table['기준_날짜'].dt.year
    bus['mm'] = bus_time_table['기준_날짜'].dt.month
    bus['dd'] = bus_time_table['기준_날짜'].dt.day
    bus['dong_id'] = bus_time_table['행정동_ID']
    bus['guest_cnt'] = bus_time_table['버스_승객_수']
    bus[['hh00', 'hh01',
         'hh02', 'hh03', 'hh04', 'hh05',
         'hh06', 'hh07', 'hh08', 'hh09',
         'hh10', 'hh11', 'hh12', 'hh13',
         'hh14', 'hh15', 'hh16', 'hh17',
         'hh18', 'hh19', 'hh20', 'hh21',
         'hh22', 'hh23']] = bus_time_table[['버스_승객_수_00시', '버스_승객_수_01시',
                                            '버스_승객_수_02시', '버스_승객_수_03시', '버스_승객_수_04시', '버스_승객_수_05시',
                                            '버스_승객_수_06시', '버스_승객_수_07시', '버스_승객_수_08시', '버스_승객_수_09시',
                                            '버스_승객_수_10시', '버스_승객_수_11시', '버스_승객_수_12시', '버스_승객_수_13시',
                                            '버스_승객_수_14시', '버스_승객_수_15시', '버스_승객_수_16시', '버스_승객_수_17시',
                                            '버스_승객_수_18시', '버스_승객_수_19시', '버스_승객_수_20시', '버스_승객_수_21시',
                                            '버스_승객_수_22시', '버스_승객_수_23시']].astype('int')

    bus_mm03 = bus[(bus['dong_id'] // 100 == 11020) & (bus['mm'] == 3)].sort_values(['busdate'])

    bus_mm03_totcnt = bus_mm03.groupby('dong_id')[['guest_cnt']].sum().reset_index()

    state_geo = gpd.read_file('./datasets/seoul_geo_dong.geojson')
    junggu_geo = state_geo[state_geo['adm_cd'].astype('int') // 100 == 11020]

    here = [37.560914, 126.990202]
    m = folium.Map(location=here, tiles="OpenStreetMap", zoom_start=14)

    folium.GeoJson(junggu_geo).add_to(m)

    m.choropleth(
        geo_data=junggu_geo,
        data=bus_mm03_totcnt,
        columns=['dong_id', 'guest_cnt'],
        key_on='feature.properties.adm_cd')

    # ---------------------------------------------------
    # web browser에 보이기 위한 준비
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    html_str = m.get_root()._repr_html_()
    # ---------------------------------------------------

    return render_template('result_map.html'
                           , KEY_MYDATA=html_str)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=7878)