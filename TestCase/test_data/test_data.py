from TestApi.Config.common import CONF,FLAG
import yaml
import random
import os
import json

username = 'test-gmrz{}'.format(random.randint(111111111,9999999999))
deviceid = 'HW5Dqw5zr5QWERTYUIOPA9D6GHJKLZXtcs{}'.format(random.randint(111111111,9999999999))

# testcase.json是拷贝了一份原始yalm数据，并把动态数据填充到json，这样保证原始数据没有被更改，web页面展示的是json数据
json_file = os.path.dirname(__file__) + '\\testcase.json'
# test_data.yalm为原始数据，供测试用例调用
yalm_path = os.path.dirname(__file__) + '\\test_data.yalm'
with open(str(yalm_path), encoding='utf-8') as f:
    data_file = yaml.load(f, Loader=yaml.FullLoader)

def test_data(case_name):
    """
    :param case_name: 根据用例名称动态填充数据
    :return:
    """
    if FLAG == 0:
        # rd为web页面每次执行测试，生成一个随机数，用来拼接username和deviceid
        rd = CONF[0]['rd']
        userName = 'test-gmrz{}'.format(rd)
        deviceID = 'HW5Dqw5zr5QWERTYUIOPA9D6GHJKLZXtcs{}'.format(rd)
        # CONF[1]判断是否使用web页面手动修改的用例
        if CONF[1]:
            all_data = CONF[1]
            if case_name in all_data:
                if 'userName' in all_data[case_name]['context']:
                    if all_data[case_name]['context']['userName']=="":
                        all_data[case_name]['context']['userName'] = userName
                if 'devices' in all_data[case_name]['context']:
                    if all_data[case_name]['context']['devices']['deviceID']=="":
                        all_data[case_name]['context']['devices']['deviceID'] = deviceID
                # 数据填充后写入文件，供web页面展示
                with open(str(json_file), 'w', encoding='utf-8') as fp:
                    fp.write(json.dumps(all_data, ensure_ascii=False, indent=4))
                return all_data[case_name]
            return False
        else:
            all_data = data_file
            if case_name in all_data:
                if 'userName' in all_data[case_name]['context']:
                    all_data[case_name]['context']['userName'] = userName
                if 'devices' in all_data[case_name]['context']:
                    all_data[case_name]['context']['devices']['deviceID'] = deviceID
                with open(str(json_file), 'w', encoding='utf-8') as fp:
                    fp.write(json.dumps(all_data, ensure_ascii=False, indent=4))
                return all_data[case_name]
            return False
    else:
        all_data = data_file
        if case_name in all_data:
            if 'userName' in all_data[case_name]['context']:
                all_data[case_name]['context']['userName'] = username
            if 'devices' in all_data[case_name]['context']:
                all_data[case_name]['context']['devices']['deviceID'] = deviceid
            return all_data[case_name]
        return False

def send_uafResponse(case_name, uafResponse):
    """
    处理testclient返回的数据uafResponse，组装send请求报文
    :param case_name:用例名称
    :param uafResponse:testclient返回的uafResponse
    :return:
    """
    if FLAG == 0:
        if CONF[1]:
            all_data = CONF[1]
            if case_name in all_data:
                if uafResponse is not None:
                    if isinstance(uafResponse, str):
                        dic = {
                            "uafResponse": '[{}]'.format(uafResponse)
                        }
                        all_data[case_name].update(**dic)
                    else:
                        all_data[case_name].update(**uafResponse)
                    with open(str(json_file), 'w', encoding='utf-8') as fp:
                        fp.write(json.dumps(all_data, ensure_ascii=False, indent=4))
                else:
                    pass
        else:
            all_data = data_file
            if case_name in all_data:
                if uafResponse is not None:
                    if isinstance(uafResponse, str):
                        dic = {
                            "uafResponse": '[{}]'.format(uafResponse)
                        }
                        all_data[case_name].update(**dic)
                    else:
                        all_data[case_name].update(**uafResponse)
                    with open(str(json_file), 'w', encoding='utf-8') as fp:
                        fp.write(json.dumps(all_data, ensure_ascii=False, indent=4))
                else:
                    pass
    else:
        all_data = data_file
        if case_name in all_data:
            if uafResponse is not None:
                if isinstance(uafResponse, str):
                    dic = {
                        "uafResponse": '[{}]'.format(uafResponse)
                    }
                    all_data[case_name].update(**dic)
                else:
                    all_data[case_name].update(**uafResponse)
            else:
                pass