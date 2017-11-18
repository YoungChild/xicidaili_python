#! /usr/bin/python
# -*- coding:utf-8 -*-

import random
import requests
import bs4
import xlwt
import time
import fake_useragent


class Items(object):
    IP = None
    Port = None
    Add = None
    Type = None


book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('Agent')

url = 'http://www.xicidaili.com/nn/1'
fa = fake_useragent.UserAgent()
headers = {'User-Agent': fa.random,
          'Referer': 'http://www.xicidaili.com'}
response = requests.get(url, headers=headers)
soup = bs4.BeautifulSoup(response.content, 'lxml')
trs = soup.find_all('tr')
items = []
sum_agent = 0
for tr in trs:
    if tr.find('td'):
        tds = tr.find_all('td')
        item = Items()
        item.IP = tr.find_all('td')[1].get_text().strip()
        item.Port = tr.find_all('td')[2].get_text().strip()
        item.Add = tr.find_all('td')[3].get_text().strip()
        item.Type = tr.find_all('td')[5].get_text().strip()
        sum_agent += 1
        items.append(item)

x = 0
for i in xrange(sum_agent):
    time.sleep(random.random()*3)
    url_test_IP = 'http://www.baidu.com'
    IP = 'http://'+items[i].IP.encode('utf-8')+':'+items[i].Port.encode('utf-8')
    headers = {'User-Agent': fa.random}
    proxies = {'http': IP,
               'https': IP}

    try:
        response_test_IP = requests.get(url_test_IP, proxies=proxies, headers=headers)
    except:
        continue

    if response_test_IP.status_code == 200:
        sheet.write(x, 0, items[i].IP)
        sheet.write(x, 1, items[i].Port)
        sheet.write(x, 2, items[i].Add)
        sheet.write(x, 3, items[i].Type)
        sheet.write(x, 4, 'http://'+items[i].IP.encode('utf-8')+':'+items[i].Port.encode('utf-8'))
        x += 1
    response_test_IP.close()

book.save(time.strftime("%y %b %d", time.localtime())+'.xls')

'''
爬xicidaili.com匿名代理的第一页上的IP地址(0)，端口(1)，服务器地址(2)，类型(3)，设置代理时所用的IP地址(4)    共约100个
所有类型为unicode
均通过'http://www.baidu.com'验证
保存的文件名为 年月日 
'''
