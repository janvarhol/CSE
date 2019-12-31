import json

from sseapiclient.tornado import SyncClient
client = SyncClient.connect('https://localhost', 'root', 'saltstack!2019', ssl_validate_cert=False)
print(json.dumps(client.api.masterfs.get_masterfs(master_id='slb-master'), indent=4))


