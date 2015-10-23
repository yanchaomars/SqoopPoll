__author__ = 'blemall'

import os
import conf_utils
import commands
import multiprocessing
from log import Logger
from multiprocessing.dummy import Pool as ThreadPool


def get_lines(f):
    tables = []
    path = "../docs/" + f
    if os.path.exists(path):
        for line in open(path):
            table = line.replace('\r\n', '').split('\t')
            tables.append(table)
    return tables


def get_cmd(placeholder, table, sid=True):
    if sid:
        cmd = placeholder.format(ip=table[0], port=table[1], sid=table[2], username=table[3], pwd=table[4],
                                 table=table[7], dir=table[6], hive_table=table[6], split_by=table[8],
                                 pvalue=conf_utils.get_day("%Y-%m-%d", -1))
    else:
        cmd = placeholder.format(ip=table[0], port=table[1], db=table[2], username=table[3],
                                 pwd=table[4], table=table[6], dir=table[5], hive_table=table[5],
                                 split_by=table[7], pvalue=conf_utils.get_day("%Y-%m-%d", -1))
    return cmd


def get_cmds():
    cmds = []
    oracle_tables = get_lines('oracle.txt')
    mysql_tables = get_lines('mysql.txt')
    for t in oracle_tables:
        cmd = get_cmd(conf_utils.get_kv_from_conf("cmds", "oracle_to_hive"), t)
        cmds.append(cmd)
    for t in mysql_tables:
        cmd = get_cmd(conf_utils.get_kv_from_conf("cmds", "mysql_to_hive"), t, False)
        cmds.append(cmd)
    return cmds


def exec_cmd(cmd):
    Logger.info("Starting import...")
    (status, text) = commands.getstatusoutput(cmd)
    print(cmd)
    if status != 0:
        print('status: ' + str(status))
        Logger.info("End of import, status: " + str(status))
        Logger.info("End of import, content: " + text)


cpus = multiprocessing.cpu_count()
pool = ThreadPool(cpus)
pool.imap(exec_cmd, get_cmds())
pool.close()
pool.join()


if __name__ == '__main__':
    pass
