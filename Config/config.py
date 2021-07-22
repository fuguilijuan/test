from TestApi.Config.common import FLAG
import os
import json

def get_config():
    conf = {
        "tomcat": {
            "host": "192.168.6.187",
            "port": 8080
        },
        "mysql": {
            "host": "192.168.6.202",
            "port": 3306,
            "user": "root",
            "password": "123456",
            "database": "uap",
            "charset": "utf8mb4"
        },
        "redis": {
            "host": "192.168.6.207",
            "port": 6379,
            "password": 123456
        }
    }
    # web页面获取的数据库配置信息
    js_file = os.path.dirname(os.path.dirname(__file__)) + '\\Web\\view\\conf.json'
    with open(js_file) as fp:
        data = json.load(fp)
    if FLAG == 0:
        conf['tomcat']['host'] = data['host']
        conf['tomcat']['port'] = data['port']
        conf['mysql']['host'] = data['ip']
        conf['mysql']['database'] = data['db']
        conf['mysql']['user'] = data['name']
        conf['mysql']['password'] = data['pwd']
        return conf
    return conf


