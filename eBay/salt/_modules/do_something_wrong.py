# -*- coding: utf-8 -*-
'''
    Custom module with faulty code to genera exception error
    and call module cust_error_handler to handle the exception 
'''

import logging # required by Salt Logger
import sys # required to get exceptions info

log = logging.getLogger(__name__)

def send_msg(recipient,
        template,
        subject='Message from Salt',
        sender=None,
        server=None):

    log.info("recipient: %s", recipient)
    log.info("subject: %s", subject)

    mydict = []

    # try/except block to handle exceptions
    try:
        # Doing something wrong
        print(mydict['FAKEKEY'])
    except:
        # Salt looging
        log.error('Ooopps !!')

        # Capture exception info
        type, value, traceback = sys.exc_info()

        # Set event tag, use exceptions/"module_function_name"
        exception_tag = 'exceptions/adrian_send_msg'
        # Set event data dictionary
        exception_data = {"type": str(type), "value": str(value), "traceback": str(traceback)}
        # Sent exception data to custom module to send event
        __salt__['cust_error_handler.send_event'](exception_tag, exception_data)

        return False

    return True
    
