# -*- coding: utf-8 -*-
'''
    Module to handle exceptions errors thrown by other custom modules
    Faulty modules must be coded using try/except block
    On exception, call this module passing exception_tag string and 
    exception data dictionary which are used in the event tag
    and event data respectively
    
    It will send a Salt Event like this:
    exceptions/faultymodule_funcname	{
    "_stamp": "2019-10-25T16:48:54.022404",
    "cmd": "_minion_event",
    "data": {
        "traceback": "<traceback object at 0x7f9916303d40>",
        "type": "<type 'exceptions.TypeError'>",
        "value": "list indices must be integers, not str"
    },
    "id": "ebay",
    "pretag": null,
    "tag": "exceptions/faultymodule_funcname"
    }
    
    How to use in other module example code:
    try:
        # Doing something wrong
        print(mydict['FAKEKEY'])
    except:
        # Salt looging
        log.error('Ooopps !!')

        # Capture exception info
        type, value, traceback = sys.exc_info()

        # Set event tag, use exceptions/"module_function_name"
        exception_tag = 'exceptions/faultymodule_funcname'
        # Set event data dictionary
        exception_data = {"type": str(type), "value": str(value), "traceback": str(traceback)}
        # Sent exception data to custom module to send event
        __salt__['cust_error_handler.send_event'](exception_tag, exception_data)
       
        return False
'''    
    
    
import logging

log = logging.getLogger(__name__)

def send_event(exception_tag='exceptions/unknown_exception',
        exception_data={"type": "Unknown type", "value": "Unknown value", "traceback": "Unknown traceback"}):

    __salt__['event.send'](exception_tag, exception_data)

    return True
    
