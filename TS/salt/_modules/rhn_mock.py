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

        # Execute hammer command with Salt dunder
        rhn_info = __salt__['cmd.run_all']('/srv/salt/RHN_Satellite_Hammer/hammer.sh ' + minion_id)

        # Check for return code
        if rhn_info['retcode'] == 0:
            rhn_info_output = rhn_info['stdout']

            # Tweak output
            # Removing first line from string
            rhn_info_tweaked = rhn_info_output.split('\n', 1)[1:][0]
            # Loading data as JSON
            rhn_info_tweaked = json.loads(rhn_info_tweaked)

            log.info("RHN MOCK: hammer_info: %s" % rhn_info_tweaked)

            # Return required info
            # TODO: Verify the output when minion is not registered / not exist
            # EXAMPLE!!!!
            if 'Registered To' in rhn_info_tweaked['Subscription Information'].keys():
                if rhn_info_tweaked['Subscription Information']['Registered To'] is not False and rhn_info_tweaked['Subscription Information']['Registered To'] != "":
                    return True


            return False
    else:
        log.error("RHN MOCK: hammer_info: No minion id received")
        return False
