__author__ = 'blemall'

import os
import commands
import time
from log import Logger
from multiprocessing.dummy import Pool as ThreadPool


ORACLE_TO_HIVE = "sqoop import --hive-import --connect jdbc:oracle:thin:@{ip}:{port}:{sid} --username {username}" \
                 " --password {pwd} --verbose --query 'select * from {table} where $CONDITIONS' --target-dir /usr/{dir} " \
                 " --split-by {split_by}  --hive-table {hive_table} --hive-database sourcedata --hive-partition-key 'dt' " \
                 " --hive-partition-value '{pvalue}' --fields-terminated-by '\\t'"
MYSQL_TO_HIVE = "sqoop import --hive-import --connect jdbc:mysql://{ip}:{port}/{db} --username {username} " \
                "--password {pwd} --verbose --query 'select * from {table} where $CONDITIONS' --target-dir /usr/{dir}  " \
                "--split-by {split_by}  --hive-table {hive_table} --hive-database sourcedata --hive-partition-key 'dt' " \
                "--hive-partition-value '{pvalue}' --fields-terminated-by '\\t'"


def get_lines(f):
    tables=[]
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
                                 pvalue=get_day("%Y-%m-%d", -1))
    else:
        cmd = placeholder.format(ip=table[0], port=table[1], db=table[2], username=table[3],
                                 pwd=table[4], table=table[6], dir=table[5], hive_table=table[5],
                                 split_by=table[7], pvalue=get_day("%Y-%m-%d", -1))
    return cmd


def get_cmds():
    cmds = []
    oracle_tables = get_lines('oracle.txt')
    mysql_tables = get_lines('mysql.txt')
    for t in oracle_tables:
        cmd = get_cmd(ORACLE_TO_HIVE, t)
        cmds.append(cmd)
    for t in mysql_tables:
        cmd = get_cmd(MYSQL_TO_HIVE, t, False)
        cmds.append(cmd)
    return cmds


def exec_cmd(cmd):
    Logger.info("Starting import...")
    print(cmd)
    count = 0
    count = count + 1
    print("current value: " + str(count))
    #(status, text) = commands.getstatusoutput(cmd)
    #print(cmd)
    #if status != 0:
    #    print('status: ' + status)
    #    Logger.info("End of import, status: " + str(status))
    #    Logger.info("End of import, content: " + text)


def get_day(fmt, ndays):
    day = time.strftime(fmt, time.localtime(time.time() + ndays * 24 * 60 * 60))
    return day


pool = ThreadPool(4)
r= pool.map(exec_cmd, get_cmds())
pool.close()
pool.join()


if __name__ == '__main__':
    pass
