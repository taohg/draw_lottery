from business.sys_user import SysUser
from business.customer_info import CustomerInfo
from common.config import load_config
from common.project_log import logger

sys_config = load_config()


def add_customer_info(param_data):
    customer_info_dao = CustomerInfo()
    data_cnt = customer_info_dao.get_count()
    record = dict()
    record.update(param_data)
    record.update({
        'cust_password': sys_config.get('cust_pwd'),
        'cust_account': f"admin88{str(data_cnt+1).rjust(3, '0')}",
        'is_valid': 0,
    })
    res = customer_info_dao.save_record(record=record)
    logger.debug(f'新增的客户编号是: {res}')
    return {'res_code': '0', 'res_msg': 'success'}


def edit_customer_info(param_data):
    customer_info_dao = CustomerInfo()
    record = dict()
    record.update(param_data)
    res = customer_info_dao.edit_record(record=record)
    logger.debug(f"{param_data.get('update_user')}修改了客户{param_data.get('cust_id')}")
    return {'res_code': '0', 'res_msg': 'success'}


def del_customer_info(param_data):
    customer_info_dao = CustomerInfo()
    data_cnt = customer_info_dao.get_count()
    record = dict()
    record.update(param_data)
    record.update({
        'is_valid': 1,
    })
    customer_info_dao.del_record(record=record)
    logger.debug(f"{param_data.get('update_user')}删除了客户{param_data.get('cust_id')}")
    return {'res_code': '0', 'res_msg': 'success'}


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