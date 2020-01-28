#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time

#########################################################
#get all paras#
#########################################################

_url =  'https://www.railway.gov.tw/tra-tip-web/tip'

requestParas = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

sta_id = dict()

##
## define sub-process

def getTripTime(sTime, eTime,sStation, eStation):

    requests_p = requests.get(_url)
    if requests_p.status_code != 200:
        print('there is an error on catching' + _url)
        return 0

    soup = BeautifulSoup(requests_p.text, 'html5lib')
    stations = soup.find(id ='cityHot').ul.find_all('li')

    for s in stations:
        station_name = s.button.text
        stationId = s.button['title']
        sta_id[station_name] = stationId


    #get csrf 
    csrf = soup.find(id = 'queryForm').find('input',{'name':'_csrf'})['value']

    #put everything into formData
    formData = {
        '_csrf':csrf,
        'trainTypeList':'ALL',
        'transfer':'ONE',
        'startOrEndTime':'true',
        'startStation':sta_id[sStation],
        'endStation': sta_id[eStation],
        'rideData':time.strftime('%Y/%m/%d'),
        'startTime': sTime,
        'endTime': eTime
    }

    print(formData)
        
    queryUrl = soup.find(id = 'queryForm')['action']

    # print('打印queryForm', soup.find(id = 'queryForm'))

    qResp = requests.post('https://tip.railway.gov.tw' + queryUrl, data= formData, headers = requestParas)

    if qResp.status_code != 200:
        print('there is an error on catching' + _url)
        return 0

    qSoup = BeautifulSoup(qResp.text, 'html5lib')

    # print('qSoup', qSoup)

    # sys.exit()
    trs = qSoup.find_all('tr', 'trip-column')

    for tr in trs:
        td = tr.find_all('td')
        print('%s : %s , %s'%(td[0].ul.li.a.text, td[1].text, td[2].text ))


"""
_csrf: 7eb5e4b3-0f01-447f-9cdd-aefcff2b1ade
startStation: 0910-三坑
endStation: 4120-新營
transfer: ONE
rideDate: 2020/01/25
startOrEndTime: true
startTime: 00:00
endTime: 23:59
trainTypeList: ALL
query: 查詢
"""

    






if __name__ == "__main__":
    getTripTime('06:00', '16:00', '臺北', '新竹')
    