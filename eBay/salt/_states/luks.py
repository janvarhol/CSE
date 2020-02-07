# -*- coding: utf-8 -*-
"""
Ensuring Disks are encrypted with the proper keys
=================================================

"""

from __future__ import absolute_import, print_function, unicode_literals
import logging
log = logging.getLogger(__name__)


def __virtual__():
    """TODO: Docstring for __virtual__.
    :returns: TODO

    """
    return 'luks'


NOT_ENCRYPTED_TMP = '{0} not on an encrypted volume'
ALREADY_WITH_KEY = '{0} already encrypted with key {1}'


def encrypted_with_key(name, key=None, slot=7, **kwargs):
    """Ensures that the given volume is encrypted with the given key in a
    particular slot

    :name: name of the volume to check
    :key: the key to encrypt the vo
    :returns: TODO

    """

    # Check for pillar encryption key
    #

    ret = {'changes': {},
           'comment': '',
           'name': name,
           'result': True}

    # Check for disk encryption on this disk


    # AM: I think this is no longer needed due with pass encrypted devices only
    #is_encrypted = __salt__['luks.on_encrypted'](name)
    #if not is_encrypted:
    #    ret['comment'] = NOT_ENCRYPTED_TMP.format(name)
    #    ret['result'] = False
    #    # Return immediately. The volume isn't encrypted
    #    return ret


    # AM: replaced luks module by luks_new
    # /srv/salt/_modules/luks_new.py
    log.info('--->>> STATE MOD 1. check key: ' + str(name) + ' ' + str(key))
    encrypted_with_key = __salt__['luks_new.check_key'](name, key)
    log.info('--->>> STATE MOD 1. check key: encrypted_with_key: ' + str(encrypted_with_key))

    # NOTE: WORKING FINE UP TO THIS LINE
    # luks_new.check_key is adding the key
    if not encrypted_with_key:
        ret['result'] = False
        ret['comment'] = 'Key not applied'

    '''
    if not encrypted_with_key:
        # Encrypt the volume with the key
        key_change_results = __salt__['luks_new.change_luks_key'](name,
                                                              key,
                                                              str(slot))

        ret['comment'] += '\n' + key_change_results['comment']
        log.debug('kcr %s', key_change_results)
        if not key_change_results['status']:
            ret['result'] = False
        else:
            encrypted_with_key = __salt__['luks_new.check_key'](name, key)
            ret['changes'] = key_change_results

    else:
        ret['comment'] += '\n' + ALREADY_WITH_KEY.format(name, '')
        ret['result'] = True
    '''
    return ret
