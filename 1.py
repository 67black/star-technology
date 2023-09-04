# coding: utf-8
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_data(xpath, is_url=True):
    """
    获取对应的数据
    :param xpath: 元素选择器,str
    :param is_url: 值是否有a标签，bool
    :return: 数据,list
    """
    data_td = driver.find_elements(By.XPATH, xpath)
    data_list = []
    for element in data_td:
        value = element.get_attribute("data-value")
        if is_url:
            values = re.findall("<a .*>(.*?)</a>", str(value))
        else:
            values = str(value)
        data_list.append(values)
    return data_list


def handel_data(data_dict):
    """
    数据清洗
    :param data_dict: 整合后的数据,dict
    :return: 清洗后的数据,dict
    """
    re_data_dict = {}
    for i in data_dict:
        if i == "isin" or i == "bood_code":
            new_list = []
            l = [j[0] for j in data_dict.get(i) if j]
            for m in l:
                if m in new_list:
                    continue
                new_list.append(m)
            re_data_dict[i] = new_list
        else:
            re_data_dict[i] = [j for j in data_dict.get(i) if j != "None"]
    return re_data_dict


def open_page():
    """
    获取打开页面中的数据
    :return: 详细数据,list
    """
    isin = []
    bood_code = []
    issuer = []
    bond_type = []
    issuer_date = []
    latest_rating = []
    for i in range(300, 1200, 300):
        driver.execute_script(f'window.scrollTo(0,{i})')  # 鼠标向下滑动一定的距离
        time.sleep(2.3)
    page_total = driver.find_element_by_class_name("page-total").text
    for j in range(int(page_total)):
        if j == 0:
            pass
        else:
            for i in range(300, 1200, 300):
                driver.execute_script(f'window.scrollTo(0,{i})')  # 鼠标向下滑动一定的距离
                time.sleep(2.3)
        # ISIN
        isin.extend(get_data('//td[@data-name="isin"]'))
        # Bond Code
        bood_code.extend(get_data('//td[@data-name="bondCode"]'))
        # Issuer
        issuer.extend(get_data('//td[@data-name="entyFullName"]', is_url=False))
        # Bond Type
        bond_type.extend(get_data('//td[@data-name="bondType"]', is_url=False))
        # Issue Date
        issuer_date.extend(get_data('//td[@data-name="issueStartDate"]', is_url=False))
        # Latest Rating
        latest_rating.extend(get_data('//td[@class="cell AC cell-last"]', is_url=False))
        if j == 4:
            pass
        else:
            driver.find_element(By.XPATH, '//li[@class="page-btn page-next"]/a').click()
    return isin, bood_code, issuer, bond_type, issuer_date, latest_rating


def save_data(file_name, **kwargs):
    """
    保存数据
    :param file_name: 文件路径,str
    :param kwargs: 参数,list
    :return: None
    """
    df = pd.DataFrame()
    for i, j in kwargs.items():
        df[i] = j
    df.to_csv(file_name, encoding='utf-8')


if __name__ == '__main__':
    # 实例化一个启动参数对象
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome()
    url = 'https://iftp.chinamoney.com.cn/english/bdInfo/'
    # 对网站发起请求
    driver.get(url)
    driver.implicitly_wait(20)
    # 点击选择框并进行选择
    driver.find_element(By.XPATH, '//*[@id="Bond_Type_select"]').click()
    driver.implicitly_wait(20)
    driver.find_element(By.XPATH, '//*[@value="100001"]').click()
    driver.find_element(By.XPATH, '//*[@id="Issue_Year_select"]').click()
    driver.implicitly_wait(20)
    driver.find_element(By.XPATH, '//*[@value="2023"]').click()
    driver.find_element(By.XPATH, '//*[@onclick="searchData()"]').click()
    driver.implicitly_wait(20)

    # 获取页面中的数据
    isin, bood_code, issuer, bond_type, issuer_date, latest_rating = open_page()
    time.sleep(2.6)
    driver.quit()
    # 整合数据
    data_dict = {
        'isin': isin,
        'bood_code': bood_code,
        'issuer': issuer,
        'bond_type': bond_type,
        'issuer_date': issuer_date,
        'latest_rating': latest_rating,
    }
    # 数据清洗
    all_data_dict = handel_data(data_dict)
    # 保存数据
    save_data(r'data\中国外汇交易中心.csv', ISIN=all_data_dict.get("isin"),
              Bond_Code=all_data_dict.get("bood_code"), Issuer=all_data_dict.get("issuer"),
              Bond_Type=all_data_dict.get("bond_type"), Issue_Date=all_data_dict.get("issuer_date"),
              Latest_Rating=all_data_dict.get("latest_rating"))
