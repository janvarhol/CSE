import salt.modules.cmdmod
import logging

log = logging.getLogger(__name__)

__salt__ = {
    'cmd.run': salt.modules.cmdmod._run_quiet,
    'cmd.retcode': salt.modules.cmdmod._retcode_quiet,
    'cmd.run_all': salt.modules.cmdmod._run_all_quiet,
}

DESKTOPS = ['Other', 'Desktop', 'Space-saving', 'Tower']
LAPTOPS = ['Laptop', 'Notebook']
SERVER = ['Server']


def device_type():
    grains = {}
    try:
        result = __salt__['cmd.run_all']('dmidecode --string chassis-type')
        
        if result['retcode'] == 0:
            log.info("TROUBLESHOOTING: ")
            log.info(result['stdout'])
         
        
            if result['stdout'] in DESKTOPS:
                grains['device_type'] = 'Desktop'
            elif result['stdout'] in LAPTOPS:
                grains['device_type'] = 'Laptop'
            elif result['stdout'] in SERVER:
                grains['device_type'] = 'Server'
            else:
                grains['device_type'] = 'Unknown'
        else:
            grains['device_type'] = 'ERROR'
    except Exception as e:
        log.error("Custom grain device_type error: " + e)
    return grains
