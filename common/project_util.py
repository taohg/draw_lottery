import json
import hashlib
import datetime
import traceback
from json import JSONEncoder
from common import sys_constant as const
from common.project_log import logger

def md5(text:str):
    # todo 开发阶段先暂时明文
    # obj = hashlib.md5(const.MD5_SALT.encode('utf-8'))
    # obj.update(text.encode('utf-8'))
    # res_string = obj.hexdigest()
    # return res_string
    res_string = text
    return res_string

class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if type(o) == datetime:
            return o.strftime(const.DATETIME_FORMATTER)
        return super().default(o)


class Pagination:
    def __init__(self, data_list: list, page_size=10, page_num=1):
        self.data_list = data_list if data_list else []
        try:
            self.page_size = int(page_size)
        except:
            self.page_size = 10
            logger.error(f"page_size：{page_size} 参数不是数值")
            logger.error(traceback.format_exc())
        try:
            self.page_num = int(page_num)
        except:
            self.page_num = 1
            logger.error(f"page_num：{page_num} 参数不是数值")
            logger.error(traceback.format_exc())

    def get_result(self):
        _start = self.page_size * (self.page_num - 1)
        _end = self.page_size * self.page_num
        res_list = self.data_list[_start: _end]
        res_dict = {
            "total": len(self.data_list),
            "rows": res_list,
        }
        return json.dumps(res_dict, cls=MyJSONEncoder)



if __name__ == '__main__':
    res = md5('000')
    print(res)
