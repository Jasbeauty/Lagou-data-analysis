#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2018/9/19 1:55 PM
# @Author: jasmine sun
# @File  : data_crawler.py
import json
import random
import time

import pymysql
import requests
from requests import RequestException

# city_list = []
# company_full__name_list = []
# company_size_list = []
# education_list = []
# industry_field_list = []
# position_advantage_list = []
# position_lables_list = []
# position_name_list = []
# salary_list = []
# work_year_list = []


def get_urls(page):
    # 类的初始化

    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false'
    form_data = 'first=true&pn=' + str(page) + '&kd=Python'
    proxies = {'http': 'http://118.190.95.43:9001', 'http': 'http://61.177.47.86:60086',
               'http': 'http://120.92.74.237:3128'}
    agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)']
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '25',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_Python?px=default&city=%E5%85%A8%E5%9B%BD',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'JSESSIONID=ABAAABAAAFCAAEGF0BCC1B4BF5D28479356E527874F353D; _ga=GA1.2.26692172.1536562417; user_trace_token=20180910145336-3dd1d0d0-b4c6-11e8-8d38-525400f775ce; LGUID=20180910145336-3dd1d486-b4c6-11e8-8d38-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.331200754.1537263322; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1536562417,1537263322; X_HTTP_TOKEN=6e95c111608958f24acc6a1dec63105c; TG-TRACK-CODE=index_navigation; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1537414693; LGRID=20180920113812-99d7dbdd-bc86-11e8-baf2-5254005c3644; SEARCH_ID=c9a851e461774fdb99e67c7e1e00fbf6'
    }

    headers['User-Agent'] = agents.pop(random.randint(0, 6))
    response = requests.post(url=url, proxies=proxies, data=form_data, headers=headers)
    response.encoding = 'utf-8'
    # print(response.text)  # str字符串类型

    # json.loads()函数是将json格式数据转换为字典
    # json.dump()和json.load()主要用来读写json文件函数
    results = json.loads(response.text)
    # print(results)  # 字典类型
    details = results['content']['positionResult']['result']
    # print(details)  # list数组类型

    for i in details:
        city = i['city']  # 所在城市
        company_full_name = i['companyFullName']  # 公司全称
        company_size = i['companySize']  # 公司规模
        education = i['education']  # 学历要求
        industry_field = i['industryField']  # 行业类型
        position_advantage = i['positionAdvantage']  # 岗位优势
        # join()：连接字符串数组。将字符串、元组、列表中的元素以指定的字符(分隔符)连接生成一个新的字符串
        position_lables = ','.join(i['positionLables'])  # 岗位标签
        position_name = i['positionName']      # 岗位名称
        salary = i['salary']    # 薪资
        work_year = i['workYear']  # 年限要求
        district = i['district']    # 城市所在的区
        job_nature = i['jobNature']     # 工作性质
        latitude = i['latitude']    # 纬度
        longitude = i['longitude']      # 经度
        position_id = i['positionId']   # 详情页面ID
        finance_stage = i['financeStage']   # 是否融资
        line_station = i['linestaion']   # 地铁线

        print(city)
        print(company_full_name)
        print(company_size)
        print(education)
        print(industry_field)
        print(position_advantage)
        print(position_lables)
        print(position_name)
        print(salary)
        print(work_year)
        print(district)
        print(job_nature)
        print(latitude)
        print(longitude)
        print(position_id)
        print(finance_stage)
        print(line_station)

        conn = pymysql.connect(host='localhost', port=3306, user='root', password='xxx', db='lagou_db',
                               charset='utf8', use_unicode=True)
        cursor = conn.cursor()
        try:
            cursor.execute("insert into lagou_table(city, company_full_name, company_size ,education, industry_field, position_advantage, position_lables, position_name, salary, work_year, district, job_nature, latitude, longitude, job_detail, finance_stage, line_station) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','https://www.lagou.com/jobs/{}.html','{}','{}')".format(city, company_full_name, company_size, education, industry_field, position_advantage, position_lables, position_name, salary, work_year, district, job_nature, latitude, longitude, position_id, finance_stage, line_station))
            conn.commit()
        except pymysql.Error as e:
            print("database error, Causes: %d: %s" % (e.args[0], e.args[1]))
        finally:
            cursor.close()
            conn.close()

        # city_list.append(city)
        # company_full__name_list.append(company_full_name)
        # company_size_list.append(company_size)
        # education_list.append(education)
        # industry_field_list.append(industry_field)
        # position_advantage_list.append(position_advantage)
        # position_lables_list.append(position_lables)
        # position_name_list.append(position_name)
        # salary_list.append(salary)
        # work_year_list.append(work_year)

    # print(city_list)
    # print(company_full__name_list)
    # print(company_size_list)
    # print(education_list)
    # print(industry_field_list)
    # print(position_advantage_list)
    # print(position_lables_list)
    # print(position_name_list)
    # print(salary_list)
    # print(work_year_list)

    try:
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None



if __name__ == '__main__':
    page = input('要爬取的页数：')
    for n in range(1, int(page) + 1):
        print("第 " + str(n) + " 页")
        get_urls(n)
        # round()方法是返回浮点数的四舍五入值
        # random.uniform(x, y)方法将随机生成一个浮点数，它在[x, y)范围内
        time.sleep(round(random.uniform(3, 5), 2))

        # random.randint()生成指定范围内的随机整数
        # time.sleep(random.randint(3, 5))
