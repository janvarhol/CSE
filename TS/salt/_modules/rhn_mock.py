# -*- coding: utf-8 -*-
'''
Interface with RHN tools mock
:configuration:
    :depends: none
'''
import logging
import json

log = logging.getLogger(__name__)

def hammer_info(minion_id=None):
    if minion_id is not None:
        rhn_info = __salt__['cmd.run_all']('/srv/salt/RHN_Satellite_Hammer/hammer.sh ' + minion_id)
        log.info(rhn_info)
    else:
        log.error("RHN MOCK: hammer_info: No minion id received")
        return False