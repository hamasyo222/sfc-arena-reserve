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
from selenium.webdriver.chrome import service as fs
import traceback
import sys



# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def setting_time(event):
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

    print(start, day, start_hour, start_minute, end_hour, end_minute)
    return(start, day, start_hour, start_minute, end_hour, end_minute)


def reserve(start, day):
    try:    
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

        #0:00まで待機
        res_date = start - datetime.timedelta(days=14)
        res_date1 = start - datetime.timedelta(days=15)
        y = res_date.year
        m = res_date.month
        d = res_date.day
        y1 = res_date1.year
        m1 = res_date1.month
        d1 = res_date1.day

        while datetime.datetime.now() < datetime.datetime(y1, m1, d1, 23, 59, 00):
            time.sleep(1)

        #
        # Chromeドライバーの起動
        #
        DRIVER_PATH = '/app/.chromedriver/bin/chromedriver' #heroku
        #DRIVER_PATH = '/Users/hamasyo/Selenium/chromedriver' #ローカル
        chrome_sevice = fs.Service(DRIVER_PATH)
        driver = webdriver.Chrome(service=chrome_sevice, options=options)
        driver.implicitly_wait(20)

        #施設予約システムにアクセス
        driver.get("https://eqres01.adst.keio.ac.jp/")

        #keio.jp認証
        #ID
        driver.find_element(By.CSS_SELECTOR,'#username').send_keys(os.environ['KEIO_ACCOUNT'])#

        #パスワード
        driver.find_element(By.CSS_SELECTOR,'#password').send_keys(os.environ['KEIO_PASSWORD'])#

        #ログイン
        driver.find_element(By.CSS_SELECTOR,'#login > section.form-element-wrapper.login_b > button').click()

        #予約キー
        driver.find_element(By.CSS_SELECTOR,'#main_content > div > div.container_body > form > div > dl > dd > input[type=text]').send_keys('0405241')

        #次へ
        driver.find_element(By.CSS_SELECTOR,'#main_content > div > div.container_body > form > div > dl > button').click()

        #画面遷移

        #期間始まり
        driver.find_element(By.NAME,'s2[reservation_date]').click()
        driver.find_element(By.NAME,'s2[reservation_date]').clear()
        driver.find_element(By.NAME,'s2[reservation_date]').send_keys(day)
        driver.find_element(By.NAME,'s2[reservation_date]').send_keys(Keys.ENTER)

        #期間終わり
        driver.find_element(By.NAME,'s2[reservation_date_to]').send_keys(day)
        driver.find_element(By.NAME,'s2[reservation_date_to]').send_keys(Keys.ENTER)

        #施設の種類
        driver.find_element(By.CSS_SELECTOR,'#main_content > div > div.container_body.top_info > div > div:nth-child(2) > div > form > div > div > div:nth-child(2) > label:nth-child(3) > input').click()

        #施設の種類
        driver.find_element(By.CSS_SELECTOR,'#target_room_id').click()

        #種類
        driver.find_element(By.CSS_SELECTOR,'#s2-control_division_id').click()
        #プルダウン選択
        Select(driver.find_element(By.CSS_SELECTOR,'#s2-control_division_id')).select_by_value("113")

        #プルダウン
        while datetime.datetime.now() < datetime.datetime(y, m, d, 0, 0, 00):
            time.sleep(1)

        #検索
        driver.find_element(By.CSS_SELECTOR,'#main_content > div > div.container_body.top_info > div > div:nth-child(2) > div > form > button').click()

        return(driver)


    except Exception as e:
        error = str(traceback.format_exc()) +"\ " + str(e)
        if len(error) > 950:
            errors = [error[i: i+950] for i in range(0, len(error), 950)]
            for j in range(len(errors)):
                send_line(errors[j])
 

def select_place(event, day, start_hour, start_minute, end_hour, end_minute, driver):
    try:
        if event['location'] == "SFCアリーナ奥":
            arena_back(driver, start_hour, start_minute, end_hour, end_minute)
        elif event['location'] == "SFCアリーナ手前":
            arena_before(driver, start_hour, start_minute, end_hour, end_minute)
        else:
            arena_back(driver, start_hour, start_minute, end_hour, end_minute)
            arena_before(driver, start_hour, start_minute, end_hour, end_minute)
            
    except Exception as e:
        error = str(traceback.format_exc()) +"\ " + str(e)
        if len(error) > 950:
            errors = [error[i: i+950] for i in range(0, len(error), 950)]
            for j in range(len(errors)):
                send_line(errors[j])
    else:
        message = day + " " + start_hour + ":" + start_minute + "〜" + end_hour + ":" + end_minute + event['location'] + "予約完了"
        send_line(message)


#時間選択 アリーナ奥
def arena_back(driver, start_hour, start_minute, end_hour, end_minute):
    driver.find_element(By.CSS_SELECTOR,'#main_content > div.container > div.container_body.noscroll > div.fix_tbl_area.time_table.found-reservable > div.fix_bottom_right > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div.time_cell.relative > label:nth-child(4)').click()
    
    #開始プルダウン
    #時間
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation_start_h')).select_by_value(start_hour)
    #分
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation_start_m')).select_by_value(start_minute)
    #終了プルダウン
    #時間
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation_end_h')).select_by_value(end_hour)
    #分
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation_end_m')).select_by_value(end_minute)

    #実開始プルダウン
    #時間
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(10) > div > div:nth-child(2) > select')).select_by_value(start_hour)
    #分
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(10) > div > div:nth-child(3) > select')).select_by_value(start_minute)

    #実終了プルダウン
    #時間
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(12) > div > div:nth-child(1) > select')).select_by_value(end_hour)
    #分
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(12) > div > div:nth-child(2) > select')).select_by_value(end_minute)

    #名称
    driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(18) > input[type=text]').send_keys('バドミントン練習')

    #人数(塾内)
    driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(20) > div > input:nth-child(1)').clear()
    driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(20) > div > input:nth-child(1)').send_keys('15')

    #e-mail
    driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(30) > div > input[type=text]:nth-child(1)').send_keys('t20651sh@sfc.keio.ac.jp')

    #連絡先
    driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(32) > input[type=text]').send_keys('08014671953')

    #登録する
    driver.find_element(By.CSS_SELECTOR,'#reservation-form > button').click()

    #画面遷移

    #ダイアログ (最終)
    while not driver.find_element(By.CSS_SELECTOR,'body > div:nth-child(20)').is_displayed():
        print("waiting on display")
    driver.find_element(By.CSS_SELECTOR,'body > div:nth-child(20) > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(1)').click()

    #画面遷移
    time.sleep(2)

    #完了確認
    driver.find_element(By.CSS_SELECTOR,'body > div.ui-dialog.ui-corner-all.ui-widget.ui-widget-content.ui-front.ui-dialog-buttons.ui-draggable.ui-resizable > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button').click()

#アリーナ手前の予約
def arena_before(driver, start_hour, start_minute, end_hour, end_minute):
    #時間選択 アリーナ手前
    driver.find_element(By.CSS_SELECTOR,'#main_content > div.container > div.container_body.noscroll > div.fix_tbl_area.time_table.found-reservable > div.fix_bottom_right > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > div.time_cell.relative > label:nth-child(4)').click()
    
    #開始プルダウン
    #時間
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation_start_h')).select_by_value(start_hour)
    #分
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation_start_m')).select_by_value(start_minute)
    #終了プルダウン
    #時間
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation_end_h')).select_by_value(end_hour)
    #分
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation_end_m')).select_by_value(end_minute)

    #実開始プルダウン
    #時間
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(10) > div > div:nth-child(2) > select')).select_by_value(start_hour)
    #分
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(10) > div > div:nth-child(3) > select')).select_by_value(start_minute)

    #実終了プルダウン
    #時間
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(12) > div > div:nth-child(1) > select')).select_by_value(end_hour)
    #分
    Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(12) > div > div:nth-child(2) > select')).select_by_value(end_minute)

    #登録する
    driver.find_element(By.CSS_SELECTOR,'#reservation-form > button').click()

    #画面遷移

    #ダイアログ (最終)
    while not driver.find_element(By.CSS_SELECTOR,'body > div:nth-child(20)').is_displayed():
        print("waiting on display")
    driver.find_element(By.CSS_SELECTOR,'body > div:nth-child(20) > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(1)').click()

    #画面遷移
    time.sleep(2)

    #完了確認
    driver.find_element(By.CSS_SELECTOR,'body > div.ui-dialog.ui-corner-all.ui-widget.ui-widget-content.ui-front.ui-dialog-buttons.ui-draggable.ui-resizable > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button').click()
    


def calender():
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
    #予約の判別
    min = (datetime.datetime.utcnow() + datetime.timedelta(days=14)).isoformat() + 'Z' # 'Z' indicates UTC time
    max = (datetime.datetime.utcnow() + datetime.timedelta(days=15)).isoformat() + 'Z'
    print('Getting the 2weeks later event')
    print(min)
    print(max)
    events_result = service.events().list(calendarId='3442e499hjv4j581l1c68n4v2g@group.calendar.google.com', timeMin=min,
                                        timeMax=max,maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print("予約なし")
    for i in range(events):
        event = events[i]
        if i == 0:
            start, day, start_hour, start_minute, end_hour, end_minute = setting_time(event)
            driver = reserve(start,day)
            select_place(event, day, start_hour, start_minute, end_hour, end_minute, driver)
        else:
            start, day, start_hour, start_minute, end_hour, end_minute = setting_time(event)
            select_place(event, day, start_hour, start_minute, end_hour, end_minute, driver)

            
    #参加確認の判別
    """
    min = (datetime.datetime.utcnow() + datetime.timedelta(days=2)).isoformat() + 'Z' # 'Z' indicates UTC time
    max = (datetime.datetime.utcnow() + datetime.timedelta(days=3)).isoformat() + 'Z'
    print('Getting the 1Days later event')
    print(min)
    print(max)
    events_result = service.events().list(calendarId='3442e499hjv4j581l1c68n4v2g@group.calendar.google.com', timeMin=min,
                                        timeMax=max,maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print("予約なし")
    for event in events:
        attend_line(event)
    """
    


#幹部ライン送る
def send_line(message):
    url = "https://notify-api.line.me/api/notify"
    access_token = os.environ['LINE_NOTIFY_TOKEN']
    headers = {'Authorization': 'Bearer ' + access_token}
    
    message = message
    data = {
        "message": message
    }

    requests.post(
        "https://notify-api.line.me/api/notify",
        headers=headers,
        data=data,
    )


"""
#参加確認ライン送る
def attend_line(event):
    start_str = event['start'].get('dateTime', event['start'].get('date'))
    end_str = event['end'].get('dateTime', event['end'].get('date'))
    start = datetime.datetime.strptime(start_str, '%Y-%m-%dT%H:%M:%S+09:00')
    end = datetime.datetime.strptime(end_str, '%Y-%m-%dT%H:%M:%S+09:00')
    day = start.strftime("%Y/%m/%d")
    start_hour = f'{start.hour:02}'
    start_minute = f'{start.minute:02}'
    end_hour = f'{end.hour:02}'
    end_minute = f'{end.minute:02}'
    url = "https://notify-api.line.me/api/notify"
    access_token = os.environ['Twinkles_TOKEN']
    headers = {'Authorization': 'Bearer ' + access_token}
    try:
        location = event['location']
    except:
        location = ""
    
    message = "\n" + "日付：" + day + "\n" + "時間：" + start_hour + ":" + start_minute + "-" + end_hour + ":" + end_minute + "\n" + "場所：" + location + "\n" + "内容：" + event['summary'] + "\n" + "参加者はこのトークにスタンプお願いします！"
    data = {
        "message": message
    }

    requests.post(
        "https://notify-api.line.me/api/notify",
        headers=headers,
        data=data,
    )


if __name__ == '__main__':
    calender()
"""