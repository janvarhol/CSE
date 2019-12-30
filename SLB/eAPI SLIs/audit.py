import json

from sseapiclient.tornado import SyncClient
client = SyncClient.connect('https://localhost', 'REDACTED', 'REDACTED', ssl_validate_cert=False)
print("configure audit:enabled and audit:valid_logins in /etc/raas/raas")
print(json.dumps(client.api.audit.get_audit(), indent=4))
