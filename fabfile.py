__author__ = 'blemall'
from fabric.api import *

env.user='root'
env.hosts = ['10.201.128.157']
code_dir = '/root/wuzhen/'
dest = code_dir + 'Sqoop'


def deploy():
    put('/home/blemall/SqoopPoll', dest)