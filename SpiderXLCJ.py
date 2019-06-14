#-*- coding:utf-8 -*-

"""
    时间：2019-6-12
    作者：
    描述：爬虫：爬取 新浪财经-新股日历
"""

import requests
import urllib3
from bs4 import BeautifulSoup as BS
import time
import re
import urllib
import csv
import bs4
import random
import datetime


#文件保存的名字
FILE_NAME="XLCJ.csv"


class SpiderXLCJ:
    #访问头
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
              #'Accept': 'text/html, */*; q=0.01',
              #'Accept-Encoding': 'gzip, deflate',
              #'Accept-Language': 'zh-CN,zh;q=0.9',
              #'Cookie':'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1560215632; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1560215632; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1560215632; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1560236557; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1560236558; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1560236558; v=AooQ2bhQ4jpkhG6WHf-P9mvY23svewozAPeCbBTCN7dqMiQt_Ate5dCP0o_n',
              #'hexin-v':'AooQ2bhQ4jpkhG6WHf-P9mvY23svewozAPeCbBTCN7dqMiQt_Ate5dCP0o_n',
              #'Host':'data.10jqka.com.cn',
              #'Referer':'http://data.10jqka.com.cn/ipo/xgsgyzq/',
              #'X-Requested-With':'XMLHttpRequest'
              }
    URL = "http://vip.stock.finance.sina.com.cn/corp/go.php/vRPD_NewStockIssue/page/1.phtml" #第二个网站，新浪财经


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_page = 0  #数据页数
        self.current_page = 0 #当前页码
        self.data_url_prefix = "http://vip.stock.finance.sina.com.cn/corp/view/vRPD_NewStockIssue.php?page=" #请求数据 前缀+页码+后缀
        self.data_url_suffix ="&cngem=0&orderBy=NetDate&orderType=desc"
        self.table_header = [] #表头文字
        self.table_data=[]#表中数据，每一行一个list

    #获取数据的页数以及表头
    def GetInfo(self):
        http = urllib3.PoolManager()
        contents = http.request("get",SpiderXLCJ.URL,headers = SpiderXLCJ.header)
        #soup = BS(contents.data.decode("gbk"), "lxml")  #解析网页
        soup = BS(contents.data, "lxml")
        table = soup.find("table",attrs={"id":"NewStockTable"}) #找到table 第一个是表头，之后是数据
        tag_header = table.find("tr",attrs={"class":"tr_2"})    #表头        
        tag_td_list = tag_header.find_all("td") #列
        for tag_td in tag_td_list:
            #print(tag_td.text)
            self.table_header.append(tag_td.text)
        #获取页数
        table = soup.find("table",attrs={"class":"table2"})
        tag=table.find("td")
        #print(tag.text)
        self.current_page,self.total_page=re.findall(r"\d+\.?\d*",tag.text.replace("\t","").replace("\n","").replace(" ",""))
    
    def GetData(self,url):
        #print(url)
        http = urllib3.PoolManager()
        contents = http.request("post",url,headers = SpiderXLCJ.header)
        #soup = BS(contents.data.decode("gbk"), "lxml")  #解析网页
        soup = BS(contents.data, "lxml")
        table = soup.find("table",attrs={"id":"NewStockTable"}) #找到table 第一个是表头，之后是数据
        tag_tr_list = table.find_all("tr")    #表头
        skip=0  #前三个跳过
        num=0   #统计数量   
        for tag_tr in tag_tr_list:
            skip+=1
            if skip>3:
                num+=1
                templist=tag_tr.text.replace("\xa0","null").replace("\n"," ").replace("\t"," ").replace("*","").split()
                #print(templist)
                self.table_data.append(templist)


    #一页一页存储
    def SavePage(self,name,data_list):          
        out = open(name,'a',newline='') #追加
        csv_write = csv.writer(out,dialect='excel')
        #csv_write.writerow(self.table_header)
        csv_write.writerows(data_list)
        out.close()

    #创建文件
    def CreateFile(self,name):
        out = open(name,'w',newline='') #创建
        csv_write = csv.writer(out,dialect='excel')
        csv_write.writerow(self.table_header)
        #csv_write.writerows(self.table_data)
        out.close()

    def Run(self):
        print("正在获取页数和表头...")
        self.GetInfo()
        print("总页数为：%s"%(self.total_page))
        print("页数和表头获取完毕")

        #date=datetime.datetime.now().strftime('%Y%m%d')
        name = FILE_NAME

        self.CreateFile(name)
        for i in range(1,int(self.total_page)+1):
            print("正在获取数据:第%d页..."%(i))
            self.GetData(self.data_url_prefix+str(i)+self.data_url_suffix) 
            self.SavePage(name,self.table_data)
            self.table_data.clear()
            print("数据保存完毕")
            #time.sleep(3)
        print("运行完毕")


if __name__ == "__main__":
    obj=SpiderXLCJ()
    obj.Run()