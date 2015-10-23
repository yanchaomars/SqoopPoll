__author__ = 'blemall'

import time
import ConfigParser

confFile = "../conf/conf.cfg"
separator = ","


def get_kv_from_conf(section, key):
    conf = ConfigParser.RawConfigParser()
    conf.read(confFile)
    value = conf.get(section, key)
    return value


def get_day(fmt, ndays):
    day = time.strftime(fmt, time.localtime(time.time() + ndays * 24 * 60 * 60))
    return day


def main():
    v = get_kv_from_conf("cmds", "load_to_hive")
    print(v)

if __name__ == '__main__':
    main()