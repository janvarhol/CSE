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
    # Import HTTPError for requests.raise_for_status() function
    from requests.exceptions import HTTPError

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


def __virtual__():
    """
    Only return if all the modules are available
    """
    if not HAS_REQUESTS:
        return False
    return __virtualname__

def satellite_get(id, url):
    resp = {}
    try:
        log.info("EXT PILLAR FOREMAN: Querying Foreman for %s" % (id))
        resp = requests.get(url + id)
        resp.raise_for_status()
    except HTTPError as http_err:
        connected = False
        log.error("EXT PILLAR FOREMAN: HTTP error occurred: %s" % http_err)
    except Exception as err:
        connected = False
        log.error("EXT PILLAR FOREMAN: EXCEPTION occurred: %s" % err)
    except:
        connected = False
        log.error("EXT PILLAR FOREMAN: Unable to connect to foreman!!")

    return resp


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


    # ADRIAN CODE TESTING BLOCK
    minion_fqdn = __grains__['fqdn']
    result = None
    url = 'http://172.31.26.239:8080/minion_data?minion_id='


    # GET by minion_fqdn or minion id
    # by minion_fqdn first
    log.info("EXT PILLAR FOREMAN: Querying Foreman - FQDN - at %s using %s as key for %s" % (url, minion_fqdn, minion_id))
    resp = satellite_get(minion_fqdn, url)
    # NOTE: #In my web service, when no record is found,
    # it returns an empty dict {}
    # but the HTTP response is valid, status code 200
    # 172.31.0.4 - - [21/Apr/2020 16:26:44] "GET /minion_data?minion_id=tsystems HTTP/1.1" 200 -
    if resp.status_code == 200 and resp.json() != {}:
        result = resp.json()
    else:
        # try by minion id
        resp = satellite_get(minion_id, url)
        log.info("EXT PILLAR FOREMAN: Querying Foreman - MINION_ID - at %s using %s as key for %s" % (url, minion_id, minion_id))
        if resp.status_code == 200 and resp.json() != {}:
            result = resp.json()

    log.info("EXT PILLAR FOREMAN: Querying Foreman response: %s" % (result))


    # Filter in selected keys
    if only and result is not None:
        result = dict((k, result[k]) for k in only if k in result)

    # Add 'foreman' (specified in conf file) key to result
    if key:
        result = {key: result}


    return result