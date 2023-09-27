from flask import Flask, render_template

from common.config import load_config
from common.project_log import logger

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


if __name__ == '__main__':
    app.run(host=sys_config.get('host'), port=sys_config.get('port'))
    # app.run(host=sys_config.get('host'), port='8001', debug=True)
