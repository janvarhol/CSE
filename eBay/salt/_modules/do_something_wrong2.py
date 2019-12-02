# -*- coding: utf-8 -*-
'''
    Custom module with faulty code to genera exception error
    and call module cust_error_handler to handle the exception 
'''

import logging # required by Salt Logger
import sys # required to get exceptions info

log = logging.getLogger(__name__)

def do_wrong():
    mydict = []
    exception_tag = 'exceptions/do_something_wrong_send_msg'
    exception_data = {"type": "ABCTYPE", "value": "ABCVALUE", "traceback": "ABCTRACE}
    __salt__['cust_error_handler.send_event'](exception_tag, exception_data)
    return False
    
