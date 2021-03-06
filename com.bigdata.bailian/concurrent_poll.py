__author__ = 'blemall'

import os
import conf_utils
import commands
from log import Logger
from multiprocessing.dummy import Pool as ThreadPool

index = 0


def get_lines(f):
    tables = []
    path = "../docs/" + f
    if os.path.exists(path):
        for line in open(path):
            table = line.replace('\r\n', '').split('\t')
            if table is not None and table != "":
                tables.append(table)
    return tables


def get_cmd(placeholder, table, sid=True):
    if sid:
        cmd = placeholder.format(ip=table[0], port=table[1], sid=table[2], username=table[3], pwd=table[4],
                                 database=table[5], table=table[7], dir=table[6], hive_table=table[6], split_by=table[8],
                                 pvalue=conf_utils.get_day("%Y-%m-%d", -1))
    else:
        cmd = placeholder.format(ip=table[0], port=table[1], db=table[2], username=table[3],
                                 pwd=table[4], table=table[6], dir=table[5], hive_table=table[5],
                                 split_by=table[7], pvalue=conf_utils.get_day("%Y-%m-%d", -1))
    return cmd


def get_cmds():
    cmds = {}
    oracle_tables = get_lines('non.txt')
    mysql_tables = []
    for t in oracle_tables:
        cmd = get_cmd(conf_utils.get_kv_from_conf("cmds", "oracle_to_hive"), t)
        cmds.__setitem__(t[7], cmd)
    for t in mysql_tables:
        cmd = get_cmd(conf_utils.get_kv_from_conf("cmds", "mysql_to_hive"), t, False)
        cmds.__setitem__(t[6], cmd)
    return cmds


def exec_cmd(cmd):
    table = cmd[0]
    command = cmd[1]
    global index
    index += 1
    print(str(index) + " Starting import " + table)
    Logger.info("Starting import " + table)
    (status, text) = commands.getstatusoutput(command)
    if status != 0:
        print(table + 'status: ' + str(status))
        Logger.info("commands: " + command)
        Logger.info("End of import, status: " + str(status))
        Logger.info("End of import, content: " + text)


pool = ThreadPool(8)
pool.imap(exec_cmd, get_cmds().items())
pool.close()
pool.join()


if __name__ == '__main__':
    pass

