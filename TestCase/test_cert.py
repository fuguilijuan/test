from TestApi.TestCase.test_data import test_data
from TestApi.Request import request
from TestApi.TestClient import test_client
import unittest

reg_uafRequest = None  # 证书注册时testclient请求需要的uafRequest，通过/uaf/reg/receive接口获取
send_uafRequest = None # 证书注册时，保存证书需要的uafRequest，通过/uaf/reg/send接口获取
auth_uafRequest = None  # 证书认证时testclient请求需要的参数uafRequest，通过/uaf/auth/receive接口获取

class Test_Cert(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        # test_client.new_testclient_obj().jvmStart()  # 调试时启动jvm
        cls.reg_receive = '/uaf/reg/receive'  # 注册发起
        cls.reg_send = '/uaf/reg/send'  # 注册完成
        cls.auth_receive = '/uaf/auth/receive'  # 认证发起
        cls.auth_send = '/uaf/auth/send'  # 认证完成
        cls.cert_update='/uaf/cert/updatestatus' #更新证书状态为已安装
    
    @classmethod
    def tearDownClass(cls) -> None:
        # test_client.new_testclient_obj().jvmShutdown()
        pass
    
    def test_cert_reg_receive(self):
        """证书：注册发起"""
        global reg_uafRequest
        body = test_data.test_data('test_cert_reg_receive')
        self.assertTrue(body is not False, '找不到测试数据，请检查参数或数据！')
        r = request.req_method('post', self.reg_receive, data=body)
        self.assertEqual(r.status_code, 200, "status_code:{}".format(r.status_code))
        self.assertEqual(r.json()['statusCode'], 1200, "fail：{}".format(r.json()))
        reg_uafRequest = r.json()['uafRequest']  # cert_testclient请求需要的uafRequest
    
    def test_cert_reg_client(self):
        """证书：注册发起调用client"""
        self.assertNotEqual(reg_uafRequest, None, "证书：注册发起接口返回的uafRequest有误")
        reg_client_response = test_client.new_testclient_obj().cert_testclient(uafRequest=reg_uafRequest)
        test_data.send_uafResponse('test_cert_reg_send',reg_client_response)  # 组装send接口请求报文
    def test_cert_reg_send(self):
        """证书：注册完成"""
        global send_uafRequest
        self.assertNotEqual(reg_uafRequest, None, "证书：注册发起接口返回的uafRequest有误")
        send_body = test_data.test_data('test_cert_reg_send')
        self.assertTrue(send_body is not False, '找不到测试数据，请检查参数或数据！')
        r = request.req_method('post', self.reg_send, data=send_body)
        self.assertEqual(r.status_code, 200, "status_code:{}".format(r.status_code))
        self.assertEqual(r.json()['statusCode'], 1200, "fail：{}".format(r.json()))
        send_uafRequest = r.json()['uafRequest'] #存储证书调用java方法时传的参数

    def test_save_cert_client(self):
        """证书：存储证书调用client"""
        self.assertNotEqual(reg_uafRequest, None, "证书：注册发起接口返回的uafRequest有误")
        send_client_response = test_client.new_testclient_obj().save_cert_client(uafRequest=send_uafRequest)
        self.assertTrue(send_client_response is not None)
        keyid = send_client_response['keyId']
        data_save_cert = test_data.test_data('test_updata_cert_status') # 获取更新证书状态为已安装的数据
        data_save_cert['context']['keyID'] = keyid # 替换keid
        dic={
            "uafResponse":"[{%s}]"%keyid
        }
        test_data.send_uafResponse('test_save_cert',dic) # 组装更新证书接口的数据

    def test_updata_cert_status(self):
        """证书：更新证书状态为已安装"""
        self.assertNotEqual(reg_uafRequest, None, "证书：注册发起接口返回的uafRequest有误")
        updata_body=test_data.test_data('test_updata_cert_status')
        self.assertTrue(updata_body is not False, '找不到测试数据，请检查参数或数据！')
        r = request.req_method('post', self.cert_update, data=updata_body)
        self.assertEqual(r.status_code, 200, "status_code:{}".format(r.status_code))
        self.assertEqual(r.json()['statusCode'], 1200, "fail：{}".format(r.json()))

    def test_cert_auth_receive(self):
        """证书：认证发起"""
        global auth_uafRequest
        body = test_data.test_data('test_cert_auth_receive')
        self.assertTrue(body is not False, '找不到测试数据，请检查参数或数据！')
        r = request.req_method('post', self.auth_receive, data=body)
        self.assertEqual(r.status_code, 200, "status_code:{}".format(r.status_code))
        self.assertEqual(r.json()['statusCode'], 1200, "fail：{}".format(r.json()))
        auth_uafRequest = r.json()['uafRequest']  # cert_testclient请求需要的uafRequest

    def test_cert_auth_client(self):
        """证书：认证发起调用client"""
        self.assertTrue(auth_uafRequest is not None, '证书：认证发起接口返回的uafRequest有误')
        __auth_client_response = test_client.new_testclient_obj().cert_auth_client(uafRequest=auth_uafRequest)
        self.assertTrue(__auth_client_response is not None)
        test_data.send_uafResponse('test_cert_auth_send',__auth_client_response)

    def test_cert_auth_send(self):
        """证书：认证完成"""
        self.assertTrue(auth_uafRequest is not None,'证书：认证发起接口返回的uafRequest有误')
        body= test_data.test_data('test_cert_auth_send')
        r = request.req_method('post', self.auth_send, data=body)
        self.assertEqual(r.status_code, 200, "status_code:{}".format(r.status_code))
        self.assertEqual(r.json()['statusCode'], 1200, "fail：{}".format(r.json()))

def get_test_cert():
    list_case = [
        Test_Cert("test_cert_reg_receive"),
        Test_Cert("test_cert_reg_client"),
        Test_Cert("test_cert_reg_send"),
        Test_Cert("test_save_cert_client"),
        Test_Cert("test_updata_cert_status"),
        Test_Cert("test_cert_auth_receive"),
        Test_Cert("test_cert_auth_client"),
        Test_Cert("test_cert_auth_send")
    ]
    return list_case

# if __name__ == '__main__':
#     suit = unittest.TestSuite()
#     suit.addTest(Test_Cert("test_cert_reg_receive"))
#     suit.addTest(Test_Cert("test_cert_reg_client"))
#     suit.addTest(Test_Cert("test_cert_reg_send"))
#     suit.addTest(Test_Cert("test_save_cert_client"))
#     suit.addTest(Test_Cert("test_updata_cert_status"))
#     suit.addTest(Test_Cert("test_cert_auth_receive"))
#     suit.addTest(Test_Cert("test_cert_auth_client"))
#     suit.addTest(Test_Cert("test_cert_auth_send"))
#
#     runner = unittest.TextTestRunner()
#     runner.run(suit)