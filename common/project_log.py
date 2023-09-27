import os
import logging
import sys
from logging.handlers import RotatingFileHandler
from common.config import load_config

sys_config = load_config()

# create formatter
formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s: %(message)s')

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(sys_config.get('log_level', logging.DEBUG))

# create console handler and set level to debug
ch = logging.StreamHandler()
# add formatter to ch
ch.setFormatter(formatter)

log_dir = sys_config.get('log_path')
log_name = sys_config.get('log_name', 'draw_lottery.log')
if not log_dir:
    log_dir = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'logs')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
fileHandler = RotatingFileHandler(filename=os.path.join(log_dir, log_name),
                                  mode='a',
                                  maxBytes=1024*1024*50,
                                  backupCount=10,
                                  encoding='utf-8')
fileHandler.setFormatter(formatter)

# add ch to logger
if sys_config.get('log_console', '').lower() == 'true':
    logger.addHandler(ch)
logger.addHandler(fileHandler)
