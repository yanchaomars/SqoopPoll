__author__ = 'blemall'
from fabric.api import *

env.user='root'
env.hosts = ['10.201.48.1']
code_dir = '/root/wuzhen'


def deploy():
    put('/home/blemall/IdeaProjects/SqoopPoll', code_dir)