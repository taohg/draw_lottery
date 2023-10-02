import json
import os
import datetime
from flask import Flask, render_template, request, make_response, session, redirect, url_for
from werkzeug.utils import secure_filename

from common.config import load_config
from common.project_log import logger
from common.project_util import md5, Pagination
from common import sys_constant as const
from business import main_business as mb

app = Flask(__name__)
app.secret_key = 'shiyongzhegexitongnengbianfu'
app.permanent_session_lifetime = datetime.timedelta(seconds=60 * 10)
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
        user_password = md5(request.form.get('user_password'))
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
            session['user_account'] = user_account
            session['role_key'] = tmp_list[0].get('is_supper')
            session['role_name'] = const.SYS_ROLE[tmp_list[0].get('is_supper')]
            session['is_login'] = 'true'
            if tmp_list[0].get('is_supper') in [0, 1]:
                # res = make_response(redirect(url_for('sys_index')))
                res = make_response(redirect(url_for('sys_index2')))
                res.set_cookie("test_cookie", "test_value", max_age=60*60*24)
                res.set_cookie("user_account", user_account, max_age=60*60*24)
                res.set_cookie("user_password", user_password, max_age=60*60*24)
                return res
            else:
                res = make_response(redirect(url_for('cust_index')))
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
    if _url in pass_list or _url.endswith('.css') or _url.endswith('.js') or _url.endswith('.jpeg') or _url.endswith(
            '.map'):
        pass
    elif session.get('is_login') is None:
        user_account = request.cookies.get('user_account')
        user_password = md5(request.cookies.get('user_password'))
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


@app.route("/sys_index", methods=['GET', 'POST'])
def sys_index():
    """
    系统经理登录成功后默认页面
    :return:
    """
    page_content = {
        'current_user': session['user_account'],
        'role_key': session['role_key'],
        'role_name': session['role_name'],
    }
    return render_template('sys_index.html', page_content=page_content)


@app.route("/sys_index2", methods=['GET', 'POST'])
def sys_index2():
    """
    系统经理登录成功后默认页面
    :return:
    """
    page_content = {
        'current_user': session['user_account'],
        'role_key': session['role_key'],
        'role_name': session['role_name'],
    }
    return render_template('sys_index2.html', page_content=page_content)


@app.route("/cust_index", methods=['GET', 'POST'])
def cust_index():
    """
    客户账号登录成功后默认页面
    :return:
    """
    page_content = {
        'current_user': session['user_account'],
        'role_key': session['role_key'],
        'role_name': session['role_name'],
    }
    return render_template('cust_index.html', page_content=page_content)


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        if not os.path.exists(os.path.join(sys_config.get('upload_dir'))):
            os.mkdir(os.path.join(sys_config.get('upload_dir')))
        f.save(os.path.join(sys_config.get('upload_dir'), secure_filename(f.filename)))
        return 'file uploaded successfully'


@app.route('/add_cust_info', methods=['POST'])
def add_cust_info():
    form_data = {}
    form_data.update(request.form)
    form_data.update({
        'create_user': session['user_account'],
        'create_time': datetime.datetime.now().strftime(const.DATETIME_FORMATTER)
    })
    return mb.add_customer_info(request.form)


@app.route("/get_cust_list", methods=['GET', 'POST'])
def get_customer_list():
    user_account = session['user_account']
    page = 1
    rows = 10
    if request.method.upper() == 'GET':
        page = int(request.args.get('page'))
        rows = int(request.args.get('rows'))
    else:
        page = int(request.form.get('page'))
        rows = int(request.form.get('rows'))
    data_list = mb.get_customer_list(user_account=user_account)
    pagination = Pagination(data_list=data_list, page_size=rows, page_num=page)
    return pagination.get_result()


@app.route("/get_sys_user", methods=['GET', 'POST'])
def get_sys_user():
    v_list = [{'cust_name': 'aaaa'}]
    mb.add_customer_info(v_list)
    # return 'json.dumps(mb.get_sys_user())'
    return json.dumps(mb.get_sys_user())


if __name__ == '__main__':
    app.run(host=sys_config.get('host'), port=sys_config.get('port'))
    # app.run(host=sys_config.get('host'), port='8001', debug=True)
