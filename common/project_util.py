import hashlib
from common import sys_constant as const


def md5(text:str):
    # todo 开发阶段先暂时明文
    # obj = hashlib.md5(const.MD5_SALT.encode('utf-8'))
    # obj.update(text.encode('utf-8'))
    # res_string = obj.hexdigest()
    # return res_string
    res_string = text
    return res_string


if __name__ == '__main__':
    res = md5('000')
    print(res)
