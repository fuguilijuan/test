from flask import render_template, request
from TestApi.Web.view import blue
from TestApi.TestCase import (test_fido, test_cert)
from TestApi.TestClient import test_client
# from TestApi.Email import send_email
# from TestApi.Ding import ding
from TestApi.Database import database_conn
from BeautifulReport.BeautifulReport import result
from BeautifulReport import BeautifulReport
from TestApi.Config.common import CONF
import urllib.request
import time
import unittest
import random
import json
import sys
import os
import yaml

directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '\\TestCase\\test_data'
jsoname = 'testcase.json' # 填充完数据的测试用例，用例展示在测试数据导航栏
yalmfile = 'test_data.yalm' # 原始测试数据，用来手动修改的

@blue.route('/index', methods=['GET', 'POST'], endpoint='index')
def index():
    """index首页"""
    return render_template('index.html')

@blue.route('/report', methods=['GET'], endpoint='report')
def report():
    return render_template('report.html')

@blue.route('/welcome', methods=['GET'], endpoint='welcome')
def welcome():
    return render_template('welcome.html')

@blue.route('/testdata', methods=['GET'], endpoint='testdata')
def testdata():
    # tm = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    with open(directory + '\\' + jsoname, encoding='utf-8') as f:
        data = json.load(f)
    return render_template(
        'testdata.html',
        data=json.dumps(data,indent=4).encode().decode('unicode-escape'),
        count=int(len(data) / 2),
        )

@blue.route('/conf', methods=['POST', 'GET'], endpoint='config')
def conf():
    """index页面测试配置"""
    # 后台地址

    rd = random.randint(11111111, 999999999)
    path = os.path.dirname(__file__) + '\\conf.json'  # 前端传入的配置写入json文件
    with open(str(directory + '\\' + yalmfile), encoding='utf-8') as f:
        case_data = yaml.load(f, Loader=yaml.FullLoader)
    if request.method == 'POST':
        time.sleep(2)
        host = request.form.get('host')  # 服务器ip
        port = request.form.get('port')  # 服务器端口
        ip = request.form.get('ip')  # 数据库ip
        db = request.form.get('db') # 数据库名
        name = request.form.get('name')  # 服务器用户名
        pwd = request.form.get('pwd')  # 服务器密码
        modify_case = request.form.get('dt')  # 修改后的测试用例
        uap_admin = "http://{}:{}".format(host, port)
        data = {
            "host": host,
            "port": port,
            "ip": ip,
            "db": db,
            "name": name,
            "pwd": pwd,
            "rd": rd
        }
        # 前端传的数据外加随机数都写入json文件，供config调用
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))
        try:
            urllib.request.urlopen(uap_admin, timeout=3).read()
            _dir = os.path.dirname(__file__)
            report_dir = os.path.dirname(_dir) + '\\templates'
            tm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            sys.stderr.write('准备执行接口自动化测试...    {}    '.format(tm+ '\n'))

            if isinstance(database_conn.execute_sql(),database_conn.pymysql.connections.Connection):
                # 修改后的用例、测试配置项，保存到CONF
                CONF.clear()
                CONF.append(data)
                CONF.append(json.loads(modify_case))
                test_client.new_testclient_obj().jvmStart()  # 启动jvm
                cases = [
                    test_fido.get_fido_case(),
                    test_cert.get_test_cert()
                ]
                suit = unittest.TestSuite()
                for case in cases:
                    suit.addTests(case)
                run = BeautifulReport(suit)
                run.report(filename='report', description='UAP接口自动化测试报告',
                           report_dir=report_dir)
                print(result)
                # send_email.send_mail()  # 发送测试报告邮件
                # ding.send_ding()  # 发送钉钉机器人通知
                return render_template(
                    'testresult.html',
                    count=result[0],
                    succ=result[1],
                    fail=result[2],
                    err=result[3],
                    data=data)
            else:
                return render_template(
                    'dberr.html',
                    msg="数据库连接失败：{}".format(database_conn.execute_sql()),
                    url="{}/uap-admin".format(uap_admin),
                    data=data,
                    flag=0)
        except Exception as e:
            return render_template(
                'dberr.html',
                err="{} tomcat打开失败。请检查ip和端口号：{}".format(uap_admin,e),
                flag=1,
                data=data)
    return render_template('conf.html', data=json.dumps(
        case_data, indent=4).encode().decode('unicode-escape'))
