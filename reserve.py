# -*- coding: utf-8 -*-
from __future__ import print_function
import requests
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains



# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def calender(mes1):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    min = (datetime.datetime.utcnow() + datetime.timedelta(days=14)).isoformat() + 'Z' # 'Z' indicates UTC time
    max = (datetime.datetime.utcnow() + datetime.timedelta(days=15)).isoformat() + 'Z'
    print('Getting the 2weeks later event')
    events_result = service.events().list(calendarId='3442e499hjv4j581l1c68n4v2g@group.calendar.google.com', timeMin=min,
                                        timeMax=max,maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        mes2 = datetime.datetime.utcnow()
        reserve(event, mes1, mes2)

        


def reserve(event, mes1, mes2):
    #ここから操作のための定義
    start_str = event['start'].get('dateTime', event['start'].get('date'))
    end_str = event['end'].get('dateTime', event['end'].get('date'))
    start = datetime.datetime.strptime(start_str, '%Y-%m-%dT%H:%M:%S+09:00')
    end = datetime.datetime.strptime(end_str, '%Y-%m-%dT%H:%M:%S+09:00')
    day = start.strftime("%Y/%m/%d")
    start_hour = f'{start.hour:02}'
    start_minute = f'{start.minute:02}'
    end_hour = f'{end.hour:02}'
    end_minute = f'{end.minute:02}'
    true_start_hour = f'{(start + datetime.timedelta(minutes=5)).hour:02}'
    true_start_minute = f'{(start + datetime.timedelta(minutes=5)).minute:02}'
    true_end_hour = f'{(end + datetime.timedelta(minutes=5)).hour:02}'
    true_end_minute = f'{(end - datetime.timedelta(minutes=5)).minute:02}'

    print(start, day, start_hour, start_minute, end_hour, end_minute, true_start_minute, true_end_minute)


    # 操作する
    #
    # Seleniumをあらゆる環境で起動させるオプション
    #
    options = Options()
    options.add_argument('--disable-gpu');
    options.add_argument('--disable-extensions');
    options.add_argument('--proxy-server="direct://"');
    options.add_argument('--proxy-bypass-list=*');
    options.add_argument('--start-maximized');
    options.add_argument('--headless'); # ※ヘッドレスモードを使用する場合、コメントアウトを外す


    #
    # Chromeドライバーの起動
    #
    DRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    driver.implicitly_wait(20)

    #施設予約システムにアクセス
    driver.get("https://eqres01.adst.keio.ac.jp/")

    ##1秒待つ
    ##time.sleep(1)

    ##keio.jp認証有無(遷移確認)
    ##if "https://auth.keio.jp/idp/profile/SAML2/Redirect/SSO" in driver.current_url:
    #ID
    driver.find_element_by_css_selector('#username').send_keys('hamasyo222@keio.jp')

    #パスワード
    driver.find_element_by_css_selector('#password').send_keys('Konnitiwa196')

    #ログイン
    driver.find_element_by_css_selector('#login > section.form-element-wrapper.login_b > button').click()

    ##1秒待つ
    ##time.sleep(1)

    ##予約キー有無
    ##if driver.current_url == "https://eqres01.adst.keio.ac.jp/reservaion-key":
    #予約キー
    driver.find_element_by_css_selector('#main_content > div > div.container_body > form > div > dl > dd > input[type=text]').send_keys('0405241')

    #次へ
    driver.find_element_by_css_selector('#main_content > div > div.container_body > form > div > dl > button').click()

    #画面遷移

    #今日の日付取得(操作前定義で行なっているためスキップ)
    #today = datetime.date.today()
    #two_weeks_lator = today + datetime.timedelta(days=14)
    #two_weeks_lator = two_weeks_lator.strftime("%Y/%m/%d")


    #期間始まり
    driver.find_element_by_name('s2[reservation_date]').click()
    driver.find_element_by_name('s2[reservation_date]').clear()
    driver.find_element_by_name('s2[reservation_date]').send_keys(day)
    #期間終わり
    driver.find_element_by_name('s2[reservation_date_to]').send_keys(day)

    #施設の種類
    driver.find_element_by_css_selector('#main_content > div > div.container_body.top_info > div > div:nth-child(2) > div > form > div > div > div:nth-child(2) > label:nth-child(3) > input').click()

    #種類
    #driver.find_element_by_css_selector('#s2-control_division_id').click()
    #プルダウン選択
    Select(driver.find_element_by_css_selector('#s2-control_division_id')).select_by_value("113")

    #検索
    driver.find_element_by_css_selector('#main_content > div > div.container_body.top_info > div > div:nth-child(2) > div > form > button').click()

    #画面遷移

    #時間選択 アリーナ奥
    driver.find_element_by_css_selector('#main_content > div.container > div.container_body.noscroll > div.fix_tbl_area.time_table.found-reservable > div.fix_bottom_right > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div.time_cell.relative > label:nth-child(61)').click()

    #開始プルダウン
    #時間
    Select(driver.find_element_by_css_selector('#reservation_start_h')).select_by_value(start_hour)
    #分
    Select(driver.find_element_by_css_selector('#reservation_start_m')).select_by_value(start_minute)
    #終了プルダウン
    #時間
    Select(driver.find_element_by_css_selector('#reservation_end_h')).select_by_value(end_hour)
    #分
    Select(driver.find_element_by_css_selector('#reservation_end_m')).select_by_value(end_minute)

    #実開始プルダウン
    #時間
    Select(driver.find_element_by_css_selector('#reservation-form > dl > dd:nth-child(10) > div > div:nth-child(2) > select')).select_by_value(true_start_hour)
    #分
    Select(driver.find_element_by_css_selector('#reservation-form > dl > dd:nth-child(10) > div > div:nth-child(3) > select')).select_by_value(true_start_minute)

    #実終了プルダウン
    #時間
    Select(driver.find_element_by_css_selector('#reservation-form > dl > dd:nth-child(12) > div > div:nth-child(1) > select')).select_by_value(true_end_hour)
    #分
    Select(driver.find_element_by_css_selector('#reservation-form > dl > dd:nth-child(12) > div > div:nth-child(2) > select')).select_by_value(true_end_minute)

    #名称
    driver.find_element_by_css_selector('#reservation-form > dl > dd:nth-child(18) > input[type=text]').send_keys('バドミントン練習')

    #人数(塾内)
    driver.find_element_by_css_selector('#reservation-form > dl > dd:nth-child(20) > div > input:nth-child(1)').clear()
    driver.find_element_by_css_selector('#reservation-form > dl > dd:nth-child(20) > div > input:nth-child(1)').send_keys('15')

    #e-mail
    driver.find_element_by_css_selector('#reservation-form > dl > dd:nth-child(30) > div > input[type=text]:nth-child(1)').send_keys('t20651sh@sfc.keio.ac.jp')

    #連絡先
    driver.find_element_by_css_selector('#reservation-form > dl > dd:nth-child(32) > input[type=text]').send_keys('08014671953')

    #登録する
    driver.find_element_by_css_selector('#reservation-form > button').click()

    #画面遷移

    #ダイアログ (最終)
    while not driver.find_element_by_css_selector('body > div:nth-child(20)').is_displayed():
        print("waiting on display")
    driver.find_element_by_css_selector('body > div:nth-child(20) > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(1)').click()
    mes3 = datetime.datetime.utcnow()
    send_line(day, start_hour, start_minute, end_hour, end_minute, mes1, mes2, mes3)


    #main_content > div.container > div.container_body.noscroll > div.fix_tbl_area.time_table.found-reservable > div.fix_bottom_right > div > div > table > tbody > tr:nth-child(1)行 > td:nth-child(2) > div.time_cell.relative > label:nth-child(4)
    #main_content > div.container > div.container_body.noscroll > div.fix_tbl_area.time_table.found-reservable > div.fix_bottom_right > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div.time_cell.relative > label:nth-child(4)
    #main_content > div.container > div.container_body.noscroll > div.fix_tbl_area.time_table.found-reservable > div.fix_bottom_right > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div.time_cell.relative > label:nth-child(3)時間


        #ライン送るで
def send_line(day, start_hour, start_minute, end_hour, end_minute, mes1, mes2, mes3):
    url = "https://notify-api.line.me/api/notify"
    access_token = os.environ['LINE_NOTIFY_TOKEN']
    headers = {'Authorization': 'Bearer ' + access_token}
    
    message = day + " " + start_hour + ":" + start_minute + "〜" + end_hour + ":" + end_minute + "予約完了"
    data = {
        "message": message + str(mes1) + str(mes2) + str(mes3)
    }

    requests.post(
        "https://notify-api.line.me/api/notify",
        headers=headers,
        data=data,
    )



if __name__ == '__main__':
    mes1 = datetime.datetime.utcnow()
    calender(mes1)
    