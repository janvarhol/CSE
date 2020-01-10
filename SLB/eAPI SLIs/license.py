import json

from sseapiclient.tornado import SyncClient
client = SyncClient.connect('https://localhost', 'root', 'xxxxx', ssl_validate_cert=False)
print(json.dumps(client.api.license.check_usage(), indent=4))
print(json.dumps(client.api.license.get_current_license(), indent=4))


