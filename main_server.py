import json
import datetime
from flask import Flask, render_template, request, make_response, session, redirect, url_for

from common.config import load_config
from common.project_log import logger
from common.encryt_util import encrypt
from common import sys_constant as const
from business import main_business as mb

app = Flask(__name__)
app.secret_key = 'shiyongzhegexitongnengbianfu'
app.permanent_session_lifetime = datetime.timedelta(seconds=60*10)
sys_config = load_config()


@app.route("/default", methods=['GET', 'POST'])
def default():
    resp = make_response(f"欢迎使用【 {sys_config.get('project_name')} 】系统")
    resp.set_cookie("test_cookie", "test_value", max_age=3600)
    return resp
    # return f"欢迎使用【 {sys_config.get('project_name')} 】系统"

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    session.permanent = True
    request.cookies
    if request.method == 'GET':
        return render_template('login.html')

    # todo 登录后处理逻辑，如果校验成功则跳转到“登录后首页”，否则跳转登录页
    if request.form:
        user_account = request.form.get('user_account')
        user_password = encrypt(request.form.get('user_password'))
        tmp_list = mb.get_sys_user_record(user_account=user_account, user_password=user_password)
        if tmp_list:
            session['user_account'] = user_account
            # 方案一：通过render_template实现跳转到指定页面
            # res = make_response(render_template('main_success.html', page_content=page_content))
            # res.set_cookie("test_cookie", "test_value", max_age=3600)
            # res.set_cookie("user_account", user_account, max_age=3600)
            # res.set_cookie("user_password", user_password, max_age=3600)
            # return res
            # 方案二：通过redirect跳转到指定url
            res = make_response(redirect(url_for('main_success')))
            session['user_account'] = user_account
            session['role_key'] = tmp_list[0].get('is_supper')
            session['role_name'] = const.SYS_ROLE[tmp_list[0].get('is_supper')]
            session['is_login'] = 'true'
            res.set_cookie("test_cookie", "test_value", max_age=3600)
            res.set_cookie("user_account", user_account, max_age=3600)
            res.set_cookie("user_password", user_password, max_age=3600)
            return res
            # return render_template('main_success.html', page_content=page_content)
        return render_template('login.html', login_msg="账号密码有误！")


@app.before_request
def handle_before_request():
    _url = request.path
    print(f'- - - handle_before_request:{_url}')
    pass_list = ['/', '/login', '/logout', '/set_cookie', '/get_cookie']
    if _url in pass_list or _url.endswith('.css') or _url.endswith('.js') or _url.endswith('.jpeg') or _url.endswith('.map'):
        pass
    elif session.get('is_login') is None:
        user_account = request.cookies.get('user_account')
        user_password = encrypt(request.cookies.get('user_password'))
        if user_account and user_password:
            tmp_list = mb.get_sys_user_record(user_account=user_account, user_password=user_password)
            if tmp_list:
                session['is_login'] = 'true'
                session['user_account'] = user_account
                session['role_key'] = tmp_list[0].get('is_supper')
                session['role_name'] = const.SYS_ROLE[tmp_list[0].get('is_supper')]
        return redirect(url_for('login'))
        # return render_template('login.html', login_msg="")
    else:
        pass
    # return render_template('login.html', login_msg="")


@app.after_request
def handle_after_request(response):
    print('- - - handle_after_request')
    return response


@app.teardown_request
def handle_teardown_request(response):

    return response

@app.route("/set_cookie", methods=['GET'])
def set_cookie():
    res = make_response("设置了cookie")
    res.set_cookie("my_cookie", 'my_cookie_value', max_age=3600)
    return res

@app.route("/get_cookie", methods=['GET'])
def get_cookie():
    _cookie = request.cookies.get('my_cookie')
    print(f'_cookie: {_cookie}')
    return f"获取到的cookie是 {_cookie}"

@app.route("/hello", methods=['GET', 'POST'])
def hello():
    mb.get_sys_user_record(user_account='', user_password='')
    return render_template('hello.html')


@app.route("/main_success", methods=['GET', 'POST'])
def main_success():
    page_content = {
        'current_user': session['user_account'],
        'role_key': session['role_key'],
        'role_name': session['role_name'],
    }
    return render_template('main_success.html', page_content=page_content)


@app.route("/get_customer_list", methods=['GET', 'POST'])
def get_customer_list():

    user_account = request.args.get('u')
    res_list = mb.get_customer_list(user_account=user_account)
    return res_list


@app.route("/get_sys_user", methods=['GET', 'POST'])
def get_sys_user():

    v_list = [{'cust_name': 'aaaa'}]
    mb.add_customer_info(v_list)
    # return 'json.dumps(mb.get_sys_user())'
    return json.dumps(mb.get_sys_user())


if __name__ == '__main__':
    app.run(host=sys_config.get('host'), port=sys_config.get('port'))
    # app.run(host=sys_config.get('host'), port='8001', debug=True)
