# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import pickle
import os.path

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


def reserve():
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
    #options.add_argument('--headless'); # ※ヘッドレスモードを使用する場合、コメントアウトを外す

    #
    # Chromeドライバーの起動

    DRIVER_PATH = '/Users/hamasyo/Selenium/chromedriver' #ローカル
    chrome_sevice = fs.Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=chrome_sevice, options=options)
    driver.implicitly_wait(20)

    #施設予約システムにアクセス
    driver.get("https://eqres01.adst.keio.ac.jp/")

    #keio.jp認証
    #ID
    driver.find_element(By.CSS_SELECTOR,'#username').send_keys('hamasyo222@keio.jp')#

    #パスワード
    driver.find_element(By.CSS_SELECTOR,'#password').send_keys('Konnitiwa196')#

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
    driver.find_element(By.NAME,'s2[reservation_date]').send_keys("2022/04/11")
    driver.find_element(By.NAME,'s2[reservation_date]').send_keys(Keys.ENTER)

    #期間終わり
    driver.find_element(By.NAME,'s2[reservation_date_to]').send_keys("2022/04/11")
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
    while datetime.datetime.now() < datetime.datetime(2022, 4, 1, 0, 0, 00):
        time.sleep(1)

    #検索
    driver.find_element(By.CSS_SELECTOR,'#main_content > div > div.container_body.top_info > div > div:nth-child(2) > div > form > button').click()

    #画面遷移

    try:
        #時間選択 アリーナ奥
        driver.find_element(By.CSS_SELECTOR,'#main_content > div.container > div.container_body.noscroll > div.fix_tbl_area.time_table.found-reservable > div.fix_bottom_right > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div.time_cell.relative > label:nth-child(4)').click()
        
        #開始プルダウン
        #時間
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation_start_h')).select_by_value("18")
        #分
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation_start_m')).select_by_value("00")
        #終了プルダウン
        #時間
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation_end_h')).select_by_value("19")
        #分
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation_end_m')).select_by_value("45")

        #実開始プルダウン
        #時間
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(10) > div > div:nth-child(2) > select')).select_by_value("18")
        #分
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(10) > div > div:nth-child(3) > select')).select_by_value("00")

        #実終了プルダウン
        #時間
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(12) > div > div:nth-child(1) > select')).select_by_value("19")
        #分
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(12) > div > div:nth-child(2) > select')).select_by_value("45")

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
    except Exception as e:
        pass
      
        #時間選択 アリーナ手前
        driver.find_element(By.CSS_SELECTOR,'#main_content > div.container > div.container_body.noscroll > div.fix_tbl_area.time_table.found-reservable > div.fix_bottom_right > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > div.time_cell.relative > label:nth-child(4)').click()
        
        #開始プルダウン
        #時間
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation_start_h')).select_by_value("18")
        #分
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation_start_m')).select_by_value("00")
        #終了プルダウン
        #時間
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation_end_h')).select_by_value("19")
        #分
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation_end_m')).select_by_value("45")

        #実開始プルダウン
        #時間
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(10) > div > div:nth-child(2) > select')).select_by_value("18")
        #分
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(10) > div > div:nth-child(3) > select')).select_by_value("00")

        #実終了プルダウン
        #時間
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(12) > div > div:nth-child(1) > select')).select_by_value("19")
        #分
        Select(driver.find_element(By.CSS_SELECTOR,'#reservation-form > dl > dd:nth-child(12) > div > div:nth-child(2) > select')).select_by_value("45")

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


if __name__ == '__main__':
    reserve()
    