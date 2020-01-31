# -*- coding: utf-8 -*-
'''
Runner to ...

'''
import logging

# Logging
log = logging.getLogger(__name__)


def run_plan():
    ret1 = __salt__['salt.execute']('youngliving', 'cmd.run_bg', arg=('export TF_IN_AUTOMATION="yes"; ./terraform apply --auto-approve plans/', 'cwd="/root/terraform/"', 'runas="root"'))
    return True
