import json

from sseapiclient.tornado import SyncClient
client = SyncClient.connect('https://localhost', 'root', 'saltstack!2019', ssl_validate_cert=False)
print(json.dumps(client.api.settings.get_auth_config(), indent=4))
#print(json.dumps(client.api.settings.get_directory_preview_status(), indent=4))
print(json.dumps(client.api.settings.test_auth_config(config_name='winad',
ssl_validate_cert=False,
group_class='group',
group_search_filter='(&(objectClass=group)(|(sAMaccountName=SSE_ACCESS-MAIN)(sAMaccountName=NetEng_Admins)(sAMaccountName=SSE_ACCESS-ADMINS)))',
base_dn='OU=CSE,DC=winad,DC=lab',
bind_pw='saltstack!2019',
auth_bind_dn_filter='(objectclass=person)',
port=3268,
display_name='winad',
auth_bind_dn='CN=saltdomainjoinsrv  1030632,OU=_restricted,DC=winad,DC=lab',
bind_dn='CN=saltdomainjoinsrv  1030632,OU=_restricted,DC=winad,DC=lab',
preview_config=False,
user_search_filter='(objectClass=person)',
group_member_is_dn=True,
account_attr_name='sAMAccountName',
driver='ldap',
host='172.31.28.22',
sync_schedule=60,
group_search_base_dn='DC=winad,DC=lab',
person_class='person',
user_search_scope='SUBTREE',
user_search_base_dn='DC=winad,DC=lab',
group_attr_name='memberOf',
use_ssl=False,
remote_uid_attr_name='objectGUID',
group_search_scope='SUBTREE'
), indent=4))

print(json.dumps(client.api.settings.start_directory_preview(), indent=4))

