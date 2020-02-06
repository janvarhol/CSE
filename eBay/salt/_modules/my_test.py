import logging
import json

log = logging.getLogger(__name__)

def get_crypt_label(device):
    #lsblk -o NAME,TYPE /dev/sda5 | awk '$2 == "crypt" {print $1}'
    cmd = 'lsblk -o NAME,TYPE ' + device + ' | awk \'$2 == "crypt" {print $1}\''
    crypt_label = __salt__['cmd.run_all'](cmd, python_shell=True)

    # Removing first two characters from  `-sda5_crypt
    crypt_label = crypt_label['stdout'][2:]
    log.info('--->>> get_crypt_label: ' + crypt_label)

    return crypt_label

def get_keys_v2(device=None):
    """
    Returns the decryption keys for this

    :volume: the volume to get the key for. This will be something like
             /dev/sda5 or /dev/mapper/sda5_crypt if using LVM
    :returns: dictionary of slot => key
    """

    if device is not None:
        # AM: get crypt label
        device_crypt_label = get_crypt_label(device)
        # format(volume=self.label) #, "]
        # AM: add function to replace label
        # lsblk -o NAME,TYPE,MOUNTPOINT /dev/sda5 | grep crypt --> parse string
        # it has to be like:

        #cmd = 'dmsetup table {self.label} --showkeys'
        cmd = 'dmsetup table ' + device_crypt_label + ' --showkeys'
    else:
        cmd = "dmsetup table --showkeys "

    log.info('--->>> running cmd: ' + cmd)
    data = __salt__['cmd.run_all'](cmd, python_shell=True)

    keys = {}

    if data['retcode'] == 0:
        # iterate over keys
        for key in data['stdout'].split('\n'):
            if key:
                cols = key.strip().split()
                key, slot = [cols[x] for x in [4, 5]]
                keys[slot] = key
    return keys
