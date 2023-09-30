from business.sys_user import SysUser
from business.customer_info import CustomerInfo

def add_customer_info(record_list):
    customer_info_dao = CustomerInfo()
    customer_info_dao.save_record(record_list=record_list)


def get_customer_list(user_account, user_password=''):
    """
    根据系统用户查询客户列表信息
    :param user_account:
    :param user_password:
    :return:
    """
    customer_info_dao = CustomerInfo()
    sys_user_dao = SysUser()
    res_list = []
    db_sys_user = sys_user_dao.get_record(user_account=user_account)
    if db_sys_user:
        if db_sys_user[0].get('is_supper') == 0:
            res_list = customer_info_dao.get_list()
        else:
            res_list = customer_info_dao.get_list_by_user(create_user=user_account)
    return res_list

def get_sys_user():
    sys_user_dao = SysUser()
    return sys_user_dao.get_list()


def get_sys_user_record(user_account, user_password):
    """
    查询用户账号信息
    :param user_account:
    :param user_password:
    :return:
    """
    sys_user_dao = SysUser()
    return sys_user_dao.get_record(user_account=user_account, user_password=user_password)