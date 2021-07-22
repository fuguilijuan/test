
from flask import Blueprint,request,session,redirect

blue = Blueprint('blue', __name__)

@blue.before_request
def is_login():
    """
    每个页面请求跳转前判断session是否登录，未登录跳转login
    :return:
    """
    if request.path == "/login":
        return None
    if not session.get("name"): # 对应login页面的用户名name属性
        return redirect("login")
    return None