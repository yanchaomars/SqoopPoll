__author__ = 'blemall'
from fabric.api import *

env.user = 'root'
env.hosts = ['10.201.48.1']
code_dir = '/root/wuzhen/'
dest = code_dir + 'SqoopPoll'


def deploy():
    # with cd(code_dir):
    #     sudo('rm -r *')
    #     sudo('mkdir SqoopPoll')
    put('/home/blemall/SqoopPoll/', code_dir)
    # with cd(dest):
    #     cd('com.bigdata.bailian/')
    #     run('python concurrent_poll.py')