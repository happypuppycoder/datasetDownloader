# -*- coding: utf-8 -*-
from urllib import parse
import requests
import time
#查询药id的url
url_id ="https://api.who-umc.org/vigibase/icsrstatistics/dimensions/drug?tradename="
#查询分级Id的url
url_drug="https://api.who-umc.org/vigibase/icsrstatistics/distributions?agegroupFilter=&continentFilter=&reactionFilter=&sexFilter=&substanceFilter="
#不良反应信息的url,两部分组成
url_info_1="https://api.who-umc.org/vigibase/icsrstatistics/distributions/reactions/preferredterms?agegroupFilter=&continentFilter=&reactionFilter="
url_info_2="&resultLimit=50&resultStart=0&sexFilter=&substanceFilter="


#浏览器里的headers
headers={
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Authorization": "Basic VmlnaUJhc2VBY2Nlc3NDbGllbnQ6cHN3ZDRWaUE=",
    "Connection": "keep-alive",
    "Host": "api.who-umc.org",
    "Origin": "http://www.vigiaccess.org",
    "Referer": "http://www.vigiaccess.org/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "umc-client-key": "6d851d41-f558-4805-a9a6-08df0e0e414b",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
}


#抓取药品Id
def crawlDrugId(url):
    try:
        data=requests.get(url=url,headers=headers,timeout=10)
        print("抓取药品Id连接服务器状态：",data)
        drug_id=data.json()[0]["Code"]
        return drug_id
    except:
        return ""

#抓取分级Id
def scaleId(url):
    try:
        data=requests.get(url=url,headers=headers,timeout=10)
        print("抓取分级Id连接服务器状态：",data)
        data=data.json()["AdrObservations"]
        scale=[]
        #scale={}
        for i in data:
            # Group=i["Group"]
            GroupId = i["GroupId"]
            # NumberOfReports=i["NumberOfReports"]
            # scale[Group]=GroupId
            scale.append(GroupId)
        return scale
    except:
        return ""

#抓取不良反应信息
def crawlAdrInfo(url):
    try:
        data=requests.get(url=url,headers=headers,timeout=10)
        print("抓取不良反应信息连接服务器状态：",data)
        data=data.json()["Observations"]
        adr_info={}
        for i in data:
            Group=i["Group"]
            NumberOfReports=i["NumberOfReports"]
            adr_info[Group]=NumberOfReports
        return adr_info
    except:
        return ""


def main(drugList):
    data=[]
    for i in range(len(drugList)):
        drugName=drugList[i]
        new_url_id = url_id + drugName   #拼接url
        drug_id = crawlDrugId(new_url_id) #抓取药品Id
        time.sleep(1)
        drug_id = parse.quote(drug_id)   #将数据进行url编码
        new_url_drug = url_drug + drug_id#拼接url
        scale = scaleId(new_url_drug)#抓取分级页Id
        time.sleep(1)
        adr_info_all = {}
        for s in scale:
            s = parse.quote(s)  #将数据进行url编码
            url_info = url_info_1 + s + url_info_2 + drug_id#拼接url
            adr_info = crawlAdrInfo(url_info)#抓取不良反应信息
            time.sleep(1)
            adr_info_all.update(adr_info)
        #print(adr_info_all)
        data.append(adr_info_all)
        
        # 保存 ADR 信息到文件
        jsonStr = json.dumps(data)
        with open(file_adr, 'w') as f: json.dump(jsonStr, f)
        print(jsonStr)
    return data

import json
file_drug_names = 'drug_names.json'
file_adr = 'adr.json'

if __name__=="__main__":
    start_time = time.time()    
    # Read JSON file
    with open(file_drug_names) as f: drugs_json = json.load(f)
    drugs = json.loads(drugs_json)
    print(drugs.keys())
    #drug=["Acustop Cataplasma"]
    data=main(list(drugs.keys()))
    print(data)
    print("successful,任务完成！！")
    end_time = time.time()
    uesd_time = end_time - start_time
    print("总用时：", uesd_time)