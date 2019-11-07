import json
import sys
from concurrent.futures import TimeoutError
from sseapiclient.tornado import SyncClient

conn_settings = { 'url': 'https://172.31.3.83',
                'username': 'root',
                'password': 'salt',
                'ssl_validation': False,
                'DS_config_name': 'winad'}

print("SSE - AD integration")
try:
    client = SyncClient.connect(conn_settings['url'],
                                conn_settings['username'],
                                conn_settings['password'],
                                ssl_validate_cert=conn_settings['ssl_validation'])
    print("Connected to SSE")
except:
    print("Can't connect to SSE")
    sys.exit(1)


# JUST GETTING INFO FROM MANUALLY C:REATED OBJECT
def show_role_group_target(hostname):
    print("JUST GETTING SOME INFO FOR TESTING")

    # Get target
    print("TARGET INFO: ")
    try:
        ret = client.api.tgt.get_target_group(name=hostname)
        if ret[1]['results'] == []:
          print("TARGET DOES NOT EXIST")
        else:
          print(json.dumps(ret[1], indent=4))
    except:
        print("TARGET INFO NOT AVAILABLE")
    print("")

    # Get role
    print("ROLE INFO: ")
    try:
        ret = client.api.auth.get_role(role_name='sys-'+hostname)
        print(json.dumps(ret[1], indent=4))
    except:
        print("ROLE INFO NOT AVAILABLE")
    print("")


    # Get group and group links
    print("GROUP INFO: ")
    try:
        ret = client.api.auth.get_group(group_name='sys-'+hostname+'-login', config_name=conn_settings['DS_config_name'])
        print(json.dumps(ret[1], indent=4))
    except:
        print("GROUP INFO NOT AVAILABLE")
    print("")

    print("GROUP_LINKS: ")
    try:
        ret = client.api.auth.get_group_links(group_name='sys-'+hostname+'-login')
        if ret[1] == []:
            print("GROUP LINKS INFO DOES NOT EXIST")
        else:
            print(json.dumps(ret[1], indent=4))
    except:
        print("GROUP LINKS INFO NOT AVAILABLE")
    print("")


    return True

def create_role_group_target(hostname):
    # HERE STARTS THE REAL PROCESS
    # 1. client.api.auth.save_role(role_name='sys-mpzhlgumpi03', perms=['schedule-read', 'cmd-read', 'returner-read', 'master-read', 'schedule-delete', 'minion-read', 'target-allminions-run', 'job-run', 'schedule-write', 'license-read', 'master-config-read', 'sec-policy-read', 'target-read', 'background_jobs-read', 'job-read', 'fs-read', 'metadata-auth-read', 'pillar-read'])
    # 2. client.api.auth.save_group(config_name='winad', group_name='sys-mpzhlgumpi03-login', roles=['User', 'sys-mpzhlgumpi03'])
    # 3. client.api.auth.save_group_link(config_name='winad', group_name='sys-mpzhlgumpi03-login', ext_group_name='sys-mpzhlgumpi03-login'))
    # 4. client.api.tgt.save_target_group(name='mpzhlgumpi03',tgt={'*': {'tgt_type': 'list', 'tgt': 'mpzhlgumpi03'}})
    # 5. client.api.tgt.save_target_group_access(tgt_uuid=tgt_uuid, access_payload={'sys-mpzhlgumpi03': {'read': True, 'write': False, 'discover': False, 'delete': False}})


    # CREATE ROLE
    print("CREATE ROLE")
    print(client.api.auth.save_role(role_name='sys-'+hostname, perms=['schedule-read', 'cmd-read', 'returner-read', 'master-read', 'schedule-delete', 'minion-read', 'target-allminions-run', 'job-run', 'schedule-write', 'license-read', 'master-config-read', 'sec-policy-read', 'target-read', 'background_jobs-read', 'job-read', 'fs-read', 'metadata-auth-read', 'pillar-read']))
    # NOTE: desc argument can't be set, automatically set to role_name
    print("")


    # CREATE GROUP and GROUP LINK
    print("CREATE_GROUP:")
    print(client.api.auth.save_group(config_name=conn_settings['DS_config_name'], group_name='sys-'+hostname+'-login', roles=['User', 'sys-'+hostname]))
    # GROUP LINK
    print(client.api.auth.save_group_link(config_name=conn_settings['DS_config_name'], group_name='sys-'+hostname+'-login', ext_group_name='sys-'+hostname+'-login'))
    print("")



    # CREATE TARGET and TARGET GROUP ACCESS
    print("CREATE TARGET: ")
    ret = client.api.tgt.save_target_group(name=hostname,tgt={'*': {'tgt_type': 'list', 'tgt': hostname}})
    # Use tgt_uuid
    tgt_uuid = ret.ret
    print("Target created: " + tgt_uuid)
    print(client.api.tgt.get_target_group(tgt_uuid=tgt_uuid))
    print(client.api.tgt.save_target_group_access(tgt_uuid=tgt_uuid, access_payload={'sys-'+hostname: {'read': True, 'write': False, 'discover': False, 'delete': False}}))
    print
    return True



def main(hostname, *args):
    print("hostname = {}".format(hostname))

    if len(args) == 1:
        for arg in args:
            key_arg = arg.split("=")[0]
            value_arg = arg.split("=")[1]
            print("Keyword argument: {} = {}".format(key_arg, value_arg))

            if key_arg == "show_info" and value_arg == 'yes':
                show_role_group_target(hostname)
            elif key_arg == "show_info" and value_arg == 'no':
                create_role_group_target(hostname)

    elif len(args) == 0:
        print("Using shown_info = yes as default")
        show_role_group_target(hostname)
    else:
        print("Check command line syntax")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SyntaxError("Insufficient arguments.")
        print("Usage: python ad_import.py hostname show_info=yes/no")

    if len(sys.argv) == 3:
        # If there are enough arguments
        main(sys.argv[1], *sys.argv[2:])
    else:
        # Pass argument hostnae only, use default for show_info
        main(sys.argv[1])
