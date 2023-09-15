import os
import sys
import configparser

BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))


def load_config():
    """
    加载所有的配置
    :return:
    """
    res_config = {}
    global BASE_PATH
    if not os.path.exists(BASE_PATH):
        BASE_PATH = os.path.dirname(os.path.dirname(__file__))
    config = configparser.ConfigParser()
    config.read(os.path.join(BASE_PATH, 'setting.ini'), encoding='utf-8')
    for section in config.sections():
        for k, v in config.items(section):
            res_config[k] = v
    return res_config


if __name__ == '__main__':
    # print(__file__)
    # print(BASE_PATH)
    # print(os.path.dirname(os.path.dirname(__file__)))
    res = load_config()
    print(res)
