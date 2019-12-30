import json

from sseapiclient.tornado import SyncClient
client = SyncClient.connect('https://localhost', 'REDACTED', 'REDACTED', ssl_validate_cert=False)
print(json.dumps(client.api.license.check_usage(), indent=4))
