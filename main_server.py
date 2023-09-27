import json

from flask import Flask, render_template

from common.config import load_config
from common.project_log import logger
from business import main_business as mb

app = Flask(__name__)
sys_config = load_config()


@app.route("/", methods=['GET', 'POST'])
def index():
    return f"欢迎使用【 {sys_config.get('project_name')} 】系统"


@app.route("/hello", methods=['GET', 'POST'])
def hello():
    return render_template('hello.html')


@app.route("/boot", methods=['GET', 'POST'])
def boot():
    return render_template('bootstrap.html')

@app.route("/getSysUser", methods=['GET', 'POST'])
def getSysUser():

    v_list = [{'cust_name': 'aaaa'}]
    mb.add_customer_info(v_list)
    # return 'json.dumps(mb.get_sys_user())'
    return json.dumps(mb.get_sys_user())


if __name__ == '__main__':
    app.run(host=sys_config.get('host'), port=sys_config.get('port'))
    # app.run(host=sys_config.get('host'), port='8001', debug=True)
