import hashlib

SALT_STRING = 'aaabbbccc'


def encrypt(text:str):
    # todo 开发阶段先暂时明文
    # obj = hashlib.md5(SALT_STRING.encode('utf-8'))
    # obj.update(text.encode('utf-8'))
    # res_string = obj.hexdigest()
    res_string = text
    return res_string


if __name__ == '__main__':
    res = encrypt('2024888')
    print(res)