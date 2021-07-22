from TestApi.Config import config
import redis

def execute_redis():
    """
    :return:返回缓存连接对象
    """
    host = config.get_config()['redis']['host']
    port = config.get_config()['redis']['port']
    pwd = config.get_config()['redis']['password']
    try:
        conn = redis.StrictRedis(host=host, port=port, password=pwd)
        return conn
    except Exception as e:
        return 'redis connection error：{}'.format(e)

