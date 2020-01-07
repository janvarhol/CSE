# cat keys_maintenance.py
# -*- coding: utf-8 -*-
'''
Runner to ...

'''
import json
import logging

# wheel
import salt.config
import salt.wheel
opts = salt.config.master_config('/etc/salt/master')
wheel = salt.wheel.WheelClient(opts)

# Logging
log = logging.getLogger(__name__)



def _minion_status():
    return __salt__['manage.status']()



def check_up(minions_up):
    try:
        with open('/tmp/total_down.json') as outfile:
            _total_down = json.load(outfile)
    except:
        _total_down = {}


    # Remove minions up from minions_down list
    for minion in minions_up:
        if minion in _total_down:
            _total_down.pop(minion, None)
            log.info("Keys Maintenance Runner - removing minion up %s from json list", minion)

    save_total_down(_total_down)



def check_down(minions_down):
    try:
        with open('/tmp/total_down.json') as outfile:
            _total_down = json.load(outfile)
    except:
        _total_down = {}


    # Update count
    for minion in minions_down:
        if minion in _total_down:
            _total_down[minion] = _total_down[minion] + 1
        else:
            _total_down[minion] = 1
        log.info("Keys Maintenance Runner - incrementing minion down count for %s", minion)

    return _total_down


def save_total_down(total_down):
    with open('/tmp/total_down.json', 'w') as outfile:
        json.dump(total_down, outfile)


def remove_keys(_total_down):
   for minion in list(_total_down):
       if _total_down[minion] > 3:
            wheel.cmd_async({'fun': 'key.delete', 'match': minion})
            log.warning("Keys Maintenance Runner - minion down exceeded limit, removing key for %s", minion)
            _total_down.pop(minion, None)


   return _total_down



def clean_outfile():
    try:
        with open('/tmp/total_down.json') as outfile:
            _total_down = json.load(outfile)
    except:
        log.error("Keys Maintenance Runner - can't open outfile")

    for minion in list(_total_down):
        ret = wheel.cmd('key.name_match', [minion])
        if ret == {}:
            log.warning("Keys Maintenance Runner - minion key %s does not exist, removing from json", minion)
            _total_down.pop(minion, None)

    return _total_down




def update_down():
    # List minions up and down
    minions_status = _minion_status()

    # Remove minions up from down list
    check_up(minions_status['up'])

    # Increment counter for minions down
    total_down = check_down(minions_status['down'])

    # Remove keys for minions down exceeding limit
    total_down = remove_keys(total_down)

    # Save minions down list to json file
    save_total_down(total_down)

    # Remove unknown minions from json
    total_down = clean_outfile()
    save_total_down(total_down)

    return total_down
