# -*- coding: utf-8 -*-
'''
Send LUKS related emails
'''

import logging
import json
from datetime import datetime, timedelta

log = logging.getLogger(__name__)


def last_update_24hs(last_notification):
    '''
    return True if last_notification was more than 24 hours ago
    '''



    # NOTE: verify correct format for last_notification
    # If last_notification value is not valid format
    # set it to now
    try:
        _last_notification = datetime.strptime(last_notification, '%a %b %d %H:%M:%S %Z %Y')
    except:
        log.info("--->> Last email notification datetime not found, OK to send another email")
        return True
    log.info("--->> last notification: " + str(_last_notification))
    #print(type(_last_notification))


    # Get now datetime
    now = datetime.now()
    log.info("--->> Now: " + str(now))
    #print(type(now))


    # Calculate difference between last notification and current datetime
    notification_delta = now - _last_notification
    log.info("--->> Notification delta: " + str(notification_delta))
    #print(type(notification_delta))


    # Set threshold (default hours=24)
    threshold_delta = timedelta(hours=24)
    log.info("--->> Threshold delta: " + str(threshold_delta))
    #print(type(threshold_delta))


    # Decide if it's ok to send another email or not
    if notification_delta > threshold_delta:
        log.info("--->> Last email sent over threshold delta, it's OK to send another email")
        return True
    else:
        log.info("--->> Email already sent in threshold time, DO NOT send another email")
        return False



def send_email(payload):
    log.info("--->> send_email payload: " + str(payload))

    # Verify if no email was sent in the last 24 hours
    # True: more than 24 hours since last email, send new email
    # False: email sent in the last 24 hours, do not send again
    notify = last_update_24hs(payload['last_notification'])

    if notify:
        log.info("--->> SENDING EMAIL to: " + payload['email'])
        __salt__['smtp.send_msg'](payload['email'], payload['email_subject'], username='_', password='_', sender='_', server='email-smtp.us-east-1.amazonaws.com', payload=payload)
        return True
    else:
        log.info("--->> NOT SENDING EMAIL")
        return False

#payload = {'mac': '0a:2d:bc:90:8a:64', 'reason': 'Network Configuration Failure', 'last_notification': 'Fri Jan 24 14:46:29 UTC 2020', 'description': 'doing some testing', 'name': 'adrian m', 'email_admin': False, 'minion_id': 'ebay', 'email': 'amalaguti78@gmail.com', 'max_fails': 7, 'num_fails': 4}

#print(send_email(payload))
