# cat /srv/salt/_runners/terraform.py
# -*- coding: utf-8 -*-
'''
Runner to ...

'''
import logging
import json
# Logging
log = logging.getLogger(__name__)


def create_plan(instance_name=None):
    if instance_name:
        ret = __salt__['salt.execute']('youngliving', 'state.sls', arg=['terraform.create_plan', 'pillar={"instance_name": ' + instance_name + '}'])
        for key in ret['youngliving'].keys():
            if ret['youngliving'][key]['result'] == True:
                # terraform template created
                return True, ret['youngliving'][key]['name']
    else:
        return False, "NO INSTANCE NAME"

def run_plan():
    ret = __salt__['salt.execute']('youngliving', 'cmd.run_bg', arg=('export TF_IN_AUTOMATION="yes"; ./terraform apply --auto-approve plans/', 'cwd="/root/terraform/"', 'runas="root"'))
    return True

def create_run(instance_name=None):
    if instance_name:
        ret = create_plan(instance_name)
        if ret[0] == True:
            run_plan()
            return True
    else:
        return False, "NO INSTANCE NAME"
