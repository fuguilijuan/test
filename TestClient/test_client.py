import jpype
import os

class TestClient:
    """
    调用java方法
    """
    def __init__(self):
        """获取当前路径"""
        self.ext_classpath = os.path.dirname(__file__)

    def fido_testclient(self, uafRequest=None, AuthUserName='username', isAddUVI='0'):
        """
        指纹：调用java方法，注册和认证都调用这个方法
        :param uafRequest:指纹接口返回的uafRequest
        :param AuthUserName:注册时的用户名
        :param isAddUVI:不清楚，默认给0
        :return:
        """
        if uafRequest is not None:
            try:
                # jpype.java.lang.System.out.println('hello world!')
                javaClass = jpype.JClass('com.gm.uaf.client.UAFTestClient')  # 包名.类名
                jd = javaClass("{}\\client.properties".format(self.ext_classpath))  # 实例化java类
                response = eval(str(jd.process(uafRequest, AuthUserName, isAddUVI)))  # process是java的方法，调用方法
                return response
            except Exception as e:
                return 'testclient get data error：{}'.format(e)
        return None

    def cert_testclient(self, uafRequest=None):
        """
        证书：证书注册调用此方法
        :param uafRequest: 证书发起接口返回的uafRequest
        :return:
        """
        if uafRequest is not None:
            try:
                util=jpype.JClass('com.gm.jolt.sampler.ConfigUtil')
                util.init("{}\\client.properties".format(self.ext_classpath))
                try:
                    javaClass = jpype.JClass('com.gm.jolt.sampler.UAFCertService')
                    jd = javaClass()
                    response = jd.createRegAssertion(uafRequest)
                    return str(response)
                except Exception as e:
                    return 'testclient get data error：{}'.format(e)
            except Exception as e:
                return 'init  error：{}'.format(e)
        return None

    @staticmethod
    def save_cert_client(uafRequest=None, save='0'):
        """
        证书注册时send接口调用此方法，返回的keyid用来组装：更新证书状态为已安装接口数据
        :param save: jmeter传的就是0
        :param uafRequest: 证书send接口返回的uafRequest
        :return:
        """
        if uafRequest is not None:
            try:
                javaClass = jpype.JClass('com.gm.jolt.sampler.UAFCertService')  # 包名.类名
                jd = javaClass()
                response = jd.saveCert(uafRequest, save)
                return eval(str(response))
            except Exception as e:
                return 'testclient get data error：{}'.format(e)
        return None

    @staticmethod
    def cert_auth_client(uafRequest=None):
        """
        证书认证时调用
        :param uafRequest:
        :return:
        """
        if uafRequest is not None:
            try:
                javaClass = jpype.JClass('com.gm.jolt.sampler.UAFCertService')  # 包名.类名
                jd = javaClass()
                response = jd.createAuthAssertion(uafRequest)
                return str(response)
            except Exception as e:
                return 'testclient get data error：{}'.format(e)
        return None

    def del_json_flie(self):
        """
        指纹：
        每次注册+认证，新生成AuthenticatorInfo.json文件
        注册+认证完成后删除AuthenticatorInfo.json文件
        :return:
        """
        all_file = os.listdir(self.ext_classpath)
        if 'AuthenticatorInfo.json' in all_file:
            os.remove(self.ext_classpath + '\\AuthenticatorInfo.json')
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


def new_testclient_obj():
    """
    实例化TestClient
    :return:
    """
    t = TestClient()
    return t

