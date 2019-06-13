'''
抓取“药帮忙”医药网站的数据，包括药品详情页面的信息，最终输出到csv
'''

from efficient_apriori import apriori
from lxml import etree
import time
from selenium import webdriver
import csv

#抓取搜索页面的数据
def download(request_url):
    #读取网站数据
    driver.get(request_url)
    time.sleep(1)
    html = etree.HTML(driver.page_source)
    #利用xpath获取指定数据
    name_lists = html.xpath('''/html/body/div[2]/ul/li/div[2]/a''')
    company_lists=html.xpath('''/html/body/div[2]/ul/li/div[4]''')
    size_lists=html.xpath('''/html/body/div[2]/ul/li/div[3]''')
    price_lists=html.xpath('''/html/body/div[2]/ul/li/div[5]/span''')
    
    for (company_list, name_list,size_list,price_list) in zip(company_lists, name_lists,size_lists,price_lists):  
        name=name_list.text.split("\n")[1].strip()
        company=company_list.text.split("\n")[1].strip()
        size=size_list.text.split("\n")[1]
        link='''http://www.ybm100.com'''+name_list.attrib['href']
        price=price_list.text
        #将需要的字段进行合并，输出到csv中
        hebing=[]
        hebing.append(name)
        hebing.append(company)
        hebing.append(size)
        hebing.append(link)
        hebing.append(price)
        
        name1, classification, approval_number  =download1(link)
        
        hebing.append(name1)
        hebing.append(classification)
        hebing.append(approval_number)
        
        csv_write.writerow(hebing)
    
#抓取详情页面的数据
def download1(request_url):
    driver.get(request_url)
    time.sleep(1)
    html = etree.HTML(driver.page_source)
    #设定抓取的字段
    name_list = html.xpath('''/html/body/div[2]/div[2]/div[2]/div[1]/span[@class='tit']''')
    classification_list=html.xpath('''//*[@id="categorySecondName"]''')
    approval_number_list=html.xpath('''/html/body/div[2]/div[3]/div[1]/div[1]/div[1]/table/tbody/tr[2]/td[2]''')
    
    name=name_list[0].text
    classification=classification_list[0].text
    approval_number=approval_number_list[0].text
    
    return name,classification,approval_number
    
driver = webdriver.Chrome('./chromedriver')

# 写CSV文件
file_name = './医药数据.csv'
base_url = 'http://www.ybm100.com/search/skuInfo.htm?all=all&categoryFirstId=1&offset='

out = open(file_name,'w', newline='', encoding='utf-8-sig')
csv_write = csv.writer(out, dialect='excel')

#输入列名
columns=['name','company','size','link','price','name1','classification','approval_number']
csv_write.writerow(columns)


#初始化页数编码
start=1
while start<3:
    request_url = base_url + str(start)
    # 下载数据
    download(request_url)
    start+=1


out.close()
print('finish')
