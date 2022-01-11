# -*- coding: utf-8 -*-

#导包,发起请求使用urllib库的request请求模块
import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import json


#待获取数据
links={}
drugs={}
file_name = 'drug_names.json'


# 1、获取下载URLs
#向URL发请求,返回响应对象
url = 'https://www.drugs.com/international/'
response = urllib.request.urlopen(url)

#提取响应内容
html_doc = response.read().decode('utf-8')
#print(html_doc)
soup=BeautifulSoup(html_doc,'html.parser')

#解析获得URL请求页面列表
list_page = soup.find_all('a',href=re.compile('/international-'))
#print(list_page, end="\n")
for link in list_page:
    link_name = str(link.get('href'))[1:-5]
    link_href = str(link.get('href'))
    links[link_name] = link_href
    #print(link_name, link_href)


# 2、获取药物名
url_base = 'https://www.drugs.com'
def get_names(url):
    print(url)
    # 向URL发请求,返回响应对象
    response = urllib.request.urlopen(url)
    #提取响应内容
    html_doc = response.read().decode('utf-8')
    #print(html_doc)
    soup=BeautifulSoup(html_doc,'html.parser')
    #解析获得drug列表
    list_drugs = soup.find_all('a',href=re.compile(r'^/international/(.*?)\.html$')) 
    #print(list_drugs)
    
    for drug in list_drugs:
        drug_name = str(drug.string)
        drug_href = url_base + str(drug.get('href'))
        drugs[drug_name] = drug_href
        print(drug_name, drug_href)


for link_href in links.values():
    get_names(url_base+link_href)

print(drugs,end="\n")
jsonStr = json.dumps(drugs)
print(jsonStr)

with open(file_name, 'w') as f:
    json.dump(jsonStr, f)

# Read JSON file
with open(file_name) as f:
    drug_loaded = json.load(f)

print(jsonStr == drug_loaded)