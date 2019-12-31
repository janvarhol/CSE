import json

from sseapiclient.tornado import SyncClient
client = SyncClient.connect('https://localhost', 'root', 'saltstack!2019', ssl_validate_cert=False)
print(json.dumps(client.api.ret.get_jids(), indent=4))
print(json.dumps(client.api.ret.get_jid(jid='20191228000349422099'), indent=4))
print(json.dumps(client.api.ret.get_load(master_id='slb-master', jid='20191228000349422099'), indent=4))

