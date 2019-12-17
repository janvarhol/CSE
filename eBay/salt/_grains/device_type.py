import salt.modules.cmdmod
import logging
import subprocess

log = logging.getLogger(__name__)

__salt__ = {
    'cmd.run': salt.modules.cmdmod._run_quiet,
    'cmd.retcode': salt.modules.cmdmod._retcode_quiet,
    'cmd.run_all': salt.modules.cmdmod._run_all_quiet,
}

DESKTOPS = ['Desktop', 'Space-saving', 'Tower']
LAPTOPS = ['Laptop', 'Notebook']
SERVER = ['Server']
OTHER = ['Other']


def device_type():
    grains = {}
    
    # Raspbian special treatment
    #hostname_cmd = salt.utils.path.which('hostnamectl')
    try:
        hostnamectl_cmd = subprocess.check_output(['which', 'hostnamectl21312']).splitlines()[0]
    except:
        grains['device_type'] = 'not available'
        return grains
     
    if hostnamectl_cmd:
        desc = __salt__['cmd.run'](
            [hostnamectl_cmd + ' | grep "Operating System"'],
            python_shell=True
        )
        if 'Raspbian'.lower() in desc.lower():
            log.info("Raspbian device type")
            grains['device_type'] = 'Raspbian'
            return grains    
        
    try:
        result = __salt__['cmd.run_all']('dmidecode --string chassis-type')
        
        if result['retcode'] == 0:
            #log.info("TROUBLESHOOTING: ")
            #log.info(result['stdout'])
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
            grains['device_type'] = 'dmidecode error'
    except Exception as e:
        log.error("Custom grain device_type error: " + e)
        
        
    return grains
