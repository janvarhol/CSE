# -*- coding: utf-8 -*-
'''
Return cached data from minions
'''
from __future__ import absolute_import, print_function, unicode_literals
# Import python libs
import logging


# Import salt libs
import salt.utils.master

log = logging.getLogger(__name__)


def grain(tgt=None, tgt_type='glob', grain='device_type', sort=False, **kwargs):
    '''
    Function similar to runner cache.grains
    Modified to look for a single grain
    
    Usage:
    salt-run master_cache.grain \* grain='device_type'
    
    Returns list of minions with given grain info and list of minions
    for which the grain was not found
    ebay:
      Debbie
    ebay-minion1:
      Desktop
    grain_not_found:
      - debian-811-1
      - ubuntu-nonenc-1
      - ubuntu16-enc-1
    '''
    if tgt is None:
        # Change ``tgt=None`` to ``tgt`` (mandatory kwarg) in Salt Sodium.
        # This behavior was changed in PR #45588 to fix Issue #45489.
        salt.utils.versions.warn_until(
            'Sodium',
            'Detected missing \'tgt\' option. Cached grains will not be returned '
            'without a specified \'tgt\'. This option will be required starting in '
            'Salt Sodium and this warning will be removed.'
        )

    pillar_util = salt.utils.master.MasterPillarUtil(tgt, tgt_type,
                                                     use_cached_grains=True,
                                                     grains_fallback=False,
                                                     opts=__opts__)
    cached_grains = pillar_util.get_minion_grains()
    
    cached_grain = {}
    cached_grain['grain_not_found'] = []
    
    log.debug("Looking grains cache info for grain: " + grain)
    
    # Default is not sort the output
    if not sort:
        for minion in cached_grains:
            if grain in cached_grains[minion]:
                cached_grain[minion] = cached_grains[minion][grain]
            else:
                cached_grain['grain_not_found'].append(minion)
    else:
    # Sort output by grain
        for minion in cached_grains:
            if grain in cached_grains[minion]:
                if cached_grains[minion][grain] not in cached_grain:
                    cached_grain[cached_grains[minion][grain]] = []
                    cached_grain[cached_grains[minion][grain]].append(minion)
                else:
                    cached_grain[cached_grains[minion][grain]].append(minion)
            else:
                cached_grain['grain_not_found'].append(minion)
                    
        
    
    return cached_grain


