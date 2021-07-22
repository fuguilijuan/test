from TestApi.TestCase.test_data import test_data
from TestApi.Request import request
from TestApi.TestClient import test_client
import unittest

reg_uafRequest = None  # 注册时testclient请求需要的uafRequest，通过/uaf/reg/receive接口获取
auth_uafRequest = None  # 认证时testclient请求需要的参数uafRequest，通过/uaf/auth/receive接口获取

class Test_Fido(unittest.TestCase):
    """指纹"""
    @classmethod
    def setUpClass(cls) -> None:
        """
        调试时启动jvm，运行run函数需要注释掉此处启动的jvm
        """
        # test_client.new_testclient_obj().jvmStart()  # 调试时启动jvm
        test_client.new_testclient_obj().del_json_flie()  # 注册前先删除AuthenticatorInfo.json
        cls.reg_receive = '/uaf/reg/receive'  # 注册发起
        cls.reg_send = '/uaf/reg/send'  # 注册完成
        cls.auth_receive = '/uaf/auth/receive'  # 认证发起
        cls.auth_send = '/uaf/auth/send'  # 认证完成

    @classmethod
    def tearDownClass(cls) -> None:
        """
        调试时关闭jvm，运行run函数需要注释掉此处关闭的jvm
        """
        test_client.new_testclient_obj().del_json_flie()  # 认证完成后删除AuthenticatorInfo.json
        # test_client.new_testclient_obj().jvmShutdown()

    def test_fido_reg_receive(self):
        """指纹：注册发起"""
        global reg_uafRequest
        body = test_data.test_data('test_fido_reg_receive')
        self.assertTrue(body is not False, '找不到测试数据，请检查参数或数据！')
        r = request.req_method('post', self.reg_receive, data=body)
        self.assertEqual(r.status_code, 200, "status_code:{}".format(r.status_code))
        # print(r.json()['statusCode'])
        self.assertEqual(r.json()['statusCode'], 1200, "fail：{}".format(r.json()))
        reg_uafRequest = r.json()['uafRequest']  # fido_testclient请求需要的uafRequest

    def test_fido_reg_client(self):
        """指纹：注册发起调用client"""
        self.assertNotEqual(reg_uafRequest, None, "指纹：注册发起接口返回的uafRequest有误")
        reg_client_response = test_client.new_testclient_obj().fido_testclient(uafRequest=reg_uafRequest)
        # print(reg_client_response)
        test_data.send_uafResponse('test_fido_reg_send', reg_client_response)  # 组装send接口请求报文

    def test_fido_reg_send(self):
        """指纹：注册完成"""
        self.assertNotEqual(reg_uafRequest, None, "指纹：注册发起接口返回的uafRequest有误")
        send_body = test_data.test_data('test_fido_reg_send')
        self.assertTrue(send_body is not False, '找不到测试数据，请检查参数或数据！')
        r = request.req_method('post', self.reg_send, data=send_body)
        self.assertEqual(r.status_code, 200, "status_code:{}".format(r.status_code))
        self.assertEqual(r.json()['statusCode'], 1200, "fail：{}".format(r.json()))

    # @unittest.skip
    def test_fido_auth_receive(self):
        """指纹：认证发起"""
        global auth_uafRequest
        body = test_data.test_data('test_fido_auth_receive')
        self.assertTrue(body is not False, '找不到测试数据，请检查参数或数据！')
        r = request.req_method('post', self.auth_receive, data=body)
        self.assertEqual(r.status_code, 200, "status_code:{}".format(r.status_code))
        self.assertEqual(r.json()['statusCode'], 1200, "fail：{}".format(r.json()))
        auth_uafRequest = r.json()['uafRequest']  # auth_testclient请求需要的uafRequest

    # @unittest.skip
    def test_fido_auth_client(self):
        """指纹：认证发起调用client"""
        self.assertNotEqual(auth_uafRequest, None, "指纹：认证发起接口返回的uafRequest有误")
        auth_client_response = test_client.new_testclient_obj().fido_testclient(uafRequest=auth_uafRequest)
        test_data.send_uafResponse('test_fido_auth_send', auth_client_response)  # 组装send接口请求报文

    # @unittest.skip
    def test_fido_auth_send(self):
        """指纹：认证完成"""
        self.assertNotEqual(auth_uafRequest, None, "指纹：认证发起接口返回的uafRequest有误")
        send_body = test_data.test_data('test_fido_auth_send')
        self.assertTrue(send_body is not False, '找不到测试数据，请检查参数或数据！')
        r = request.req_method('post', self.auth_send, data=send_body)
        self.assertEqual(r.status_code, 200, "status_code:{}".format(r.status_code))
        self.assertEqual(r.json()['statusCode'], 1200, "fail：{}".format(r.json()))
def get_fido_case():
    """
    组装测试用例
    :return:
    """
    list_case = [
        Test_Fido("test_fido_reg_receive"),
        Test_Fido("test_fido_reg_client"),
        Test_Fido("test_fido_reg_send"),
        Test_Fido("test_fido_auth_receive"),
        Test_Fido("test_fido_auth_client"),
        Test_Fido("test_fido_auth_send")
    ]
    return list_case


# if __name__ == '__main__':
#
#     suit = unittest.TestSuite()
#     suit.addTest(Test_Fido("test_fido_reg_receive"))
#     suit.addTest(Test_Fido("test_fido_reg_client"))
#     suit.addTest(Test_Fido("test_fido_reg_send"))
#     suit.addTest(Test_Fido("test_fido_auth_receive"))
#     suit.addTest(Test_Fido("test_fido_auth_client"))
#     suit.addTest(Test_Fido("test_fido_auth_send"))
#     runner = unittest.TextTestRunner()
#     runner.run(suit)
