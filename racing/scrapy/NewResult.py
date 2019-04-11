from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime,timedelta
from db.mysqlConnector import MysqlConnector
from util.GlobalFunction import GlobalFunction
from datetime import datetime
import re

class NewResult:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def result_data(self):
        url = GlobalFunction.racing_result_url
        self.driver.get(url)

        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME,'raceMeeting_select')))
        finally:
            print('getDateList')

        date_list = []
        el = self.driver.find_element_by_xpath('//*[@id="selectId"]')

        # get date list
        for option in el.find_elements_by_tag_name('option'):
            option_value = option.get_attribute('value')
            option_date = datetime.strptime(option_value, '%d/%m/%Y')
            if datetime.now() > (option_date + timedelta(days=1)):
                date_list.append(option_date.strftime('%Y/%m/%d'))

        db = MysqlConnector()
        exist_date = db.select_sql("select matchDate from match_date GROUP BY matchDate");
        exist_row = [item[0].strftime('%Y/%m/%d') for item in exist_date]

        not_exist_date_list = list(set(date_list) - set(exist_row))

        not_exist_date_list.sort()
        for date in not_exist_date_list:
            self.get_result_date(date)

    def get_result_date(self, date):
        db = MysqlConnector()
        sql = "INSERT INTO match_date(matchDate) VALUES (%s);"
        db.batch_insert_sql(sql, [[date]])

        url = GlobalFunction.racing_result_url + '?RaceDate=' + date
        self.driver.get(url)

        # 外國賽事無 raceMeeting_select
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,'raceMeeting_select')))
        except TimeoutException:
            return print("海外賽事")
        finally:
            print('Success number of match')

        racing_bar_len = len(self.driver.find_elements_by_xpath('/html/body/div/div[2]/table/tbody/tr[1]/td'))

        batch_match_data = []

        for n in range(2, racing_bar_len):
            self.driver.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr[1]/td[%d]' % n).click()

            match_date = datetime.strptime(self.driver.find_element_by_xpath('/html/body/div/div[3]/p[1]/span[1]').text[6:16], '%d/%m/%Y').strftime('%Y-%m-%d')
            place = self.driver.find_element_by_xpath('/html/body/div/div[3]/p[1]/span[1]').text[-4:].strip()
            match_name = self.driver.find_element_by_xpath('/html/body/div/div[4]/table/tbody/tr[3]/td[1]').text
            race_no = re.search('第 (.*) 場',self.driver.find_element_by_xpath('/html/body/div/div[4]/table/thead/tr/td[1]').text)
            race_no = race_no.group(1)
            rank_distance = self.driver.find_element_by_xpath('/html/body/div/div[4]/table/tbody/tr[2]/td[1]').text
            ranking = rank_distance.split("-")[0].strip()
            distance = rank_distance.split("-")[1].strip()
            going = self.driver.find_element_by_xpath('/html/body/div/div[4]/table/tbody/tr[3]/td[3]').text
            course = self.driver.find_element_by_xpath('/html/body/div/div[4]/table/tbody/tr[2]/td[3]').text
            bonus = self.driver.find_element_by_xpath('/html/body/div/div[4]/table/tbody/tr[4]/td[1]').text
            match_info_colum_list = [match_date, race_no, place, match_name, ranking, distance, going, course, bonus]
            batch_match_data.append(match_info_colum_list)

            horse_row_len = len(self.driver.find_elements_by_xpath('/html/body/div/div[5]/table/tbody/tr'))
            horse_colunm_len = len(self.driver.find_elements_by_xpath('/html/body/div/div[5]/table/tbody/tr[1]/td'))

            batch_horse_data = []
            for x in range(1, horse_row_len+1):
                horse_column_list = [match_date, race_no]
                for y in range(1, horse_colunm_len+1):
                    horse_text = self.driver.find_element_by_xpath('/html/body/div/div[5]/table/tbody/tr[%d]/td[%d]' % (x, y)).text
                    if y == 11:
                        horse_text = '00:' + horse_text.replace('.', ':', 1)
                    horse_column_list.append(horse_text)
                batch_horse_data.append(horse_column_list)

            horse_sql = """INSERT IGNORE INTO horse_matches_result
                    (matchDate,race,place,horse_number,horse_name,jockey,trainer,actual_weight,declar_weight,draw,lbw,running_position,finish_time,win_odds)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            print(batch_horse_data)
            db.batch_insert_sql(horse_sql, batch_horse_data)

        db = MysqlConnector()
        info_sql = "INSERT IGNORE INTO place_matches_info(matchDate,race,place,matchName,ranking,distance,course,going,bonus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        db.batch_insert_sql(info_sql, batch_match_data)
