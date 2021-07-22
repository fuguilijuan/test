from BeautifulReport.BeautifulReport import result
import json
import requests
import sys
import os

sys.path.append(os.path.dirname(__file__).replace('/', '\\'))  # 集成到CICD时用到

url = "https://oapi.dingtalk.com/robot/send?access_token" \
      "=b1785c0fc03b862c95b019d02d00ae7f705241badbc6bb6fa28bbdd6da3eff6b "
header = {
    "Content-Type": "application/json"
}

def send_ding():
    """
    测试用例执行结果发送钉钉通知
    """
    if result[2] > 0:
        data_fail = {
            "msgtype": "text", "text": {
                "content": "测试结果：{}个接口用例执行完成，{}个接口有异常，详情请查阅邮箱附件！".format(
                    result[0], result[2])}, "at": {
                "isAtAll": True}}
        requests.post(url, headers=header, data=json.dumps(data_fail))
    else:
        data_pass = {
            "msgtype": "text",
            "text": {
                "content": "{}个接口用例执行完成，测试结果正常！".format(result[0])

            },
            "at": {
                "isAtAll": True
            }
        }
        requests.post(url, headers=header, data=json.dumps(data_pass))
    print('已发送钉钉通知')


