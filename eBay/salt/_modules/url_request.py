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

# POST DATA
url_post = 'https://httpbin.org/post'
headers_post = {'Content-type': 'application/json', 'Accept': 'application/json'}
payload_post = {'key1': 'value1', 'key2': 'value2'}

# GET DATA
url_get = 'https://httpbin.org/get'

# PUT DATA
url_put = 'https://httpbin.org/put'
payload_put = {'include_scan': True }


log = logging.getLogger(__name__)

def request_get():
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

def request_put(minion_id, include_scan=True):
    try:
        res = requests.put(url_put, json={'include_scan': include_scan}, verify=False)
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

def request_post():
    try:
        res = requests.post(url_post, json=payload_post, headers=headers_post, verify=False)
        #log.info("url_post call status code: " + str(res.status_code))

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
            print("JSON response: " + json.dumps(res.json()['json'], indent=4))
            return res.json()['json']
        else:
            log.error('url_request module: Invalid response - not 200 code')
            #print("ERROR NOT 200")
            return {}


        
def get_minion_data(minion_id):
    # GET DATA
    minion_id = str(minion_id)
    log.info("url_request get minjion_id: " + minion_id)
    url_get = 'http://172.31.26.239:8080/minion_data?minion_id=%' + minion_id
    log.info("url_request get string: " + url_get)
    
    try:
        res = requests.get(url_get, verify=False)
        log.info("url_request call status code: " + str(res.status_code))

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
            # Check data is dictionary and required key 'minion_id' in dictionary
            if type(res.json()) is dict and 'minion_id' in res.json():
                log.info('url_request module: response dictionary looks correct')
                return res.json()
            else:
                return {}
        else:
            log.error('url_request module: Invalid response - not 200 code')
            #print("ERROR NOT 200")
            return {}        
        
# post
#print(json.dumps(request_post(), indent=4, sort_keys=True))

#get
#url_response = request_get()
#print(type(url_response))
#print("response: " + str(url_response))
