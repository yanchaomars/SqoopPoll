__author__ = 'blemall'

import datetime
import logging.handlers


def init_log():
    logger = logging.getLogger()
    today = str(datetime.date.today())
    log_file = "../logs/"+today+".log"
    handler = logging.handlers.TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=40)
    formatter = logging.Formatter('%(asctime)19s %(levelname)-8s %(name)s %(threadName)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
Logger = init_log()


if __name__ == '__main__':
    pass
