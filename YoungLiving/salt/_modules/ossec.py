# cat  /srv/salt/_modules/ossec.py
# -*- coding: utf-8 -*-
'''
Run ossec calls
:configuration:
    :depends: none
'''
import logging
import json
from datetime import datetime

#import time

log = logging.getLogger(__name__)

def list_agents():
    '''
    List agents status
    '''

    active_agents = []
    not_active_agents = []
    other_status_agents = []
    agents_status = {}

    ret = __salt__['cmd.run']('/root/list_agents.sh')
    agents_list = ret.split("\n")

    for agent_status in agents_list:
        if "is not active" in agent_status:
            not_active_agents.append(agent_status)
        elif "is active" in agent_status:
            active_agents.append(agent_status)
        else:
            other_status_agents.append(agent_status)

    agents_status['active'] = active_agents
    agents_status['not active'] = not_active_agents
    agents_status['other status'] = other_status_agents

    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    agents_status['last_scan'] = dt_string

    # Save to file
    if len(agents_status['not active']) > 0:
        with open('/tmp/not_active.json', 'w') as outfile:
            json.dump(agents_status['not active'], outfile)
    return agents_status

def email_status():
    '''
    Send email of not active agents
    '''

    agents_status = list_agents()

    try:
        ret = __salt__['smtp.send_msg']('amalaguti78@gmail.com', json.dumps(agents_status['not active'], indent=4), subject="ossec alert from Salt", sender='amalaguti78@gmail.com', server='email-smtp.us-east-1.amazonaws.com', username='AKIA3N7P2RQTAOD7GX6A', password='BKW1OVxK3M0J/2VjJHeq15xtsMUXk7cJbQ9q6kaIXENZ', attachments=['/tmp/not_active.json'])
        #ret = __salt__['smtp.send_msg']('ossecalerts@youngliving.com', json.dumps(agents_status['not active'], indent=4), subject='ossec alert from Salt', sender='noreply@youngliving.com', server='smtp.youngliving.com', attachments=['/tmp/not_active.json'])
    except:
        return "Failed to send email"

    return agents_status
