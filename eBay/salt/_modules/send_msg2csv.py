# -*- coding: utf-8 -*-
'''
Module for Sending Messages via SMTP - updating for mime.multipart

.. versionadded:: 2014.7.0

'''

import csv

log = logging.getLogger(__name__)


__virtualname__ = 'send_msg2csv'


def send_msg(recipient, subject, mac):
    log.info("recipient: %s", recipient)
    log.info("subject: %s", subject)
    log.info("mac: %s", mac))

    return True
