import re

from bs4 import BeautifulSoup
import requests

import json


INN = input('Введите ИНН: ')

BASE_URL = 'https://kad.arbitr.ru'
URL = BASE_URL + '/Kad/SearchInstances'

def get_info(base_url, request_url, inn_data, page):
    'get data from server'

    # get new cookie to emulate new user(avoiding api throttling)
    cookie_rsp = requests.request("POST", base_url).cookies
    cookie_template = '__ddg1_={__ddg1_}; ASP.NET_SessionId={NET_SessionId}; CUID={CUID}; _ga=GA1.2.2007930681.1658848048; _gid=GA1.2.1827432965.1658848048; Notification_All={Notification_All}; tmr_lvid=ca310c0f5371b917a42fcdb6b3494272; tmr_lvidTS=1658848048868; _ym_uid=1658848049165771965; _ym_d=1658848049; _ym_isad=2; pr_fp=130cdccb67bb6124eb9a498809c8cf6452a8e98824b69ffb14e0f712842710a3; rcid=0238718e-ffc8-418c-8902-d0b89cb7e099; _gat=1; _gat_FrontEndTracker=1; _dc_gtm_UA-157906562-1=1; tmr_detect=0%7C1658855979855; tmr_reqNum=34; wasm={wasm}'
    cookie = cookie_template.format(
        __ddg1_=cookie_rsp.get('__ddg1_'),
        NET_SessionId=cookie_rsp.get('ASP.NET_SessionId'),
        CUID=cookie_rsp.get('CUID'),
        Notification_All=cookie_rsp.get('Notification_All'),
        wasm='e448faae41c56172efa31362f6c314b9',
    )
    url = request_url

    payload = json.dumps({
    "Page": page,
    "Count": 25,
    "Courts": [],
    "DateFrom": None,
    "DateTo": None,
    "Sides": [
        {
        "Name": inn_data,
        "Type": -1,
        "ExactMatch": False
        }
    ],
    "Judges": [],
    "CaseNumbers": [],
    "WithVKSInstances": False
    })

    headers = {
    'authority': 'kad.arbitr.ru',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'cookie': cookie,
    'origin': 'https://kad.arbitr.ru',
    'referer': 'https://kad.arbitr.ru/',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'x-date-format': 'iso',
    'x-requested-with': 'XMLHttpRequest'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def parse_page(info):
    soup = BeautifulSoup(info.text, 'html.parser')
    for el in soup.find_all('tr'):
        print('------------------->')

        print('Дата: ', el.find('span').text)
        print('Номер дела:', el.find('a', {'class': 'num_case'}).text.replace('\r\n', '').strip())

        plaintiff_spans = el.find('td', {'class': 'plaintiff'}).find_all('span', 'js-rolloverHtml')
        print('Истец:', [i for i in re.findall(r'<strong>(.+?)</strong>', str(plaintiff_spans))])

        respondents_spans = el.find('td', {'class': 'respondent'}).find_all('span', 'js-rolloverHtml')
        print('Ответчик:', [i for i in re.findall(r'<strong>(.+?)</strong>', str(respondents_spans))])


i = 1
final_flag = False

while not final:
    info = get_info(BASE_URL, URL, INN, i)
    parse_page(info)

    if not info.text:
        final_flag = True
    i += 1
