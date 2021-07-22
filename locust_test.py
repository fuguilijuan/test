
from locust import HttpUser, TaskSet, task, between,constant
from locust.contrib.fasthttp import FastHttpUser
# import requests
import json
import random
import jpype
import os
# import multiprocessing


fail_reg_count = 0
fail_send_count = 0
fail_client_count = 0

class TestClient:
    """
    调用java方法
    """

    def __init__(self):
        """获取当前路径的上级路径"""
        # self.ext_classpath = os.path.dirname(__file__).replace('/', '\\')
        self.ext_classpath = "D:\\gmrz\\TestApi\\TestClient"

    def fido_testclient(self, uafRequest, AuthUserName="00000000000", isAddUVI='0'):
        """
        指纹：调用java方法
        :param uafRequest:注册接口返回的uafRequest
        :param AuthUserName:注册时的用户名
        :param isAddUVI:不清楚，默认给0
        :return:
        """
        try:
            # jpype.java.lang.System.out.println('hello world!')
            javaClass = jpype.JClass('com.gm.uaf.client.UAFTestClient')
            jd = javaClass("{}\\client.properties".format(self.ext_classpath))
            response = jd.process(uafRequest, AuthUserName, isAddUVI)
            return eval(str(response))
        except Exception as e:
            return 'testclient get data error：{}'.format(e)

    def auth_testclient(self):
        pass

    def jvmStart(self):
        """
        启动jvm并加载所有jar包
        :return:
        """
        try:
            jvmPath = jpype.getDefaultJVMPath()
            jpype.startJVM(jvmPath, "-ea", '-Djava.ext.dirs={}\\jar'.format(self.ext_classpath))
        except Exception as e:
            return 'jvm start error：{}'.format(e)

    @staticmethod
    def jvmShutdown():
        """
        关闭jvm
        :return:
        """
        jpype.shutdownJVM()


def uafResponse():
    """
    返回TestClient实例
    :return:
    """
    t = TestClient()
    return t


class UserBehavior(FastHttpUser):  # TaskSet
    wait_time = constant(1)

    def on_start(self):
        uafResponse().jvmStart()
        self.start_receive = 'http://192.168.6.201:8080/uaf/reg/receive'  # 注册发起
        self.finish_receive = 'http://192.168.6.201:8080/uaf/reg/send'  # 注册完成
        self.header = {
            "Content-Type": "application/fido+uaf"
        }
        transNo = "transNo-transNo{}".format(random.randint(10000000, 99999999))
        userName = 'TestFgui{}'.format(random.randint(10000000, 99999999))
        authType = "00"
        deviceID = 'HW5Dqw5zr5QWERTYUIOPA9D6GHJKLZX{}CVB'.format(random.randint(10000000, 99999999))
        self.data = {
            "test_fido_reg_receive": {
                "context": {
                    "appID": "1103",
                    "transNo": transNo,
                    "userName": userName,
                    "transType": "00",
                    "authType": authType,
                    "opType": "01",
                    "dn": "eyJjYXJkTk8iOiIxMjM0NTY3ODkxMjM0NTY3ODkiLCJjYXJkVHlwZSI6IjAxIiwiY2FyZE5hbWUiOiJ0ZXN0In0",
                    "devices": {
                        "deviceID": deviceID,
                        "deviceName": "ALP-AL001",
                        "deviceType": "HUAWEI"
                    }
                }
            },
            "test_fido_reg_send": {
                "context": {
                    "appID": "1103",
                    "opType": "00",
                    "transNo": transNo,
                    "userName": userName,
                    "transType": "00",
                    "authType": authType,
                    "ext": "",
                    "from": "01",
                    "devices": {
                        "deviceID": deviceID,
                        "deviceName": "ALP-AL001",
                        "deviceType": "HUAWEI",
                        "osVersion": 23,
                        "osType": "android"}
                }
            }
        }

    def on_stop(self):
        uafResponse().jvmShutdown()

    @task
    def test_fido_reg_receive(self):
        """指纹：注册发起"""
        global fail_reg_count, fail_send_count, fail_client_count
        body = self.data['test_fido_reg_receive']
        r = self.client.post(self.start_receive, headers=self.header, data=json.dumps(body))
        if r.status_code == 200:
            # test_client请求需要的uafRequest
            if r.json()['statusCode'] == 1200:
                uafresponse = uafResponse().fido_testclient(uafRequest=r.json()['uafRequest'])
                if type(uafresponse) == dict:
                    # print("uafResponse:", uafresponse)
                    self.data['test_fido_reg_send'].update(**uafresponse)
                    send_body = self.data['test_fido_reg_send']
                    r1 = self.client.post(self.finish_receive, headers=self.header, data=json.dumps(send_body))
                    if r1.status_code == 200:
                        if r1.json()['statusCode'] == 1200:
                            # print("注册发起：", r.json())
                            # print("注册调用client：ok")
                            # print("注册完成：", r1.json())
                            pass
                        else:
                            fail_send_count += 1
                    else:
                        fail_send_count += 1
                else:
                    fail_client_count += 1
            else:
                fail_reg_count += 1
        else:
            fail_reg_count += 1
        if fail_reg_count + fail_client_count + fail_send_count > 5:
            print("fail_reg_count:{} fail_client_count:{} fail_send_count:{}".
                  format(fail_reg_count, fail_client_count, fail_send_count))


class RunTest(FastHttpUser):
    tasks = [UserBehavior]
    # wait_time = between(1, 2)
    wait_time = constant(1)


if __name__ == '__main__':
    # uafResponse().jvmStart()
    # os.system('locust -f locust_test.py --headless  -u 200 -r 10 --host=http://192.168.6.187')  # no-web模式
    os.system('locust -f locust_test.py --host=http://192.168.6.201')  # web打开地址：localhost:8089
    # os.system('locust -f locust_test.py --master')  # 单机分布式压测
    # os.system('locust -f locust_api.py --host=https://www.baidu.com')
    """
    分布式压测，主从机都需要locust环境和压测脚本
    1、locust -f locust_test.py --master  主机
    2、locust -f locust_test.py --worker  从机
    3、locust -f locust_test.py --worker --master-host=192.168.3.212    设置从机对应的主机
    no Web 模式：locust -f locust_test.py --headless  -u 100 -r 10
    """
