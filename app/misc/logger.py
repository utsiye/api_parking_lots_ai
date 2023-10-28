from loguru import logger
import sys

logger.remove()
logger.add('./logs/errors.log', rotation='24h', retention='14 days', level='INFO', format='[{time}]     #{level}    [{file}]  -  [LINE:{line}]   {message}')
logger.add(sys.stderr, level='INFO', format='[{time}]     #{level}    [{file}]  -  [LINE:{line}]   {message}')
