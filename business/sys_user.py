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