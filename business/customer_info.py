from common.database import DbHelper
from common.project_log import logger


class CustomerInfo:

    def __init__(self):
        self.db_helper = DbHelper()
        pass

    def save_record(self, record):
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
        add_tuple = (record.get('cust_name'),
                     record.get('link_name'),
                     record.get('link_phone'),
                     record.get('party_name'),
                     record.get('cust_logo'),
                     record.get('plan_date'),
                     record.get('user_num'),
                     record.get('cust_addr'),
                     record.get('cust_account'),
                     record.get('cust_password'),
                     record.get('act_date'),
                     record.get('is_act'),
                     record.get('create_user'),
                     record.get('create_time'),
                     record.get('remark'),
                     record.get('is_valid'))
        return self.db_helper.insert_sql(_sql, add_tuple)

    def edit_record(self, record):
        _sql = """
            update customer_info
            set cust_name = ?,
                link_name = ?,
                link_phone = ?,
                party_name = ?,
                cust_logo = ?,
                plan_date = ?,
                user_num = ?,
                cust_addr = ?,
                --cust_account = ?,
                --cust_password = ?,
                act_date = ?,
                --is_act = ?,
                --create_user = ?,
                --create_time = ?,
                update_user = ?,
                update_time = ?,
                remark = ?
            where id = ?
        """
        edit_tuple = (record.get('cust_name'),
                      record.get('link_name'),
                      record.get('link_phone'),
                      record.get('party_name'),
                      record.get('cust_logo'),
                      record.get('plan_date'),
                      record.get('user_num'),
                      record.get('cust_addr'),
                      # record.get('cust_account'),
                      # record.get('cust_password'),
                      record.get('act_date'),
                      # record.get('is_act'),
                      # record.get('create_user'),
                      # record.get('create_time'),
                      record.get('update_user'),
                      record.get('update_time'),
                      record.get('remark'),
                      record.get('cust_id'))
        return self.db_helper.exec_sql(_sql, edit_tuple)

    def del_record(self, record):
        _sql = """
            update customer_info
            set create_user = ?,
                create_time = ?,
                is_valid = ?
            where id = ?
        """
        del_tuple = (record.get('create_user'),
                     record.get('create_time'),
                     record.get('is_valid'),
                     record.get('cust_id'))
        return self.db_helper.insert_sql(_sql, del_tuple)

    def get_count(self) -> int:
        _sql = """
            select count(*) as data_cnt from customer_info
        """
        res_list = self.db_helper.query_sql(_sql)
        logger.debug(f'res_list:{res_list}')
        return res_list[0].get('data_cnt')

    def get_list(self):
        _sql = """
            select * from customer_info
            where is_valid = '0'
            order by id desc
        """
        res_list = self.db_helper.query_sql(_sql)
        logger.debug(f'res_list:{res_list}')
        return res_list

    def get_list_by_user(self, create_user=''):
        _sql = """
            select * from customer_info
            where is_valid = '0'
              and create_user = ?
            order by id desc
        """
        res_list = self.db_helper.query_sql(_sql, (create_user,))
        logger.debug(f'res_list:{res_list}')
        return res_list
