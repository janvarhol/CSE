import requests
import json
import logging

# Disable insecure warning message
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Import HTTPError for requests.raise_for_status() function
from requests.exceptions import HTTPError

# import SaltInvocationError for testing (eB)
from salt.exceptions import SaltInvocationError


# GET DATA
url_get = 'https://httpbin.org/get'

log = logging.getLogger(__name__)
      
def get_minion_data():
    # GET DATA
    url_get = 'http://172.31.26.239:8080/minion_data?minion_id=0000001'
    try:
        res = requests.get(url_get, verify=False)
        log.info("url_post call status code: " + str(res.status_code))

        # REQUEST note:
        # if response: will return True for anything between 200 to 400, False otherwise

        # REQUEST note:
        # requests.raise_for_status() raises an HTTPError for certain status codes
        # If the status code indicate a successful request, the exception is not raised
        res.raise_for_status()

        # request status code
        # print(res.status_code)
    except HTTPError as http_err:
        #print('HTTP error occurred: ' + str(http_err))
        log.error('url_request module: HTTP error occurred: ' + str(http_err))
        #raise SaltInvocationError(str('http_err'))
        return {}
    except Exception as err:
        #print('Other error occurred: ' + str(err))
        log.error('url_request module: Other error occurred: ' + str(err))
        #raise SaltInvocationError(str(err))
        return {}
    else: # everything is fine, proceed
        if res.status_code == 200:
            log.info('url_request module: 200 query OK')
            #print("JSON response: " + json.dumps(res.json(), indent=4))
            
            # Some checking before returning data
            # Check data is dictionary and expected key 'origin' in data
            if type(res.json()) is dict and 'origin' in res.json():
                return res.json()
            else:
                return {}
        else:
            log.error('url_request module: Invalid response - not 200 code')
            #print("ERROR NOT 200")
            return {}

