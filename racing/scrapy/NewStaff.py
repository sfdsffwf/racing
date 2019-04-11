from selenium import webdriver
from db.mysqlConnector import MysqlConnector
from util.GlobalFunction import GlobalFunction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class NewStaff:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def trainer_data(self):
        session = GlobalFunction.session
        url = GlobalFunction.trainer_url
        table_list = self.handle_data(url, session)
        db = MysqlConnector()
        sql = "REPLACE  INTO trainers(season, name, r1, r2, r3, r4, r5, total_horse, won_amount)" \
              " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        db.batch_insert_sql(sql, table_list)

    def jockey_data(self):
        session = GlobalFunction.session
        url = GlobalFunction.jockey_url
        table_list = self.handle_data(url, session)
        db = MysqlConnector()
        sql = "REPLACE  INTO jockeys(season, name, r1, r2, r3, r4, r5, total_match, won_amount) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        db.batch_insert_sql(sql, table_list)

    def handle_data(self, url, session):
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
                (By.XPATH,'/html/body/div/div[2]/div[2]/table/thead/tr[1]/td[1]')))
        finally:
            print('getDateList')

        row_count = len(self.driver.find_elements_by_xpath('/html/body/div/div[2]/div[2]/table/tbody[1]/tr'))
        column_count = len(self.driver.find_elements_by_xpath('/html/body/div/div[2]/div[2]/table/tbody[1]/tr[1]/td'))
        table_list = []
        xpath = '/html/body/div/div[2]/div[2]/table/tbody[1]/tr[%d]/td[%d]'

        for n in range(1, row_count + 1):
            column_list = [session]
            for m in range(1, column_count + 1):
                new_xpath = xpath % (n, m)
                text = self.driver.find_element_by_xpath(new_xpath).text
                column_list.append(text.replace('$', '').replace(',', ''))
            table_list.append(column_list)

        return table_list
