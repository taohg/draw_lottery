from common.database import DbHelper
from common.project_log import logger


class SysUser:

    def __init__(self):
        self.db_helper = DbHelper()
        pass

    def save_record(self, record):
        _sql = """
            insert into sys_user(
                user_account,
                user_password
            ) values (
                ?,
                ?
            )
        """
        self.db_helper.exec_sql(_sql, record)

    def get_list(self):
        _sql = """
            select * from sys_user
        """
        res_list = self.db_helper.query_sql(_sql)
        logger.debug(f'res_list:{res_list}')
        return res_list

    def get_record(self, user_account='', user_password=''):
        _sql2 = f"and user_password = '{user_password}'" if user_password else ''
        _sql = f"""
            select * 
            from (
                SELECT t1.user_account , t1.user_password , t1.is_supper 
                from sys_user t1
                union all
                select t2.cust_account, t2.cust_password, 2
                from customer_info t2
            )
            where user_account = ?
            {_sql2}
        """
        res_list = self.db_helper.query_sql(_sql, query_para=(user_account, ))
        return res_list