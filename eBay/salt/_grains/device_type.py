import salt.modules.cmdmod
import logging
import os

log = logging.getLogger(__name__)

__salt__ = {
    'cmd.run': salt.modules.cmdmod._run_quiet,
    'cmd.retcode': salt.modules.cmdmod._retcode_quiet,
    'cmd.run_all': salt.modules.cmdmod._run_all_quiet,
}

DESKTOPS = ['Other', 'Desktop', 'Space-saving', 'Tower']
LAPTOPS = ['Laptop', 'Notebook']
SERVER = ['Server']
OTHER = ['Other']


def device_type():
    grains = {}
    
    # TESTING NOTE:
    # Using Debian for testing
    # Replace Debian by Raspbian
    # Set grains['device_type'] as needed
    #if os.uname()[3].startswith('Debian'):
    #    log.info("Debbie system")
    #    grains['device_type'] = 'Desktop'
    #    return grains
    hostname_cmd = salt.utils.path.which('hostnamectl')
    if hostname_cmd:
        desc = __salt__['cmd.run'](
            hostname_cmd,
            python_shell=False
        )
    log.info(desc)
        
        
    try:
        result = __salt__['cmd.run_all']('dmidecode --string chassis-type')
        
        if result['retcode'] == 0:
            log.info("TROUBLESHOOTING: ")
            log.info(result['stdout'])
            first_line = result['stdout'].splitlines()[0]
        
            if first_line in DESKTOPS:
                grains['device_type'] = 'Desktop'
            elif first_line in LAPTOPS:
                grains['device_type'] = 'Laptop'
            elif first_line in SERVER:
                grains['device_type'] = 'Server'
            elif first_line in OTHER:
                grains['device_type'] = 'Other'
            else:
                grains['device_type'] = 'Unknown'
        else:
            grains['device_type'] = 'ERROR'
    except Exception as e:
        log.error("Custom grain device_type error: " + e)
    return grains
