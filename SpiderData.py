# -*-coding:utf-8 -*-
"""
    时间：2019-6-11
    功能：爬虫：爬取同花顺网站的行情数据
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
FILE_NAME="THS.csv"


class SpiderTHS:
    #访问头
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
              'Accept': 'text/html, */*; q=0.01',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Cookie':'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1560215632; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1560215632; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1560215632; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1560236557; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1560236558; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1560236558; v=AooQ2bhQ4jpkhG6WHf-P9mvY23svewozAPeCbBTCN7dqMiQt_Ate5dCP0o_n',
              'hexin-v':'AooQ2bhQ4jpkhG6WHf-P9mvY23svewozAPeCbBTCN7dqMiQt_Ate5dCP0o_n',
              'Host':'data.10jqka.com.cn',
              'Referer':'http://data.10jqka.com.cn/ipo/xgsgyzq/',
              'X-Requested-With':'XMLHttpRequest'
              }
    URL1 = 'http://data.10jqka.com.cn/ipo/xgsgyzq/' #解析的第一个网站 
    #URL2 = "http://vip.stock.finance.sina.com.cn/corp/go.php/vRPD_NewStockIssue/page/1.phtml" #第二个网站，新浪财经
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_page = 0  #数据页数
        self.current_page = 0 #当前页码
        self.data_url_prefix = "http://data.10jqka.com.cn/ipo/xgsgyzq/board/all/field/SGDATE/page/" #ajax请求数据 前缀+页码+后缀
        self.data_url_suffix ="/order/desc/ajax/1/"
        self.table_header = [] #表头文字
        self.table_data=[]#表中数据，每一行一个list
    
    def GetHeader(self):
        header_list = ['Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
          'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
          'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        ]
       #cookie影响着访问频率，此网址限制这同一个cookie访问的频率
        cookie_list =["Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1559120824,1559121818,1559636913,1560244222; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1560244222; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1560244222; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1560307177; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1560307177; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1560307177; v=AvQ7RvKyFSdpuIFrVChM_mUGxbllzRo7WvKs645Ug2kAFZrvtt3oR6oBfIjd",
                      "Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1560215632; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1560215632; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1560215632; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1560236557; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1560236558; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1560236558; v=AooQ2bhQ4jpkhG6WHf-P9mvY23svewozAPeCbBTCN7dqMiQt_Ate5dCP0o_n",
                      "Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1559120824,1559121818,1559636913,1560244222; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1560244222; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1560244222; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1560307177; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1560307177; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1560307177; v=AuQrNmJiZVcHB5GbJalcDvV2tenVfQ21yqacCv4Ecrxwe4rfJo3YdxqxbL1N",
                      "Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1559120824,1559121818,1559636913,1560244222; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1560244222; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1560244222; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1560319285; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1560319285; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1560319285; ClientInfo=; v=AoRLFsKChXeIlDG72yK8LhVWVQl1nagzasA8S54lEpsQIio_xq14l7rRDNnt",
                      "Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1559120824,1559121818,1559636913,1560244222; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1560244222; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1560244222; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1560319364; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1560319364; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1560319364; v=AluUC1FvguLLUf6WqE1bm7az6rTGMG8NaUUz5k2YNWRz3XWi1QD_gnkUwzRe",
                      "Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1559120824,1559121818,1559636913,1560244222; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1560244222; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1560244222; ClientInfo=; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1560320136; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1560320136; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1560320136; v=AnG-SZ8BiABpjyQUW7qheRDFgPYIXuVNj9OJ6VOGbztV2Z9gm671oB8imbbg",
                      "Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1559120824,1559121818,1559636913,1560244222; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1560244222; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1560244222; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1560320136; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1560320136; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1560320136; v=AkaJSBwYZ1EaVjO1-98eSKNMlzfLp4m-XNS-2TBvMPlGlejhmDfacSx7DpUD",
                      "Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1559120824,1559121818,1559636913,1560244222; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1560244222; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1560244222; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1560320136; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1560320136; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1560320136; v=AhjX0r7-8fsYWN1_mApoUmEy6U2pAX8r3ltQE1IJZr0ETrZ7-hFMGy51IKCh",
                      "Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1559120824,1559121818,1559636913,1560244222; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1560244222; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1560244222; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1560320136; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1560320136; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1560320136; v=Ag_AN-1rjgZ7tYr6i5bnP6LPnqgaNGGn_bVnViEcqUGHVCFeKQTzpg1Y96Qy",
                      "Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1559120824,1559121818,1559636913,1560244222; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1560244222; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1560244222; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1560320136; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1560320136; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1560320136; v=Al2SDSMl3PydU7jQFU119YRpbDJUepArm5T1vB8imFXha3Ok58qhnCv-BUus"
                      
            ]
        return {'User-Agent':random.choice(header_list),
                  'Accept': 'text/html, */*; q=0.01',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Cookie':random.choice(cookie_list),
                  #'hexin-v':'AooQ2bhQ4jpkhG6WHf-P9mvY23svewozAPeCbBTCN7dqMiQt_Ate5dCP0o_n',
                  'Host':'data.10jqka.com.cn',
                  'Referer':'http://data.10jqka.com.cn/ipo/xgsgyzq/',
                  'X-Requested-With':'XMLHttpRequest'
                }


    #获取数据的页数以及表头
    def GetInfo(self):
        http = urllib3.PoolManager()
        contents = http.request("get",SpiderTHS.URL1,headers = self.GetHeader()) 
        soup = BS(contents.data, "lxml")  #解析网页
        pages = soup.find("span",attrs={"class":"page_info"}).get_text()
        self.current_page,self.total_page=pages.split("/")  #获取总页数和当前页数
        #获取表格头
        tag_table = soup.find("table",attrs={"class":"m_table","id":"fixtable"})
        tag_tr = tag_table.find("tr")
        tag_th=tag_tr.find("th")
        texts = tag_tr.text.replace("\n"," ").replace("\xa0"," ")
        textList =texts.split()  #多了一个新股详情
        if "新股详情" in textList:
            textList.remove("新股详情")
        self.table_header = textList
        

    def GetData(self,url):
        while True:
            http = urllib3.PoolManager()
            contents = http.request("get",url,headers = self.GetHeader()) 
            soup = BS(contents.data, "lxml")
            try:
                tag_tbody = soup.find("tbody",attrs={"class":"m_tbd"})
                tag_list = tag_tbody.find_all("tr")
            except:
                interval=random.random()*5
                print("当前爬虫被限制，%ds后继续"%(interval))
                time.sleep(interval)
                continue
            num = 0
            for tag_row in tag_list:            #处理一行数据
                num+=1
                row_list=[]  #保存一行的值
                tag_td_list = tag_row.find_all("td")        #处理标签内每一个值和子标签
                for tag_td in tag_td_list:      #处理一行中的一列，即一个单元格
                    flag = False
                    td_text=""      #一个td一个显示字符
                    temp_text=""
                    for item in tag_td:                       
                        if item.name == 'a':
                            if item.text != "":
                                if flag:
                                    td_text+="|"                           
                                td_text+=item.text.replace("\t"," ").replace("\n"," ").split()[0]
                                flag = True
                        if type(item)==bs4.element.NavigableString:  #td中一个字符串
                            temp_text=item
                            text_list=temp_text.replace("\t"," ").replace("\n"," ").split()
                            if len(text_list)==0:
                                continue
                            if flag:
                                td_text+="|"
                            td_text+=text_list[0]
                            flag = True
                            #print(td_text)
                    #print(td_text) #此处获取每个单元格的值
                    row_list.append(td_text)
                self.table_data.append(row_list)    
                #print("已经获取数据行数：%d"%(num))
            break

    #所有数据获取之后一次存储
    def SaveAll(self,name):          
        out = open(name,'w',newline='') #创建
        csv_write = csv.writer(out,dialect='excel')
        csv_write.writerow(self.table_header)
        csv_write.writerows(self.table_data)
        out.close()
    
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
            #interval=random.random()*5
            #print("interval:%ds"%(interval))
            #time.sleep(interval)
        #print("正在保存数据...")
        #print("数据数量:%d"%(len(self.table_data)))
        #self.SaveAll("THS.csv")
        #print("数据保存完毕")
        print("运行完毕")

if __name__ == "__main__":
    obj = SpiderTHS()
    #obj.GetInfo()
    #obj.GetData("http://data.10jqka.com.cn/ipo/xgsgyzq/board/all/field/SGDATE/page/1/order/desc/ajax/1/index")
    #while True:
    #    print (obj.GetHeader())
    obj.Run()     