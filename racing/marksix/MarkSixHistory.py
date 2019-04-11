from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import json

from db.mysqlMarkSixConnector import MysqlMarkSixConnector

class MarkSixHistory():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def getData(self):
        url = "https://bet.hkjc.com/marksix/getJSON.aspx?sb=0"

        stmonth = ['0101', '0401', '0701', '1001']
        edmonth = ['0331', '0630', '0930', '1231']

        styear = 2019
        endyear = 2019

        while styear <= endyear:
            for idx,val in enumerate(stmonth):
                result_arr = []
                newurl = url + "&sd=" + str(styear) + stmonth[idx] + "&ed=" + str(styear) + edmonth[idx]

                self.driver.get(newurl)

                try:
                    WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_tag_name('body'))
                finally:
                    print('getDateList')

                bodyText = self.driver.find_element_by_tag_name('pre').text
                jsonBody = json.loads(bodyText)

                for jsonObj in jsonBody:
                    noStr = jsonObj['no'];
                    noArr = [x.strip() for x in noStr.split('+')]
                    result = [jsonObj['id'], datetime.strptime(jsonObj['date'], '%d/%m/%Y').strftime('%Y-%m-%d'),
                              noArr[0], noArr[1], noArr[2], noArr[3], noArr[4], noArr[5], jsonObj['sno']]
                    result_arr.append(result)

                db = MysqlMarkSixConnector()
                info_sql = "REPLACE INTO marksix.result_history (id, date, no1, no2, no3, no4, no5, no6, sno) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                db.batch_insert_sql(info_sql, result_arr)

            styear += 1