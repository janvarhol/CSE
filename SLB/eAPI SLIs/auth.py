import json

from sseapiclient.tornado import SyncClient
client = SyncClient.connect('https://localhost', 'root', 'saltstack!2019', ssl_validate_cert=False)
#print(json.dumps(client.api.api.discover(), indent=4))
print(dir(client))
#print(client._discovered_errors)
print(json.dumps(client.api_versions, indent=4))


