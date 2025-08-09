import requests
import pandas as pd
import datetime as dt
import json
data = []
url = "https://api.cnyes.com/media/api/v1/newslist/category/headline" #新聞連結
payload = {
    "page":1,
    "limit":30,
    "isCategoryHeadline":1,
    "startAt": int((dt.datetime.today() - dt.timedelta(days=10)).timestamp()),
    "endAt":int(dt.datetime.today().timestamp())
} #參數
res = requests.get(url, params = payload) #連線鉅亨網, 先抓一次以取得last_page
jd = json.loads(res.text) #解析JSON轉成dict
data.append(pd.DataFrame(jd['items']['data'])) #取出新聞資料

for i in range(2, jd['items']['last_page'] + 1):
    payload["page"] = i
    res = requests.get(url, params = payload) #連線鉅亨網
    jd = json.loads(res.text) #解析JSON轉成dict
    data.append(pd.DataFrame(jd['items']['data'])) #取出新聞資料

df = pd.concat(data, ignore_index = True) #取出新聞資料
df = df[['newsId', 'title', 'summary']]#取出特定欄位
df['link'] = df['newsId'].apply(lambda  x: 'https://m.cnyes.com/news/id/' + str(x))#建立連結
df.to_csv('news.csv', encoding = 'utf-8-sig')
print(df)
