import sqlite3
import random
import traceback
from common.config import load_config
from common.project_log import logger


class DbHelper:
    def __init__(self):
        def dict_factory(cursor, row):
            """
            返回 dict 形式的行，将列名映射到相应的值
            :param cursor:
            :param row:
            :return:
            """
            fields = [column[0] for column in cursor.description]
            return {key: value for key, value in zip(fields, row)}

        sys_config = load_config()
        self.conn = sqlite3.connect(sys_config.get('db_file'), check_same_thread=False)
        # self.conn = sqlite3.connect(r'F:\tmp\test_sqlite\demo.db', check_same_thread=True)
        # self.conn.row_factory = sqlite3.Row
        self.conn.row_factory = dict_factory
        self.cursor = self.conn.cursor()

    def query_sql(self, query_sql: str, query_para=None) -> list:
        res = None
        try:
            if query_para:
                res = self.cursor.execute(query_sql, query_para)
            else:
                res = self.cursor.execute(query_sql)
        except:
            logger.error(query_sql)
            logger.error(traceback.format_exc())
        else:
            logger.debug(query_sql)
            res = res.fetchall()
        return res

    def exec_sql(self, exec_sql: str, exec_para):
        try:
            if type(exec_para) == tuple:
                self.cursor.execute(exec_sql, exec_para)
            elif type(exec_para) == list:
                self.cursor.executemany(exec_sql, exec_para)
        except:
            self.conn.rollback()
            logger.error(traceback.format_exc())
            return -1
        else:
            self.conn.commit()
            return self.conn.total_changes

    def __del__(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except:
            print(traceback.format_exc())


if __name__ == '__main__':
    _sql = """
    
    select t1.name, t2.name as name2, t1.create_time from test_taohg t1, test_taohg2 t2
    where t1."type" = t2."type" ;
    """
    db_helper = DbHelper()
    res = db_helper.query_sql(_sql, '')
    for item in res:
        print(item['name'], item['name2'])
        logger.debug(item)
        # print(item.get('name'), item.get('name2'))

    _sql = """
        insert into test_taohg(type, name) values (?, ?)
    """
    res = db_helper.exec_sql(_sql, (random.randint(10, 20), 'test'))
    print(res)
