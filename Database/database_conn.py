from TestApi.Config import config
import pymysql

def execute_sql(sql=None):
    """
    执行sql语句
    :param sql:传入需要执行的sql语句
    :return:
    """
    db_conn=config.get_config()
    if 'mysql' in db_conn:
        try:
            db = pymysql.connect(**config.get_config()['mysql'])
            if sql is not None:
                cur = db.cursor()
                cur.execute(sql)
                db.commit()
                cur.close()
                db.close()
                return cur.fetchall()
            return db
        except Exception as e:
            return 'database connection error：\t{}'.format(e)

# print(execute_sql())


