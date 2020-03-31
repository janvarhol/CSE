# cat get_files.py
import json

from sseapiclient.tornado import SyncClient
client = SyncClient.connect('https://X', 'root', 'X', ssl_validate_cert=False)


sse_files = client.api.fs.get_env(saltenv='base')[1]
# PRINTING ALL FILES FROM SSE
print(json.dumps(sse_files, indent=4))

# Exporting files
for sse_file in sse_files:
    sse_file_uuid = sse_file['uuid']
    #print(json.dumps(client.api.fs.get_file(file_uuid='c889d147-f104-4689-9ec7-905f84e3638e'), indent=4))
    file_path = client.api.fs.get_file(file_uuid=sse_file_uuid)[1]['path']
    file_contents = client.api.fs.get_file(file_uuid=sse_file_uuid)[1]['contents']

    print('################################################')
    print('File name: ' + file_path)
    print(file_contents)
