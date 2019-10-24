# -*- coding: utf-8 -*-
'''
Module for Sending Messages via SMTP - updating for mime.multipart
.. versionadded:: 2014.7.0
'''

import csv
from datetime import datetime
import logging
log = logging.getLogger(__name__)

def send_msg(recipient, subject, mac):
    log.info("recipient: %s", recipient)
    log.info("subject: %s", subject)
    log.info("mac: %s", mac)

    # send email...
    # blah
    # blah
    
    # save data to csv file
    save2csv(recipient, subject, mac)

    return True

def save2csv(recipient, subject, mac):
    '''
    Save data to csv file
    '''
    
    with open('/tmp/email_records.csv', mode='a') as email_records:
        email_records_writer = csv.writer(email_records, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        email_records_writer.writerow([datetime.now(), recipient, subject, mac])

    return True

