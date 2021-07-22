import sys
import os
# curPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)

from TestApi.TestCase import (test_fido, test_cert)
from TestApi.TestClient import test_client
from TestApi.Config import config
from TestApi.Email import send_email
from TestApi.Ding import ding
from TestApi.Database import database_conn
from BeautifulReport.BeautifulReport import result
from BeautifulReport import BeautifulReport
import time
import unittest


if __name__ == '__main__':
    _dir = os.path.dirname(__file__)
    report_dir = os.path.dirname(_dir) + '\\Report'
    sys.stderr.write('准备执行接口自动化测试...    {}    '.format(
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))+'\n')
    uap_admin = "http://{}:{}/{}".format(config.get_config()['tomcat']['host'],
                                         config.get_config()['tomcat']['port'], 'uap-admin/')  # 后台地址
    if isinstance(database_conn.execute_sql(), database_conn.pymysql.connections.Connection):
        # 判断数据库连接是否正常
        test_client.new_testclient_obj().jvmStart()
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
        test_client.new_testclient_obj().jvmShutdown()
        print(result)
        # send_email.send_mail()  # 发送测试报告邮件
        # ding.send_ding()  # 发送钉钉机器人通知
    else:
        print('后台：{}'.format(uap_admin))
        print(database_conn.execute_sql())
