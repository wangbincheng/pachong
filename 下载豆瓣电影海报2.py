#环境：Mac Python3
# coding:utf-8
import requests
import json
import os
from lxml import etree
from selenium import webdriver

query = '张柏芝'
downloadPath = './'

''' 下载图片 '''
def download(src, id):
    dir = downloadPath + str(id) + '.jpg'
    try:
        pic = requests.get(src, timeout=10)
    except requests.exceptions.ConnectionError:
    # print 'error, %d 当前图片无法下载', %id
        print('图片无法下载')
    if not os.path.exists(downloadPath):
        os.mkdir(downloadPath)
    if os.path.exists(dir):
        print('已存在:'+ id)
        return
    fp = open(dir, 'wb')
    fp.write(pic.content)
    fp.close()

    
def searchImages():
    ''' for 循环 请求全部的 url '''
    for i in range(0, 22471, 20):
        url = 'https://www.douban.com/j/search_photo?q='+query+'&limit=20&start='+str(i)
        html = requests.get(url).text # 得到返回结果
        print('html:'+html)
        response = json.loads(html,encoding='utf-8') # 将 JSON 格式转换成 Python 对象
        for image in response['images']:
            print(image['src']) # 查看当前下载的图片网址
            download(image['src'], image['id']) # 下载一张图片

def getMovieImages():
    url = 'https://movie.douban.com/subject_search?search_text='+ query +'&cat=1002'
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    html = etree.HTML(driver.page_source)
    # 使用xpath helper, ctrl+shit+x 选中元素，如果要匹配全部，则需要修改query 表达式
    src_xpath = "//div[@class='item-root']/a[@class='cover-link']/img[@class='cover']/@src"
    title_xpath = "//div[@class='item-root']/div[@class='detail']/div[@class='title']/a[@class='title-text']"

    srcs = html.xpath(src_xpath)
    titles = html.xpath(title_xpath)
    for src, title in zip(srcs, titles):
        print('\t'.join([str(src),str(title.text)]))
        download(src, title.text)

    driver.close()

getMovieImages()
