import logging
import logging.handlers as handlers
import time

# create logger
logger = logging.getLogger('ThreadExtruder')
logger.setLevel(logging.DEBUG)


# create file handler and set level to debug
fh = handlers.TimedRotatingFileHandler('logging.log',when='D', interval=7, backupCount=7)

fh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to fh
fh.setFormatter(formatter)

# add ch to logger
logger.addHandler(fh)