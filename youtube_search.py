from youtubesearchpython import VideosSearch
import json

검색어 = '중구 명동'

json_res = VideosSearch(검색어,1).result()
print(json_res[])