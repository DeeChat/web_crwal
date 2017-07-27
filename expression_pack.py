# coding:utf-8
import requests
import re
from bs4 import BeautifulSoup
import time
import numpy as np
from urllib import request
import os

# get new urls
def getUrls(html):
    '''
    get the urls in html page
    :param html: html page
    :return: urls in html page, and url contains some .gif img
    '''
    new_urls = []
    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.find_all('a', target = "_blank")
    for url in urls:
        url = url.get('href')                                               # get the url
        if url[-4:] == 'html':
            new_urls.append(url)
    return new_urls


# get HTML Text
def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 60)                                  # 向服务器发送请求
        r.raise_for_status()                                                 # 若状态码 != 200， 抛出异常
        r.encoding = r.apparent_encoding                                     # utf-8 编码
        return r.text                                                        # 返回文本内容
    except:
        return ''

# 解析页面,得到第i
def parsePage(html,i,j):
    '''
    对HTML页面进行解析, 并将gif保存至本地
    :param html: html page
    :param i: the i-th folder
    :param j: the j-th url in i-th page
    :return: None
    '''
    try:
        soup = BeautifulSoup(html, 'html.parser')
        urls = soup.find_all('img')
        for k,url in enumerate(urls):                                                  # k-th gif
            url = url.get('data-original')
            if url != None:
                request.urlretrieve(url, 'result'+str(i)+'/'+str(j)+'_'+str(k)+'.gif')
                print('save the {}_{}-th img'.format(j,k))
                time.sleep(np.random.randint(10,15))
    except:
        return None




if __name__ == '__main__':
    num_pages = 32                                                                      # 抓取的页面数
    for i in range(1,num_pages+1):
        if not os.path.isdir('result' + str(i)):
            os.mkdir('result' + str(i))
        print('processing:{}, {}% finished.'.format(i,i/float(num_pages/100)))
        try:
            url = 'http://www.wxcha.com/biaoqing/dongtai/update_' + str(i) + '.html'    # 对应的url链接
            html = getHTMLText(url)                                                     # 得到HTML页面
            urls = getUrls(html)
            for j,url in enumerate(urls):
                html = getHTMLText(url)                                                 # 得到HTML页面
                parsePage(html,i,j)                                                      # 对HTML页面进行解析, 并将gif保存至本地
                time.sleep(10,20)
        except:
            continue

        sleeptime = np.random.randint(30,60)                                            # 防止频繁访问
        time.sleep(sleeptime)