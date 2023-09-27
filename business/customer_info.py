from common.database import DbHelper
from common.project_log import logger


class CustomerInfo:

    def __init__(self):
        self.db_helper = DbHelper()
        pass

    def save_record(self, record_list):
        _sql = """
            insert into customer_info(
                --id,
                cust_name,
                link_name,
                link_phone,
                party_name,
                cust_logo,
                plan_date,
                user_num,
                cust_addr,
                cust_account,
                cust_password,
                act_date,
                is_act,
                create_user,
                create_time,
                remark,
                is_valid
            ) values (
                --?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """
        add_list = [(i.get('cust_name'),
                     i.get('link_name'),
                     i.get('link_phone'),
                     i.get('party_name'),
                     i.get('cust_logo'),
                     i.get('plan_date'),
                     i.get('user_num'),
                     i.get('cust_addr'),
                     i.get('cust_account'),
                     i.get('cust_password'),
                     i.get('act_date'),
                     i.get('is_act'),
                     i.get('create_user'),
                     i.get('create_time'),
                     i.get('remark'),
                     i.get('is_valid')) for i in record_list]
        self.db_helper.exec_sql(_sql, add_list)

    def get_list(self):
        _sql = """
            select * from customer_info
        """
        res_list = self.db_helper.query_sql(_sql)
        logger.debug(f'res_list:{res_list}')
        return res_list