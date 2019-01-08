#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2018/10/8 2:28 PM
# @Author: jasmine sun
# @File  : mapServer.py

import pandas as pd
import pymysql
from flask import Flask, render_template, jsonify

# 生成Flask实例
app = Flask(__name__)


# 不同城市不同薪资水平占比
@app.route('/bar', methods=['GET'])
def show_map():
    return render_template('BarChart.html')


@app.route('/get_bar_data', methods=['POST'])
def get_bar_data():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='xxx', db='lagou_db',
                           charset='utf8', use_unicode=True)

    city_datas = pd.read_sql("select city, count(city) from lagou_table group by city having count(city) > 1", conn).iloc[:, 0]
    city_list = city_datas.values.tolist()

    cursor = conn.cursor()
    sql = "select t.city, t.work_year, count(t.id) as work_count from `lagou_table` t group by t.city, t.work_year"
    cursor.execute(sql)
    result = cursor.fetchall()

    city_map = {}
    for city in city_list:
        experience_count = [0] * 7
        for tp in result:
            if tp[0] == city:
                if tp[1] == '应届毕业生':
                    experience_count[0] = int(tp[2])
                elif tp[1] == '1年以下':
                    experience_count[1] = int(tp[2])
                elif tp[1] == '1-3年':
                    experience_count[2] = int(tp[2])
                elif tp[1] == '3-5年':
                    experience_count[3] = int(tp[2])
                elif tp[1] == '5-10年':
                    experience_count[4] = int(tp[2])
                elif tp[1] == '10年以上':
                    experience_count[5] = int(tp[2])
                elif tp[1] == '不限':
                    experience_count[6] = int(tp[2])

        city_map[city] = experience_count

    return jsonify(city_map)



# 全国 Python 岗位公司地理分布
@app.route('/maps')
def maps():
    return render_template('maps.html')


@app.route('/get_data', methods=['POST'])
def get_data():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='xxx', db='lagou_db',
                           charset='utf8', use_unicode=True)
    # longitude 经度  latitude  纬度
    information = pd.read_sql(
        "select company_full_name, latitude, longitude from lagou_table where latitude not like '0.0'", conn)
    companys = information.iloc[:, 0]
    latitude = information.iloc[:, 1]
    longtitude = information.iloc[:, 2]

    companys_list = companys.values.tolist()
    latitude_list = latitude.values.tolist()
    longtitude_list = longtitude.values.tolist()

    data = [list(x) for x in zip(longtitude_list, latitude_list)]

    # 调节圆点大小
    add = ',30'
    for i in range(len(data)):
        data[i] = ','.join(data[i])
        data[i] = data[i] + add

    mix_data = [list(x) for x in zip(companys_list, data)]
    a_list = []
    for item in mix_data:
        a = {
            'name': item[0],
            'value': item[1].strip(',').split(',')
        }
        a_list.append(a)

   

    return jsonify(a_list)


if __name__ == '__main__':
    app.run()
