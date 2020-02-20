# -*- coding: utf-8 -*-
'''
LUKS Disk encryption module for interacting with LUKS encrypted devices.


:configuration:

:depends: none

'''
from __future__ import absolute_import, print_function, unicode_literals
import binascii
import logging
import six
import tempfile
import uuid

LOG_LEVELS = ['error', 'info', 'debug', 'critical', 'warning']
log = logging.getLogger(__name__)
HDR_BACK_PATH = "/tmp/header_backup_tmp-{}"


def set_grain():
    '''There can be multiple mount points encrypted. This grains module
    iterates through each one and fetches the status, whether it is is
    encrypted and then whether the key stored in pillar can decrypt it.
    '''
    grains = {'luks_encrypted': False, 'mounts': get_mounted_volumes(True)}

    all_encrypted = all((m['on_encrypted'] for m in grains['mounts']))
    grains['luks_encrypted'] = all_encrypted

    __salt__['grains.set']('luks', grains, force=True)
    # __salt__['saltutil.refresh_grains']()
    return __salt__['grains.get']('luks')


# Needed as functions
def on_encrypted(volume):
    """
    Returns whether the volume is on a luks encrypted device.

    This does not tell you which key is used. I simply tells you whether it is
    encrypted.

    :device: the original device /dev/sda5 or /dev/mapper/something--vg-root
    :returns: boolean

    CLI Example:

    .. code-block:: bash

        salt <minion_id> luks.on_encrypted /dev/sda5

        salt <minion_id> luks.on_encrypted /dev/mapper/something--vg-root

    """
    luks_device = LuksDevice(volume)
    return luks_device.on_encrypted()


def check_key(volume, key=None, slot=None):
    """
    Determines whether `volume` is on a device encrypted with `key` in slot
    `slot`

    :volume: the volume to check. e.g. /dev/mapper/hostname--vg-root
    :key: the key
    :slot: slot to verify
    :returns: boolean

    CLI Example:

    .. code-block:: bash

        salt <minion_id> luks.check_key /dev/sda5 "some-secret-key"
        salt <minion_id> luks.check_key /dev/sda5 "some-secret-key" slot=7
        salt <minion_id> luks.check_key /dev/mapper/something--vg-root "some-secret"

    """
    # AM: logging
    device = volume
    log.info('--->>> 1. luks_new.check_key, device: ' + device)
    log.info('--->>> 1b.luks_new.check_key, initiating LuksDevice')
    #luks_device = LuksDevice(volume)
    luks_device = LuksDevice(device)

    log.info('--->>> 1c. check_key calling is_encrypted_with_key: key: %s, slot: %s' % (key, slot))

    # AM: original return
    #return luks_device.is_encrypted_with_key(key, slot)
    #_is_encrypted_with_key = {}
    _is_encrypted_with_key = luks_device.is_encrypted_with_key(key, slot)

    log.info('--->>> 1d. CHECK KEY COMPLETED: returning is_encrypted_with_key_status: ' + str(_is_encrypted_with_key))

    return _is_encrypted_with_key
    #return True


def change_luks_key(volume, key, slot='7'):
    """
    Change the LUKS key phrase in the slot

    :device: the original device /dev/sda5 or /dev/mapper/something--vg-root
    :new_key: the new key to encrypt the drive with
    :slot: which luks slot to put the key into
    :returns: dictionary results of key change

    CLI Example:

    .. code-block:: bash

    """

    luks_device = LuksDevice(volume)
    if not luks_device.on_encrypted():
        return None
    return luks_device.change_luks_key(key, slot)


def get_info(volume=None):
    """
    Get information about the volume given.

    :volume: the original device /dev/sda5 or /dev/mapper/something--vg-root
    :returns: dictionary of information

    CLI Example:

    .. code-block:: bash

        salt <minion_id> luks.get_info /dev/sda5
        salt <minion_id> luks.get_info /dev/sda5
    """
    info = {}
    if volume:
        luks_device = LuksDevice(volume)
        return luks_device.get_info()
    else:
        for volume in get_mounted_volumes():
            luks_device = LuksDevice(volume['device'])
            info[volume['device']] = luks_device.get_info()
    return info


def get_all_debugging():
    # all mounted volumes
    # all keys on volumes
    # all luks grains

    _info = {}
    _info['luks_grain'] = __salt__['grains.get']('luks')
    _info['compliant_grain'] = __salt__['grains.get']('compliant')
    for volume in get_mounted_volumes():
        luks_device = LuksDevice(volume['device'])
        _info[volume['device']] = luks_device.get_info()
        dev = _info[volume['device']]['device']
        _info[volume['device']].update({
                    'open_slots': luks_device.get_open_slot(list_all=True),
                    'keys': luks_device.get_keys_v2(),
                    'on_encrypted': luks_device.on_encrypted(),
                    'is_logical_device': luks_device.is_logical_device,
                    'get_enc_slots': luks_device.get_enc_slots(),
                    'cryptsetup luksDump cmd': 'cryptsetup luksDump {}'.format(dev),
                    'cryptsetup luksDump': __salt__['cmd.run']('cryptsetup luksDump {}'.format(dev))
                })

    return _info


def get_keys(volume):
    """
    Get a list of keys on this volume. This will not return the key string
    itself, but rather meta information about the key (slot, etc)

    :volume: the original device /dev/sda5 or /dev/mapper/something--vg-root
    :returns: list of keys

    CLI Example:

    .. code-block:: bash

        salt <minion_id> luks.get_keys /dev/sda5
        salt <minion_id> luks.get_keys /dev/mapper/something--vg-root
    """
    log.info('--->>> 6. Running get_keys for volume: ' + volume)
    volume = '/dev/sda5'
    log.info('--->>> 6B TROUBLESHOOTING. Running get_keys for volume: ' + volume)
    luks_device = LuksDevice(volume)

    if not luks_device.on_encrypted():
        return None
    return luks_device.get_keys_v2()


def open_slot(volume, **kwargs):
    """
    Get the first open luks slot

    :volume: the device /dev/sda5 or /dev/mapper/something--vg-root
    :returns: integer of first open luks slot

    CLI Example:

    .. code-block:: bash

        salt <minion_id> luks.open_slot /dev/sda5
        salt <minion_id> luks.open_slot /dev/mapper/something--vg-root
    """
    luks_device = LuksDevice(volume)
    if not luks_device.on_encrypted():
        return None
    return luks_device.get_open_slot(list_all=kwargs.get('list_all'))


def get_mounted_volumes(give_status=False):
    """
    Fetch a list of mounted volumes on this machine.

    This will return only those volumes that are interesting as defined in
    pillar values:

    .. code-block:: bash
        linux_encryption_whitelist_volumes:
          - /
          - /home

    The default list consists only of `/` (root).

    :returns: list of volumes

    """
    # Should use

    whitelist = __salt__['pillar.get'](
                                       'linux_encryption_whitelist_volumes',
                                       ['/'])
    volume_list = LuksManager().get_mounted_volumes(whitelist)
    if give_status:
        for v in volume_list:
            v['on_encrypted'] = LuksDevice(v['device']).on_encrypted()


    return volume_list
    # return volumes


def gen_hdr_backup(volume, **kwargs):
    """
    Generate a header backup file for the given encrypted volume.

    :volume: the original device /dev/sda5 or /dev/mapper/something--vg-root
    :returns: string path to the header backup

    CLI Example:

    .. code-block:: bash

    """
    luks_device = LuksDevice(volume)
    if not luks_device.on_encrypted():
        return None
    return luks_device.backup_luks_header()


def get_log_device(volume, **kwargs):
    """
    Get the logical device a volume resides on.

    :volume: the original device /dev/sda5 or /dev/mapper/something--vg-root
    :returns: string path to the logical device

    CLI Example:

    .. code-block:: bash

        salt <minion_id> luks.get_log_device /dev/mapper/something--vg-root "some-secret"
    """
    luks_device = LuksDevice(volume)
    return luks_device.logical_device


def test_key(volume, key):
    """Test key on volume

    :volume: string i.e. device path something like /dev/sda5 or /dev/mapper/something--vg-root
    :key: string key to check
    :returns: boolean

    """
    luks_device = LuksDevice(volume)
    return luks_device.is_encrypted_with_key(key=key)


######################
######################
######################
######################
######################
######################


class LuksManager(object):

    """
    Manage LUKS keys
    """

    def __init__(self):
        """
        Initialize the LUKS manager.
        """
        pass

    def get_mounted_volumes(self, whitelist=[]):
        """
        Return a list of mounted volumes including only those in the
        whitelist.

        :whitelist: list of strings representing mountpoints
        :returns: list of mountpoints

        """
        active_volumes = __salt__['mount.active']()
        # all_volumes = map(
        #         lambda v,i: i['mount_point'] = v,
        #         filter(lambda k, i: k in whitelist, active_volumes.items()))

        volumes = []

        for k, volume in six.iteritems(active_volumes):
            if k in whitelist:
                volume['mount_point'] = k
                # volume['info'] = self.get_info()
                volumes.append(volume)

        return volumes


class LuksDevice(object):

    """
    Represents a LuksDevice found by a volume on the device

    """

    def __init__(self, volume):
        """
        Initialize the LuksDevice manager with a volume. This volume
        must come in the form of a known mounted volume. This will usually look
        something like /dev/sda5 or /dev/mapper/ebay--encrypted--vg-root.

        In the case of /dev/sda5 it is a traditional block devices. The
        /dev/mapper/... version is an LVM volume.

        """
        log.info('--->>> LuksDevice initialization, volume: ' + volume)
        self.volume = volume
        self.volume_label = self.volume.split('/')[-1]

        # AM: I think parents is not needed
        #self.parents = self.device_parents()

        # Get the underlying block device i.e. /dev/sda5, store this in
        # device
        self.logical_device = None

        self.LV = None
        self.LG = None

        # AM: removing functions get_physical_device, repplaced by volume (device from my module)
        #self.device = self.get_physical_device()
        self.device = volume
        log.info('--->>> LuksDevice initialization, device: ' + self.device)
        self.label = self.volume_label

        #if self.is_logical_device:
        #    self.get_logical_info()
            # There are times when there is no logical device but this code
            # things this is a logical device
        #    if self.logical_device:
        #       self.label = self.logical_device.split('/')[-1]

        self.device_label = self.device.split('/')[-1]

        self._master_key_file_bin = None

        self.header_backup_file = _self_dest_temp_file(destroy=False,
                                                       prefix='luks_hdr_bak')

        log.info('--->>> LuksDevice initialization, header_backup_file: ' + str(self.header_backup_file))
        log.info('--->>> LuksDevice initialization, starting header backup')
        self.backup_luks_header()

        log.info('--->>> LuksDevice initialization, generating master keyfile ADRIAN')
        self.generate_master_keyfile_adrian()

    def generate_master_keyfile_adrian(self):
        # HARD CODED VALUES FOR TESTING 
        #tmp_cmd = 'cat {} | {}'.format(keyfile.name, cmd).strip()
        cmd = 'dmsetup table --showkeys sda5_crypt | awk \'{{ print $5 }}\' | xxd -r -p > /tmp/master-key'
        log.info('---> generate_master_keyfile_adrian:' + cmd)
        #ret = __salt__['cmd.run_all'](cmd, python_shell=True)   
        ret = self.cmd(cmd)
        log.info('---> generate_master_keyfile_adrian: ret: ' + str(ret))   


    def backup_luks_header(self):
        """
        Backup the luks header so it can be restored when something fails

        cryptsetup luksHeaderBackup <device> --header-backup-file <file>
        :returns: filepath to header backup

        """
        tmp_header_backup_file = HDR_BACK_PATH.format(uuid.uuid4())
        cmd = ("cryptsetup luksHeaderBackup {self.device} "
               "--header-backup-file {header_backup_file}")
        self.cmd(cmd, header_backup_file=tmp_header_backup_file)

        cmd2 = "cat {header_backup_file} > {self.header_backup_file.name}"
        self.cmd(cmd2, header_backup_file=tmp_header_backup_file)
        __salt__['file.remove'](tmp_header_backup_file)

        return self.header_backup_file.name

    def recover_luks_header(self):
        """
        Recover the luks header from the backup

        cryptsetup luksHeaderRestore <device> --header-backup-file <file>

        :returns: bool
        """
        cmd = ("cryptsetup luksHeaderRestore {self.device} "
               "--header-backup-file {self.header_backup_file.name}")
        _l('recovering luks header from backup %s',
           self.header_backup_file.name)
        return self.cmd(cmd, **kwargs)

    def key_cmd(self, cmd, keyfile, **kwargs):

        tmp_cmd = 'cat {} | {}'.format(keyfile.name, cmd).strip()

        # add stdin to the end of the string if it isn't already there
        if tmp_cmd[-1] != '-':
            tmp_cmd += ' -'

        log.info('---> 2d. key_cmd: tmp_cmd: '+ tmp_cmd)

        return self.cmd(cmd=tmp_cmd, **kwargs)

    # AM: troubleshooting add new key
    def key_cmd_new(self, cmd, keyfile, slot, device, **kwargs):

        #tmp_cmd = 'cat {} | {}'.format(keyfile.name, cmd).strip()
        tmp_cmd = cmd

        # add stdin to thee nd of the string if it isn't already there
        #if tmp_cmd[-1] != '-':
        #    tmp_cmd += ' -'
        #log.info('---> key_cmd_new: device: '+ str(device))
        #tmp_cmd = 'printf "XXXXXXXX8" | cryptsetup luksAddKey /dev/sda5 -S 7 --master-key-file /tmp/master-key -v -'
        log.info('---> 4d. key_cmd_new: tmp_cmd: '+ tmp_cmd)

        return self.cmd(cmd=tmp_cmd, **kwargs)

    def cmd(self, cmd, run_all=True, **kwargs):

        cmd_here = cmd.format(self=self, **kwargs)
        log.info('--->>> running cmd: ' + str(cmd_here))
        if run_all:
            ret_value = __salt__['cmd.run_all'](cmd_here, python_shell=True)
        else:
            ret_value = __salt__['cmd.run'](cmd_here)

        _l('keyfile_cmd: {{ %s }} --- %s', cmd_here, ret_value)

        return ret_value

    def get_info(self):
        info_keys = ['volume', 'volume_label',
                     'device', 'device_label', 'logical_device',
                     'label', 'label', 'is_logical_device']
        info = dict()
        for k in info_keys:
            info[k] = getattr(self, k)
        return info

    @property
    def master_key_file_bin(self):
        # AM: this checking is not needed
        #if not self.on_encrypted():
        #    return None

        if not self._master_key_file_bin:
            log.info('---> MASTER KEY GENERATION: master_key_file_bin function, calling generate_master_keyfile')
            self.generate_master_keyfile()

        log.info('---> MASTER KEY GENERATION: master_key_file_bin function, returning _master_key_file_bin')
        return self._master_key_file_bin

    def generate_master_keyfile(self):
        """
        Generate a master keyfile for the given device.

        :returns: the path to the master keyfile in binary and text format

        """
        key = self.get_keys_v2().get('0')
        log.info('---> MASTER KEY GENERATION: generate_master_keyfile: key:'+ str(key))
        if not key:
            log.info('---> MASTER KEY GENERATION: generate_master_keyfile: not key, returning False')
            return False

        binary_string = binascii.unhexlify(key)

        self._master_key_file_bin = _self_dest_temp_file()
        self._master_key_file_bin.write(binary_string)
        self._master_key_file_bin.flush()
        log.info('---> MASTER KEY GENERATION: generate_master_keyfile FINISHED')

    def on_encrypted(self):

        # cryptsetup executable may not be on the system. This is a 100% sure
        # indicator that the system is not encrypted
        if self.cmd("which cryptsetup")['retcode'] == 1:
            return False

        return self.cmd('cryptsetup isLuks {self.device}')['retcode'] == 0

    @property
    def is_logical_device(self):
        # Start here
        res = self.cmd('lvdisplay -v')
        if 'No volume groups' in res['stderr']:
            return False
        try:
            lv_info = ' '.join(self.cmd('dmsetup ls', run_all=False).split('\n'))
        except:
            return False
        return self.volume_label in lv_info

    def is_encrypted_with_key(self, key=None, slot=None, keyfile=None, device=None):
        """
        Is `device` encrypted with `key` in slot `slot`

        :key: the key
        :slot: slot to verify
        :returns: boolean

        """
        # AM: logging
        log.info('--->>> 2a. is_encrypted_with_key: key: %s slot: %s keyfile: %s device: %s' % (key, slot, str(keyfile), str(self.device)))
        # AM: keyfile is wrong here, keyfile is showing device

        # AM: adding return dictionary, status + changes
        _status = {}


        if not any((key, keyfile)):
            raise Exception('key or keyfile must be provided')

        if slot is not None and str(slot) in self.get_open_slot(list_all=True):
            _l('no key in slot %s', slot)
            return False
            #return False, _status

        slot_arg = ''

        if slot is not None:
            log.info('--->>> using slot argument: ' + str(slot))
            slot_arg = '--key-slot {slot}'.format(slot)
            log.info('--->>> using slot variable: ' + slot_arg)
        # AM: hard coding slot 7
        else:
            slot = 7
            slot_arg = '--key-slot 7'
            log.info('--->>> hard coding slot 7: ' + slot_arg)

        # AM: checking key in all available slots, removing --key-slot argument
        #cmd = ('cryptsetup luksOpen --test-passphrase {self.device} {slot_arg} -v')
        cmd = ('cryptsetup luksOpen --test-passphrase {self.device} -v')

        if not keyfile:
            log.info('--->>> 2b. not keyfile!! calling function _generate_new_key)')
            keyfile = _generate_new_key(key, return_keyfile=True)

        # AM: logging
        log.info('--->>> 2c. is_encrypted_with_key: cmd: %s, slot_arg: %s , keyfile: %s' % (cmd, slot_arg, str(keyfile)))
        log.info('--->>> 2c. calling self.key_cmd')
        # AM: using new function key_cmd_new
        res = self.key_cmd(cmd, slot_arg=slot_arg, keyfile=keyfile)
        #res = self.key_cmd_new(cmd, slot_arg=slot_arg, keyfile=keyfile)
        log.info('--->>> 2e. showing res: ' + str(res))


        if res['retcode'] == 0:
            log.info('--->>> 2f. encryption key exists: retcode: %s, stdout: %s, stderr: %s' % (res['retcode'], res['stdout'],res['stderr']))
            log.info('--->>> 2f. ALL DONE, system is encrypted and key is  available')
            _status['status'] = True
            _status['changes'] = False
            #return True, _status
            return True
        else:
            log.info('--->>> 2f. KEY IS NOT AVAILABLE: retcode: %s, stdout: %s, stderr: %s' % (res['retcode'], res['stdout'],res['stderr']))
            log.info('--->>> 2f. KEY MUST BE ADDED')

            # AM: add new key
            # Using add_luks_key directly
            # Would it be better to use change_luks_key ?
            log.info('--->>> 2g. Running add_luks_key: %s slot %s, device: %s' % (str(keyfile), slot, self.device))
            add_key_status = self.add_luks_key(keyfile, slot, self.device)
            log.info('--->>> 2h. Return add_luks_key: add_key_status: %s' % (add_key_status))
            #_l('key incorrect, or problem setting key')

            # AM: checking return of add_luks_key
            if add_key_status['retcode'] == 0:
                log.info('--->>> 2i. add_luks_key SUCCESSFUL!! returning True, retcode: %s, stdout: %s, stderr: %s' % (add_key_status['retcode'], add_key_status['stdout'], add_key_status['stderr']))
                _status['status'] = True
                _status['changes'] = True
                #return True, _status
                return True
            else:
                log.info('--->>> 2i. add_luks_key FAILED!! returning False, retcode: %s, stdout: %s, stderr: %s' % (add_key_status['retcode'],add_key_status['stdout'], add_key_status['stderr']))
                _status['status'] = False
                _status['changes'] = False
                #return False, _status
                return False

        #    return False
        #return True


    def change_luks_key(self, key, slot='7'):
        """
        Change the LUKS key phrase in the slot

        :new_key: the new key
        :slot: which slot to put the key in
        :returns: dictionary with key change results

        """
        # cryptsetup luksChangeKey /dev/<device> -S 6 (</path/to/keyfile>)
        _l('slots %s', slot, level='info')
        slot_status = self.get_enc_slots().get(str(slot))

        _l('slot %s status: ', slot_status)

        key = _generate_new_key(key, return_keyfile=True)

        used_available_slot = None

        if slot_status == 'ENABLED':
            _l("kkksss - The key slot is used. Do a luksChangeKey or KillSlot")

            used_available_slot = self.get_open_slot()

            _l('slot %s is available for temporary usage')

            tmp_key = _generate_new_key(return_keyfile=True)

            add_key_status = self.add_luks_key(slot=used_available_slot,
                                               keyfile=tmp_key)

            _l('tmp key added in slot %s - %s',
               used_available_slot,
               add_key_status)

            # I need a known key to luksKillSlot a slot

            remove_slot_results = self.kill_key_in_slot(slot, tmp_key)

            _l('used slot %s to luksKillSlot %s - %s',
               used_available_slot,
               slot,
               remove_slot_results)

            if remove_slot_results['retcode'] != 0:
                _l(('could not luksKill the key in slot %s with temp key '
                    'in slot %s, recovering header'),
                    slot,
                    used_available_slot)
                _l('could not do luksKillSlot %s %s %s',
                   slot, remove_slot_results['stdout'],
                   remove_slot_results['stderr'])
                self.recover_luks_header()
                return None

        add_key_status = self.add_luks_key(slot=slot, keyfile=key)

        # We can probably rely on the add_key_status, but this is a
        # confirmation
        res_data = {'comment': add_key_status['stdout']}
        if not add_key_status or not self.is_encrypted_with_key(keyfile=key):
            msg = 'unable to set new key on slot: {}'.format(slot)
            log.error(msg)
            res_data['status'] = False

            self.recover_luks_header()
        else:
            if used_available_slot is not None:
                remove_slot_results = self.kill_key_in_slot(used_available_slot,
                                                            key)
            res_data['status'] = True

        res_data['key'] = {
                'filepath': key.name,
                'key': open(key.name, 'rb').read()
                }
        return res_data




    def get_open_slot(self, list_all=False):
        """
        Get the first available encryption slot.

        :returns: str 0-6

        """
        if self.on_encrypted():

            cmd = 'cryptsetup luksDump {self.device} | grep ": DISABLED"'
            res = self.cmd(cmd)
            slots = []
            for r in res['stdout'].split('\n'):
                slot = r.split()[2][0]  # without the colon
                if not list_all:
                    if slot != '0':
                        return slot
                slots.append(slot)
            if list_all and slots:
                return slots
        return None


    def get_crypt_label(self, device=None):
        #lsblk -o NAME,TYPE /dev/sda5 | awk '$2 == "crypt" {print $1}'
        cmd = 'lsblk -o NAME,TYPE ' + device + ' | awk \'$2 == "crypt" {print $1}\''
        crypt_label = __salt__['cmd.run_all'](cmd, python_shell=True)

        # Removing first two characters from  `-sda5_crypt
        crypt_label = crypt_label['stdout'][2:]
        log.info('--->>> get_crypt_label: ' + crypt_label)

        return crypt_label


    def get_keys_v2(self, device=None):
        """
        Returns the decryption keys for this
        :volume: the volume to get the key for. This will be something like
                 /dev/sda5 or /dev/mapper/sda5_crypt if using LVM
        :returns: dictionary of slot => key
        """
        log.info('--->>> Running get_keys_v2 on device: ' + str(device))
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
        log.info('--->>> dmsetup ran')

        keys = {}

        if data['retcode'] == 0:
            # iterate over keys
            for key in data['stdout'].split('\n'):
                if key:
                    cols = key.strip().split()
                    key, slot = [cols[x] for x in [4, 5]]
                    keys[slot] = key
        return keys

    def add_luks_key(self, keyfile, slot=7, device=None):  # not implemented
        """
        Add a key to the device in a slot

        :returns: boolean
        """
        log.info('--->>> 4. add_luks_key: keyfile: %s, slot: %s , device: %s' % (str(keyfile), slot, device))

        # AM: modifed to hardcoded data to make it work
        #cmd = ("cryptsetup luksAddKey {self.device} -S {slot} "
        #       "--master-key-file {self.master_key_file_bin.name} -v")
        # command should end with '-' to read from stdin, it's added in key_cmd/key_cmd_new functions

        # AM: testing, works OK!
        #cmd = ("printf \"XXXXXXX8\" | cryptsetup luksAddKey " + '/dev/sda5' + " -S 7 "
        #       "--master-key-file " + '/tmp/master-key' + " -v")

        cmd = ("cat %s | cryptsetup luksAddKey %s -S %s --master-key-file %s -v -" % (keyfile.name, device, slot, '/tmp/master-key'))
        log.info('--->>> 4.b add_luks_key cmd: ' + cmd)

        # AM: troubleshooting
        #return self.key_cmd(cmd, slot=slot, keyfile=keyfile)
        log.info('--->>> 4.c calling key_cmd_new')
        return self.key_cmd_new(cmd, keyfile, slot, device)

    def kill_key_in_slot(self, slot, key):
        """
        kill the key on device in slot"""

        cmd = 'cryptsetup luksKillSlot {self.device} {slot} -v'

        return self.key_cmd(cmd, keyfile=key, slot=slot)

    def get_enc_slots(self):
        """
        returns the luks slots used on the device. This takes devices in the
        format of something like sda5


        :returns: dictionary of slots by id

        """
        # the device needs to be in the form of /dev/sda5, lvm or not
        # cryptsetup luksDump /dev/<device> | grep BLED
        cmd = ('cryptsetup luksDump {device} | grep BLED | awk '
               '"{{{{print \$3, \$4}}}}"').format(device=self.device)

        res = self.cmd(cmd)
        slots = {}
        slot_list = res['stdout'].strip().split('\n')
        log.debug('luks:get_enc_slots slot_list %s', slot_list)
        for slot in filter(lambda s: s, slot_list):
            cols = slot.split(': ')
            slots[cols[0]] = cols[1]

        return slots

    def device_parents(self):
        """
        Determine the physical drive for a logical device

        :returns: string representing the logical device path
        """

        # TODO look at using pyudev for finding the device parent
        cmd = "lsblk -o name  --paths {self.volume} -sln"
        # cmd = "lsblk -o name  {self.volume}"
        lsblk_output = self.cmd(cmd, run_all=False)

        parents = []
        for line in map(lambda l: l.strip(), lsblk_output.split('\n')):
            line_parts = line.split()
            if line_parts:
                key = line_parts[0]
                parents.append(key)

        log.debug('parents %s', parents)
        return parents

    def get_physical_device(self):
        """
        Get the physical device this volume is on. This will be something
        like /dev/sda5
        :returns: string i.e.  /dev/sda5

        """
        log.debug('luks:get_physical_device parents %s', self.parents)
        return self.parents[-2]

    def get_logical_info(self):
        # cmd_tpl = ("lvs -o +devices {self.volume} --noheadings " \
        #            "| awk '{{print $1,$2,$5}}' | sed 's/(.*//'")
        cmd_tpl = ("lvs -o +devices {self.volume} --noheadings ")
        res = self.cmd(cmd_tpl, run_all=True)
        res_out = res['stdout'].split()

        #self.LV, self.LG, logical_device = res_out.split()
        try:
            self.LV = res_out[1]
            self.LG = res_out[2]
            log.debug('luks:get_logical_info res_out: %s', res_out)
            self.logical_device = res_out[-1].split('(')[0]
        except:
            # Some machinees are hard-failing because of a variety of reasons.
            # This is likely due to raid mounts, but further testing must be
            # done to resolve it
            log.error('this machine is failing hard when doing a lvs logical info lookup ')


def generate_key():
    """
    Generate a random key. This currently uses the uuid module to generate a
    key that looks something like

        ee2953ac-f696-478f-83bd-7ba71715ba68

    :returns: string key

    """
    return str(uuid.uuid4())


def _generate_new_key(key=None, destroy=False, return_keyfile=False):
    """
    Generate a new key randomly.

    :returns: str the key text

    """
    if not key:
        # AM: logging
        log.info('--->>> 3a. _generate_new_key: key: ' + key)
        key = generate_key()
        log.info('--->>> 3a. _generate_new_key: key: ' + key)
        log.info('--->>> 3a. _generate_new_key: key type: ' + str(type(key)))

    # AM: forcing key to be string
    key = str(key)

    if return_keyfile:
        key_file = _self_dest_temp_file()
        log.info('--->>> 3b. _generate_new_key: key: %s, key_file: %s' % (key, key_file))
        log.info('--->>> 3b. _generate_new_key: key type: ' + str(type(key)))
        key_file.write(key.encode('utf-8'))
        key_file.flush()

        log.info('--->>> 3c.1. _generate_new_key: returning keyfile ' +str(key_file))
        return key_file
    else:
        log.info('--->>> 3c.2. _generate_new_key: returning key' +str(key))
        return key


def _self_dest_temp_file(prefix="tmp", destroy=False):
    """
    Generate temporary files that are deleted on close.

    See https://docs.python.org/2/library/tempfile.html

    :prefix: str prefix to add to the beginning of each file
    :destroy: boolean whether the file should self-destruct, defaults to False
    :returns: file-like object

    """
    if destroy:
        return tempfile.NamedTemporaryFile(dir='/tmp/', prefix=prefix)
    else:
        return open(__salt__['temp.file'](prefix=prefix), 'wb+')


def _e(string, *args):
    """
    Error Logging

    :code:

    :string: str logging string, with regular logging placeholders
    :*args: args
    :returns: None

    """
    _l(string, *args)


def _l(string, *args, **kwargs):
    """
    Logging, default level is debug

    :string: log string
    :args: log parameters
    :returns: None

    """
    level = kwargs.get('level', 'debug')
    tpl = 'luks:: {}: {}'.format(__name__, string)
    if level not in LOG_LEVELS:
        log.error('invalid log level given %s', level)

        # Defaulting to debug
        level = 'debug'

    getattr(log, level)(tpl, *args)
