import json

from sseapiclient.tornado import SyncClient
client = SyncClient.connect('https://localhost', 'root', 'saltstack!2019', ssl_validate_cert=False)
print(json.dumps(client.api.stats.db_health(), indent=4))
print(json.dumps(client.api.stats.get_queue_size(), indent=4))


