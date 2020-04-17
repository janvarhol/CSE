# -*- strcoding: utf-8 -*-
"""
A module to pull data from Foreman, via its API into the Pillar dictionary
Adapted for TS with the following changes:
1. Use minion_id and minion fqdn (from grains)
2. Return selected keys only, under subscription_facet_attributes,
tom2r719:
    ----------
    foreman:
        ----------
        subscription_facet_attributes:
            ----------
            activation_keys:
                |_
                  ----------
                  id:
                      34
                  name:
                      tc-rhel-ot_unix-activation-key-ux


Configuring the Foreman ext_pillar
==================================

Set the following Salt config to setup Foreman as external pillar source:

.. code-block:: yaml

  ext_pillar:
    - foreman_ts:
        key: foreman # Nest results within this key
        only: ['subscription_facet_attributes'] # Add only these keys to pillar

  foreman.url: https://example.com/foreman_api
  foreman.user: username # default is admin
  foreman.password: password # default is changeme

The following options are optional:

.. code-block:: yaml

  foreman.api: apiversion # default is 2 (1 is not supported yet)
  foreman.verifyssl: False # default is True
  foreman.certfile: /etc/ssl/certs/mycert.pem # default is None
  foreman.keyfile: /etc/ssl/private/mykey.pem # default is None
  foreman.cafile: /etc/ssl/certs/mycert.ca.pem # default is None
  foreman.lookup_parameters: True # default is True

An alternative would be to use the Foreman modules integrating Salt features
in the Smart Proxy and the webinterface.

Further information can be found on `GitHub <https://github.com/theforeman/foreman_salt>`_.

Module Documentation
====================
"""
from __future__ import absolute_import, print_function, unicode_literals

# Import python libs
import logging

from salt.ext import six

try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

__opts__ = {
    "foreman.url": "http://foreman/api",
    "foreman.user": "admin",
    "foreman.password": "changeme",
    "foreman.api": 2,
    "foreman.verifyssl": True,
    "foreman.certfile": None,
    "foreman.keyfile": None,
    "foreman.cafile": None,
    "foreman.lookup_parameters": True,
}


# Set up logging
log = logging.getLogger(__name__)

# Declare virtualname
__virtualname__ = "foreman_ts"



def resp_mock(minion_fqdn=None):
    '''
    Mock satellite server response
    '''
    satellite_resp = {
        'subscription_facet_attributes':
            { 'activation_keys':
                {
                    'id': 34,
                    'name': 'tc - rhel - ot_unix - activation - key - ux'
                }
            },
        'autoheal': True,
        'installed_products':
            {
                'arch': 'x86_64',
                'productId': 329,
                'productName': 'Red Hat Enterprise Linux Fast Datapath',
                'version': '7 Beta'
            }
    }

    satellite_resp_fqdn = {
        'subscription_facet_attributes':
            { 'activation_keys':
                {
                    'id': 99,
                    'name': 'tc - rhel - ot_unix - activation - key - ux'
                }
            },
        'autoheal': False,
        'installed_products':
            {
                'arch': 'x86_64',
                'productId': 999,
                'productName': 'Solaris 11 Super Cool App',
                'version': '11 Beta'
            }
    }


    if minion_fqdn is not None:
        return satellite_resp
    else:
        return satellite_resp_fqdn


def __virtual__():
    """
    Only return if all the modules are available
    """
    if not HAS_REQUESTS:
        return False
    return __virtualname__


def ext_pillar(minion_id, pillar, key=None, only=()):  # pylint: disable=W0613
    """
    Read pillar data from Foreman via its API.
    """
    url = __opts__["foreman.url"]
    user = __opts__["foreman.user"]
    password = __opts__["foreman.password"]
    api = __opts__["foreman.api"]
    verify = __opts__["foreman.verifyssl"]
    certfile = __opts__["foreman.certfile"]
    keyfile = __opts__["foreman.keyfile"]
    cafile = __opts__["foreman.cafile"]
    lookup_parameters = __opts__["foreman.lookup_parameters"]


    #log.info("EXT PILLAR FOREMAN: Querying Foreman at %s for information for %s", url, minion_id)


    # ADRIAN CODE TESTING BLOCK
    minion_fqdn = __grains__['fqdn']
    result = {}   # Variable used for returning pillar results
    resp = {}     # Variable used for satellite response
    #result = { "minion fqdn": minion_fqdn }


    # TODO: I don't think this code is right,
    #       It would be better to verify and check server responses codes and common exceptions
    try:
        log.info("EXT PILLAR FOREMAN: Querying Foreman at %s for information for %s", url, minion_id)
        resp = resp_mock(minion_fqdn)  # Change this to resp_mock() to get the code return by minion_fqdn
    except:
        log.debug("EXT PILLAR FOREMAN: minion_id: %s not found in Satellite server" % minion_id)

    if resp == {}:
        try:
            log.info("EXT PILLAR FOREMAN: Querying Foreman at %s for information using FQDN for %s" % minion_fqdn)
            resp = resp_mock(minion_fqdn)
        except:
            log.debug("EXT PILLAR FOREMAN: minion FQDN: %s not found in Satellite server" % minion_fqdn)

    result.update(resp)
    log.debug("EXT PILLAR FOREMAN: DEBUG RESULT PRE ONLY: %s" % result)

    if only:
        result = dict((k, result[k]) for k in only if k in result)

    log.debug("EXT PILLAR FOREMAN: DEBUG RESULT --POST-- ONLY: %s" % result)
    # ADRIAN CODE TESTING BLOCK END


    '''
    try:
        # Foreman API version 1 is currently not supported
        if api != 2:
            log.error(
                "Foreman API v2 is supported only, please specify"
                "version 2 in your Salt master config"
            )
            raise Exception

        headers = {"accept": "version=" + six.text_type(api) + ",application/json"}

        if verify and cafile is not None:
            verify = cafile

        resp = requests.get(
            url + "/hosts/" + minion_id,
            auth=(user, password),
            headers=headers,
            verify=verify,
            cert=(certfile, keyfile),
        )
        result = resp.json()

        log.debug("Raw response of the Foreman request is %s", result)

        if lookup_parameters:
            parameters = dict()
            for param in result["all_parameters"]:
                parameters.update({param["name"]: param["value"]})

            result["parameters"] = parameters

        if only:
            result = dict((k, result[k]) for k in only if k in result)

    except Exception:  # pylint: disable=broad-except
        log.exception("Could not fetch host data via Foreman API:")
        return {}


    if key:
        result = {key: result}
    '''


    return result