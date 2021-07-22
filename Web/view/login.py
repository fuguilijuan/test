from flask import request, render_template, session, redirect
from TestApi.Web.view import blue

@blue.route('/login', methods=['GET','POST'])
def login():
    """登录页面"""
    session.permanent = True  # session开启
    if request.method == 'POST':
        name = request.form.get('name')
        pwd = request.form.get('pwd')
        if (name == 'test' and pwd == '123') or (name == '1' and pwd == '1'):
            session['name'] = name
            # print(request.cookies)
            return redirect('index')
        else:
            return render_template('login.html', msg='账号或密码错误，请重新输入！')
    return render_template('login.html')



