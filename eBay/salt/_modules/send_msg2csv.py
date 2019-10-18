# -*- coding: utf-8 -*-
'''
Module for Sending Messages via SMTP - updating for mime.multipart
.. versionadded:: 2014.7.0
'''

import csv
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
    with open('/tmp/employee_file.csv', mode='w') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow([recipient, subject, mac])
        employee_writer.writerow([recipient, subject, mac])
    
    return True
