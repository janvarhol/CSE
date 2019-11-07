from concurrent.futures import TimeoutError
from sseapiclient.tornado import SyncClient
client = SyncClient.connect('https://XXXX', 'root', 'XXXXXX', ssl_validate_cert=False)
#print(client)

# Get target
print("TARGET: ")
print(client.api.tgt.get_target_group(tgt_uuid='380162d9-93bc-473a-9d16-3881b5eb7e4d'))
print("")

# Get role
print("ROLE: ")
print(client.api.auth.get_role(role_name='sys-mpzhlgumpi01'))
print("")


# Get group
print("ALL GROUPS: ")
print(client.api.auth.get_all_groups())
print("GROUP_LINKS: ")
print(client.api.auth.get_group_links())
print("GET GROUP: ")
print(client.api.auth.get_group(group_name='sys-mpzhlgumpi02-login', config_name='winad'))
print("")


# CREATE ROLE
print("CREATE ROLE")
#print(client.api.auth.save_role(role_name='sys-mpzhlgumpi02', perms=['schedule-read', 'cmd-read', 'returner-read', 'master-read', 'schedule-delete', 'minion-read', 'target-allminions-run', 'job-run', 'schedule-write', 'license-read', 'master-config-read', 'sec-policy-read', 'target-read', 'background_jobs-read', 'job-read', 'fs-read', 'metadata-auth-read', 'pillar-read']))
# NOTE: desc argument can't be set, automatically set to role_name
print("")


# CREATE GROUP and GROUP LINK
print("CREATE_GROUP:")
#print(client.api.auth.save_group(config_name='winad', group_name='sys-mpzhlgumpi02-login', roles=['User', 'sys-mpzhlgumpi02']))
# GROUP LINK
#print(client.api.auth.save_group_link(config_name='winad', group_name='sys-mpzhlgumpi02-login', ext_group_name='sys-mpzhlgumpi02-login'))
print("")



# CREATE TARGET and TARGET GROUP ACCESS
print("CREATE TARGET: ")
ret = client.api.tgt.save_target_group(name='mpzhlgumpi02',tgt={'*': {'tgt_type': 'list', 'tgt': 'mpzhlgumpi02'}})
# Use tgt_uuid
tgt_uuid = ret.ret
print("Target created: " + tgt_uuid)
#print(client.api.tgt.get_target_group(tgt_uuid=tgt_uuid))
print(client.api.tgt.save_target_group_access(tgt_uuid=tgt_uuid, access_payload={'sys-mpzhlgumpi02': {'read': True, 'write': False, 'discover': False, 'delete': False}}))
print("")