
from TestApi.Web.view import login, index
from TestApi.Web import app
from flask_cors import *
import datetime


CORS(app, supports_credentials=True)  # 解决跨域问题
app.secret_key = "TPmi4aLWRbyVq8zu9v82dWYW1"  # session方式登录需要配置
app.permanent_session_lifetime = datetime.timedelta(seconds=10 * 60) #session设置10分钟

"""注册视图函数"""
app.register_blueprint(login.blue)
app.register_blueprint(index.blue)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
