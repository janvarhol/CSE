# -*- coding: utf-8 -*-
'''
Return cached data from minions
'''
from __future__ import absolute_import, print_function, unicode_literals
# Import python libs
import fnmatch
import logging
import os

# Import salt libs
import salt.config
from salt.ext import six
import salt.log
import salt.utils.args
import salt.utils.gitfs
import salt.utils.master
import salt.payload
import salt.cache
import salt.fileserver.gitfs
import salt.pillar.git_pillar
import salt.runners.winrepo
from salt.exceptions import SaltInvocationError
from salt.fileserver import clear_lock as _clear_lock

log = logging.getLogger(__name__)

__func_alias__ = {
    'list_': 'list',
}


def grain(tgt=None, tgt_type='glob', **kwargs):
    '''
    .. versionchanged:: 2017.7.0
        The ``expr_form`` argument has been renamed to ``tgt_type``, earlier
        releases must use ``expr_form``.
    Return cached grains of the targeted minions.
    tgt
        Target to match minion ids.
        .. versionchanged:: 2017.7.5,2018.3.0
            The ``tgt`` argument is now required to display cached grains. If
            not used, the function will not return grains. This optional
            argument will become mandatory in the Salt ``Sodium`` release.
    tgt_type
        The type of targeting to use for matching, such as ``glob``, ``list``,
        etc.
    CLI Example:
    .. code-block:: bash
        salt-run cache.grains '*'
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
    return cached_grains
