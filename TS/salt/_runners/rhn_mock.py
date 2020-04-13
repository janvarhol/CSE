# -*- coding: utf-8 -*-
'''
Runner to interface with RHN tools mock.

This runner does a little trick using salt.execute runner
to execute module on a remote minion
'''
import logging

# Logging
log = logging.getLogger(__name__)

# Set minion acting as satellite server
# TODO: change this variable
satellite_server = 'tsystems'

def hammer_info(minion_id=None):
    if minion_id is not None:
        ret = __salt__['salt.execute'](satellite_server, 'rhn_mock.hammer_info', arg=[minion_id])
        log.info("RHN MOCK: RUNNER hammer_info: %s" % ret)

        if ret[satellite_server] == True:
            return True
        else:
            return False
    else:
        return False