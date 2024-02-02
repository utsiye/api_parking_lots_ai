import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('main_logger')

logger.setLevel(logging.INFO)
format_log = logging.Formatter(u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s')
handler = TimedRotatingFileHandler(filename='./logs/errors.log', when='d', interval=1, backupCount=14)

handler.setFormatter(format_log)

console_out = logging.StreamHandler()

logger.addHandler(console_out)
logger.addHandler(handler)
