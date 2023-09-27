from business.sys_user import SysUser
from business.customer_info import CustomerInfo

def add_customer_info(record_list):
    customer_info_dao = CustomerInfo()
    customer_info_dao.save_record(record_list=record_list)

def get_sys_user():
    sys_user_dao = SysUser()
    return sys_user_dao.get_list()