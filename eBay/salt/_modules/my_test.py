import logging
import json
from datetime import datetime, timedelta

log = logging.getLogger(__name__)

def get_keys(self, device=None):
    """
    Returns the decryption keys for this

    :volume: the volume to get the key for. This will be something like
             /dev/sda5 or /dev/mapper/sda5_crypt if using LVM
    :returns: dictionary of slot => key
    """

    if device is not None:
        # format(volume=self.label) #, "]
        # AM: add function to replace label
        # lsblk -o NAME,TYPE,MOUNTPOINT /dev/sda5 | grep crypt --> parse string
        #cmd = 'dmsetup table {self.label} --showkeys'
        cmd = 'dmsetup table sda5_crypt --showkeys'
    else:
        cmd = "dmsetup table --showkeys "

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
