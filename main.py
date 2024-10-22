# -*- coding: utf-8 -*-
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


keio_id = os.environ["KEIO_ID"]
keio_pass = os.environ["KEIO_PASS"]
tell = os.environ["TELL"]
line_token = "np51SvAnnMw6ay84USPZhMZb44G0YSAuLRjxYbAYupo"# os.environ["NOTIFY_TOKEN"]
twin_token = "np51SvAnnMw6ay84USPZhMZb44G0YSAuLRjxYbAYupo" #ツイン全体 os.environ["TWIN_TOKEN"]



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
    # 操作する
    #
    # Seleniumをあらゆる環境で起動させるオプション
    #
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--proxy-server="direct://"')
    options.add_argument('--proxy-bypass-list=*')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless') # ※ヘッドレスモードを使用する場合、コメントアウトを外す
    options.binary_location = os.getcwd() + "/bin/headless-chromium"
    
    
    
    """
    #0:00まで待機
    res_date = start - datetime.timedelta(days=15)
    y = res_date.year
    m = res_date.month
    d = res_date.day

    while datetime.datetime.utcnow() < datetime.datetime(y, m, d, 15, 00, 00):
        time.sleep(1)
    """

    #
    # Chromeドライバーの起動
    #
    print("ドライバー起動")

    #DRIVER_PATH = '/app/.chromedriver/bin/chromedriver' #heroku
    #DRIVER_PATH = '/Users/hamasyo/Selenium/chromedriver' #ローカル
    #get_driver = GetChromeDriver()
    #get_driver.install()
    #chrome_sevice = fs.Service(DRIVER_PATH)
    #driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome(service=chrome_sevice, options=options)
    driver = webdriver.Chrome(os.getcwd() + "/bin/chromedriver", options=options)
    driver.implicitly_wait(20)

    #施設予約システムにアクセス
    driver.get("https://eqres01.adst.keio.ac.jp/")

    #keio.jp認証
    #ID
    driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div/div/div[2]/form/div[1]/div[3]/div/div[2]/span/input').send_keys(keio_id)

    #次へ
    driver.find_element(By.CSS_SELECTOR,'#form20 > div.o-form-button-bar > input').click()

    #パスワード
    driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/main/div[2]/div/div/div[2]/form/div[1]/div[3]/div/div[2]/span/input').send_keys(keio_pass)#

    #確認
    driver.find_element(By.CSS_SELECTOR,'#form45 > div.o-form-button-bar > input').click()

    #予約キー
    driver.find_element(By.CSS_SELECTOR,'#main_content > div > div.container_body > form > div > dl > dd > input[type=text]').send_keys('0405241')

    time.sleep(1)
    
    #次へ
    driver.find_element(By.CSS_SELECTOR,'#main_content > div > div.container_body > form > div > dl > button').click()

    #画面遷移

    #期間始まり
    time.sleep(1)
    
    driver.find_element(By.NAME,'s2[reservation_date]').click()
    driver.find_element(By.NAME,'s2[reservation_date]').clear()
    driver.find_element(By.NAME,'s2[reservation_date]').send_keys(day)
    driver.find_element(By.NAME,'s2[reservation_date]').send_keys(Keys.ENTER)
    
    #期間終わり
    driver.find_element(By.NAME,'s2[reservation_date_to]').send_keys(day)
    driver.find_element(By.NAME,'s2[reservation_date_to]').send_keys(Keys.ENTER)

    time.sleep(1)
    #施設の種類
    driver.find_element(By.CSS_SELECTOR,'#main_content > div > div.container_body.top_info > div > div:nth-child(2) > div > form > div > div > div:nth-child(2) > label:nth-child(3) > input').click()

    time.sleep(1)
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
 

def select_place(event, day, start_hour, start_minute, end_hour, end_minute, driver, n):
    if event['location'] == "SFCアリーナ奥":
        n = arena_back(driver, start_hour, start_minute, end_hour, end_minute, n)
    elif event['location'] == "SFCアリーナ手前":
        n = arena_before(driver, start_hour, start_minute, end_hour, end_minute, n)
    else:
        n = arena_back(driver, start_hour, start_minute, end_hour, end_minute, n)
        n = arena_before(driver, start_hour, start_minute, end_hour, end_minute, n)

    message = day + " " + start_hour + ":" + start_minute + "〜" + end_hour + ":" + end_minute + event['location'] + "予約完了"
    send_line(message)
    return n


#時間選択 アリーナ奥
def arena_back(driver, start_hour, start_minute, end_hour, end_minute, n):
    driver.find_element(By.CSS_SELECTOR,'#main_content > div.container > div.container_body.noscroll > div.fix_tbl_area.time_table.found-reservable > div.fix_bottom_right > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div.time_cell.relative > label:nth-child(66)').click()
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

    if n == 0:
        detail(driver)

    #登録する
    driver.find_element(By.CSS_SELECTOR,'#reservation-form > button').click()

    #画面遷移

    #ダイアログ (最終)
    while not driver.find_element(By.CSS_SELECTOR,'body > div:nth-child(20)').is_displayed():
        print("waiting on display")
    driver.find_element(By.CSS_SELECTOR,'body > div:nth-child(20) > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(1)').click()

    #画面遷移
    time.sleep(3)

    #完了確認
    driver.find_element(By.CSS_SELECTOR,'body > div.ui-dialog.ui-corner-all.ui-widget.ui-widget-content.ui-front.ui-dialog-buttons.ui-draggable.ui-resizable > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button').click()
    n += 1
    return n

#アリーナ手前の予約
def arena_before(driver, start_hour, start_minute, end_hour, end_minute, n):
    #時間選択 アリーナ手前
    driver.find_element(By.CSS_SELECTOR,'#main_content > div.container > div.container_body.noscroll > div.fix_tbl_area.time_table.found-reservable > div.fix_bottom_right > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > div.time_cell.relative > label:nth-child(66)').click()
    
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

    if n == 0:
        detail(driver)

    #登録する
    driver.find_element(By.CSS_SELECTOR,'#reservation-form > button').click()

    #画面遷移

    #ダイアログ (最終)
    while not driver.find_element(By.CSS_SELECTOR,'body > div:nth-child(20)').is_displayed():
        print("waiting on display")
    driver.find_element(By.CSS_SELECTOR,'body > div:nth-child(20) > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(1)').click()

    #画面遷移
    time.sleep(3)

    #完了確認
    driver.find_element(By.CSS_SELECTOR,'body > div.ui-dialog.ui-corner-all.ui-widget.ui-widget-content.ui-front.ui-dialog-buttons.ui-draggable.ui-resizable > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button').click()
    
    n += 1
    return n

def detail(driver):
    #名称
    driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(18) > input[type=text]').send_keys('バドミントン練習')

    #人数(塾内)
    driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(20) > div > input:nth-child(1)').clear()
    driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(20) > div > input:nth-child(1)').send_keys('25')

    #e-mail
    driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(30) > div > input[type=text]:nth-child(1)').send_keys(keio_id)

    #連絡先
    driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(32) > input[type=text]').send_keys(tell)


def calender():
    try:
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
            #with open('token.pickle', 'wb') as token:
                #pickle.dump(creds, token)
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        #予約の判別
        min = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        max = (datetime.datetime.utcnow() + datetime.timedelta(days=15)).isoformat() + 'Z'

        print('Getting the 2weeks later event')
        print(min)
        print(max)
        events_result = service.events().list(calendarId='3442e499hjv4j581l1c68n4v2g@group.calendar.google.com', timeMin=min,
                                            timeMax=max,maxResults=9999, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print("予約なし")
        else:
            n = 0
            for event in events:
                start, day, start_hour, start_minute, end_hour, end_minute = setting_time(event)
                if datetime.datetime.utcnow() + datetime.timedelta(days=12,hours=9) < start < datetime.datetime.utcnow() + datetime.timedelta(days=15,hours=9):
                    if n == 0:
                        driver = reserve(start,day)
                        n = select_place(event, day, start_hour, start_minute, end_hour, end_minute, driver, n)
                    else:
                        n = select_place(event, day, start_hour, start_minute, end_hour, end_minute, driver, n)

    except Exception as e:
        error = str(traceback.format_exc()) +"\ " + str(e)
        if len(error) > 950:
            errors = [error[i: i+950] for i in range(0, len(error), 950)]
            for j in range(len(errors)):
                send_line(errors[j])

    #参加確認の判別
    for event in events:
        start, day, start_hour, start_minute, end_hour, end_minute = setting_time(event)
        if datetime.datetime.utcnow() + datetime.timedelta(days=1,hours=9) < start < datetime.datetime.utcnow() + datetime.timedelta(days=2,hours=9):
            attend_line(event)
            


#幹部ライン送る
def send_line(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {'Authorization': 'Bearer ' + line_token}
    
    message = message
    data = {
        "message": message
    }

    requests.post(
        "https://notify-api.line.me/api/notify",
        headers=headers,
        data=data,
    )



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
    access_token = twin_token
    headers = {'Authorization': 'Bearer ' + access_token}
    try:
        location = event['location']
    except:
        location = ""
    
    message = "\n" + "日付：" + day + "\n" + "時間：" + start_hour + ":" + start_minute + "-" + end_hour + ":" + end_minute + "\n" + "場所：" + location + "\n" + "内容：" + event['summary'] + "\n" + "参加者はこのトークにリアクションお願いします！"
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
