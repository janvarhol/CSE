# -*- coding: utf-8 -*-
'''
Module for saving exceptions data

'''

import csv
from datetime import datetime
import logging
log = logging.getLogger(__name__)


def exception_2csv(type="Unknown_type", value="Unknown_value", traceback="Unknown_traceback"):
    '''
    Save data to csv file
    '''
    today = datetime.now()
    d1 = today.strftime("%Y%m%d")
    d2 = today.strftime("%H%M%S")
    with open('/tmp/exceptions.csv', mode='a') as exceptions_records:
        exceptions_records_writer = csv.writer(exceptions_records, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        exceptions_records_writer.writerow([d1, d2, type, value, traceback])

    return True
