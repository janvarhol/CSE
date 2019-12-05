# -*- coding: utf-8 -*-
'''
An engine to save Salt events to Redis
Requires redis

TEST
1. salt-master -l info
2. salt-call event.send 'slb/custom/ret' '{status: completed}'

:configuration:
    Example configuration
    # cat /etc/salt/master.d/engines.conf

    .. code-block:: yaml
        engines:
          - test:
              tags: ['salt/job/*/ret/*', 'slb/custom/*']

        engines_dirs:
          - /srv/salt_engines

:depends:
    redis > python -m pip install redis

'''

# Import python libs
from __future__ import absolute_import, print_function, unicode_literals
import logging
import fnmatch
import redis

# Import salt libs
import salt.utils.event
import salt.utils.json

log = logging.getLogger(__name__)


def redis_set(redis_conn,event):
    #jevent = salt.utils.json.dumps(event)

    #Filter by event tag and save as JSON string
    if event['tag'].startswith('salt/job/'):
        print("PROCESSING SALT JOB EVENT")
        event_record = { "event_type": "salt_job_return", "tag": event['tag'], "more_info": event['data'] }
        jevent_record = salt.utils.json.dumps(event_record)

        try:
            redis_conn.set(event['data']['jid'], jevent_record)
        except:
            log.error("Engine unable to connect to Redis server")

        print("VERIFYING REDIS DATA")
        redis_data = redis_conn.get(event['data']['jid'])
        jredis_data = salt.utils.json.loads(redis_data)
        print(salt.utils.json.dumps(jredis_data, indent=4))

    elif event['tag'].startswith('slb/custom/'):
        print("PROCESSING SLB CUSTOM EVENT")
        event_record = { "event_type": "slb_custom", "tag": event['tag'], "more_info": event['data'] }
        jevent_record = salt.utils.json.dumps(event_record)

        try:
            redis_conn.set(event['data']['data']['__pub_jid'], jevent_record)
        except:
            log.error("Engine unable to connect to Redis server")

        print("VERIFYING REDIS DATA")
        redis_data = redis_conn.get(event['data']['data']['__pub_jid'])
        jredis_data = salt.utils.json.loads(redis_data)
        print(salt.utils.json.dumps(jredis_data, indent=4))
    else:
        log.warning("Engine unable to handle event type")

    return True

def start(tags):
    '''
    Listen to events and write them to a log file
    '''
    if __opts__['__role'] == 'master':
        event_bus = salt.utils.event.get_master_event(
                __opts__,
                __opts__['sock_dir'],
                listen=True)
        log.info('TEST ENGINE STARTED ON MASTER')
    else:
        event_bus = salt.utils.event.get_event(
            'minion',
            transport=__opts__['transport'],
            opts=__opts__,
            sock_dir=__opts__['sock_dir'],
            listen=True)
        log.debug('test engine started')

    # Establish Redis connection
    try:
        redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
    except:
        log.error("Engine unable to connect to Redis server")

    while True:
        event = event_bus.get_event(full=True)
        jevent = salt.utils.json.dumps(event, indent=4)
        #if event and event['tag'] in tags:
        if event:
            #Iterate thru tags list
            #Remove end '/' to match both strings
            if any(fnmatch.fnmatch(event['tag'].rstrip('/'), tag.rstrip('/')) for tag in tags):
                log.info("LOOKING FOR TAGS: " + str(tags))
                log.info("TAG: {} - PROCESSING NEW EVENT FOUND MATCHING: {}".format(event['tag'].rstrip('/'), jevent))
                redis_set(redis_conn,event)
