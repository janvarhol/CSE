import salt.modules.cmdmod
import logging
import os


import requests
import json

# Disable insecure warning message
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = 'https://httpbin.org/post'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
payload = {'key1': 'value1', 'key2': 'value2'}



log = logging.getLogger(__name__)

def url_post():
    grains = {}
      
    try:
        r = requests.post(url, json=payload, headers=headers, verify=False)
        log.info("url_post call status code: " + r.status_code)
        if r.status_code == 200:
            log.info("JSON response: " + json.dumps(r.json()['json'], indent=4))
            grains['url_post'] = r.json()['json']
        else:
            grains['device_type'] = 'ERROR WITH POST CALL'
    except:
        log.error("Custom grain url_post error")
        
    
    event_tag='custom_grain/url_post'
    event_data={"url": url, "payload": payload}

    __salt__['event.send'](event_tag, event_data)
    return grains
