import requests
from bs4 import BeautifulSoup
import time
import sys

##
## define paras

url = 'https://tip.railway.gov.tw/tra-tip-web/tip'
staDic = {}
today = time.strftime('%Y/%m/%d')
sTime = '06:00'
eTime = '12:00'


requestParas = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

##
## main function
def getTripInfo(start_s, end_s):
    resp = requests.get(url, headers = requestParas)
    if resp.status_code != 200:
        print('there is an error：' + url)
        return
    
    soup = BeautifulSoup(resp.text, 'html5lib')
    stations_list = soup.find_all("div", {'class' :'line-inner hr cityHr'})


    for stations in stations_list:
        station_ = stations.ul.find_all('li')
        for station in station_:
            stationName = station.button.text
            stationId = station.button['title']
            staDic[stationName] = stationId
    
    csrf = soup.find(id = 'queryForm').find('input',{'name':'_csrf'})['value']
    formData = {
        'trainTypeList':'ALL',
        'transfer':'ONE',
        'startOrEndTime':'true',
        'startStation':staDic[start_s],
        'endStation':staDic[end_s],
        'rideDate':today,
        'startTime':sTime,
        'endTime':eTime, 
        '_csrf':csrf
    }
    
    queryUrl = soup.find(id='queryForm')['action']
    qResp = requests.post('https://tip.railway.gov.tw'+queryUrl, data=formData, headers = requestParas)

    if qResp.status_code != 200:
        print('there is an error：' + url)
        return

    qSoup = BeautifulSoup(qResp.text, 'html5lib')
    trs = qSoup.find_all('tr', 'trip-column')

    print('\n'+'#'*30)
    print('{} to {} schedule as below'.format(start_s, end_s))
    print('#'*30 + '\n')


    print('車次', '開始時間', '到達時間', '花費時間')
    for tr in trs:
        td = tr.find_all('td')
        print('%s : %s, %s, %s' % (td[0].ul.li.a.text, td[1].text, td[2].text, td[3].text)) 
        

if __name__ == '__main__':
    """test function"""
    getTripInfo('浮洲', '新竹')
