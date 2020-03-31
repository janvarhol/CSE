# cat del_auth_config.py
import json

from sseapiclient.tornado import SyncClient
client = SyncClient.connect('https://X', 'root', 'XXX', ssl_validate_cert=False)

print(json.dumps(client.api.settings.get_auth_config(), indent=4))


#ret = client.api.settings.delete_auth_config(config_name='fakewidad')
#print(ret)
