# coding:utf-8
import requests
import json
from lxml import etree
from selenium import webdriver
url = 'https://www.douban.com/j/search_photo?q=麦迪&limit=20&start=0'
html = requests.get(url).text
response = json.loads(html,encoding='utf-8')

def download(src,name):
    dir = './' + name + '.jpg'
    try:
        pic = requests.get(src,timeout=10)
    except Exception:
        print("error,%s 当前图片无法下载" % src)
    fp = open(dir,'wb')
    fp.write(pic.content)
    fp.close()

#下载明星图片
print(response['images'])
for photo in response['images']:
    print(photo['src'])
    download(photo['src'],photo['id'])    

driver = webdriver.Chrome('./chromedriver')
for start in range(0,120,15):
    url = 'https://movie.douban.com/subject_search?search_text='+'周星驰'+'&cat=1002'+'&start='+str(start)
    driver.get(url)
    #print(driver.page_source)
    html = etree.HTML(driver.page_source)
    src_xpath = "//*[@class='item-root']/a/img/@src"
    title_xpath = "//*[@class='item-root']/div[@class='detail']/div[@class='title']/a/text()"
    srcs = html.xpath(src_xpath)
    titles = html.xpath(title_xpath)
    # print(srcs,titles)
    for src,title in zip(srcs,titles):
        print(src,title)
        download(src,title)
driver.close()
