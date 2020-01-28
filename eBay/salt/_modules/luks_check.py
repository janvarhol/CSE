# -*- coding: utf-8 -*-
'''
Checking for LUKS encryption in all disks
:configuration:
    :depends: none
'''
import logging
import json

#import time

log = logging.getLogger(__name__)


def is_disk_encrypted(block_device, block_devices, TYPE):
    '''
    Run cryptsetup isLuks /dev/<device>
    retcode 0 = Disk Encrypted
    retcode 1 = Disk not encrypted
    '''
    print("--->>> Checking disk encrypted on device: " + block_device)
    log.info("--->>> Checking disk encrypted on device: " + block_device)
    # Check if device name ends with partition number, like /dev/sda5

    # Testing fix for linux_raid_member
    if block_devices[block_device][TYPE] == 'linux_raid_member':
        # assuming it is encrypted
        print("--->>> linux_raid_member device: " + block_device)
        log.info("--->>> linux_raid_member device: " + block_device)

        return 0

    if block_device[-1:].isdigit():
        # BEING EXTRA CAREFUL, REDUNDANT, WIH STR AND UNICODE STRINGS
        # IF THIS FIXES THE ISSUE, LATER POLISH THE CODE
        cryptsetup_bin = __salt__['cmd.which']('cryptsetup')
        cryptsetup_bin = str(cryptsetup_bin)
        log.info("cryptsetup_bin: " + str(cryptsetup_bin))
        log.info(type(cryptsetup_bin))
        if cryptsetup_bin != None and len(cryptsetup_bin) > 9:
            log.info("--->> cryptsetup_bin: " + str(cryptsetup_bin))
            cryptsetup_isLuks_cmd = cryptsetup_bin + ' isLuks ' + str(block_device)
            log.info("Running cryptsetup command: " + cryptsetup_isLuks_cmd)
            cryptsetup_isLuks = __salt__['cmd.retcode'](cryptsetup_isLuks_cmd, ignore_retcode=True)
        else:
            log.warning("cryptsetup binary was not found in path!!!")
            return 1

    elif block_device[-1:].isalpha():
    # if device name ends with alpha, meaning it's a disk, like /dev/sdb
        print("--->>> Scanning disk for LVM information")
        log.info("--->>> Scanning disk for LVM information")
        try:
            lvm_pv_info = __salt__['lvm.pvdisplay'](block_device)
            lvm_vol_group_name = lvm_pv_info[block_device]['Volume Group Name']
            lvm_lv_info = __salt__['lvm.lvdisplay'](lvm_vol_group_name)
            for log_vol_name in lvm_lv_info:
              lvm_log_vol_name = lvm_lv_info[log_vol_name]['Logical Volume Name']
              print("--->>> Scanned Logical Volume Name: " + lvm_log_vol_name)
              log.info("--->>> Scanned Logical Volume Name: " + lvm_log_vol_name)

              # Run crypsetup using LVM Logical Volume Name instead of device name
              # /dev/sdb vs /dev/home/homevol
              cryptsetup_isLuks = __salt__['cmd.retcode']('cryptsetup isLuks ' + lvm_log_vol_name, ignore_retcode=True)
              # if cryptsetup is not 0, return failure, disk not encrypted
              if cryptsetup_isLuks >= 1:
                print("--->>> cryptsetup on scanned Logical Volume Name FAILED: " + lvm_log_vol_name)
                log.warning("--->>> cryptsetup on scanned Logical Volume Name FAILED: " + lvm_log_vol_name)
                return cryptsetup_isLuks
        except:
            # If something goes wrong, return 1 (False / Disk not encrypted, must be fixed)
            return 1
    else:
        print("--->>> Un-handled case, returning Disk not encrypted")
        return 1
#    print(cryptsetup_isLuks)

    return cryptsetup_isLuks


def is_boot_partition(block_device, block_devices):
    '''
    Check if a non encrypted device is the boot partition
    True = the non encrypted device is the boot partition
    False = the non encrypted device IS NOT the boot partition
    '''

    # Read mount points from /etc/fstab
    mount_points = __salt__['mount.fstab']()
    partitions = mount_points.keys()

    # TROUBLESHOOTING INFO
    print("__is_boot_partition_MOUNT_POINTS: " + json.dumps(mount_points, indent=4))
    print("__is_boot_partition_PARTITIONS: " + str(partitions))
    print("__is_boot_partition_BLOCK_DEVICE: " + block_device)
    print("__is_boot_partition_BLOCK_DEVICES: " + json.dumps(block_devices, indent=4))
    # END TROUBLESHOOTING INFO

    IS_BOOT = False
    UUID = 'UUID'

    # TESTING DATA  -- REMOVE THIS
    #block_devices = {"/dev/nvme000021": {
    #    "TYPE": "ext4",
    #    "PTUUID": "49c9eba8-8b77-4a92-a88c-a703736ee0e7",
    #    "PARTUUID": "6fb24b2e-01"}
    #    }
    #block_device = '/dev/nvme000021'
    #print("TESTING DATA:")
    #print("testing_data_BLOCK_DEVICES: " + json.dumps(block_devices, indent=4))
    #print("testing_data__DEVICE: " + block_device)
    #  END TESTING DATA  -- REMOVE THIS

    # Use PTUUID for /dev/nvme* devices
    #if block_device.startswith('/dev/nvme'):
    #    for key in block_devices[block_device].keys():
    #        print("Checking UUID key on block device")
    #        if key == 'PTUUID':
    #            print("UUID CHANGED TO PTUUID FOR DEVICE " + block_device)
    #            UUID = 'PTUUID'


    if "UUID" in block_devices[block_device].keys():
        UUID = 'UUID'
        print("Using UUID")
        block_device_UUID = block_devices[block_device][UUID]
        print("block_device_UUID: " + block_device_UUID)
    elif "PTUUID" in block_devices[block_device].keys():
        UUID = 'PTUUID'
        print("Using PTUUID")
        block_device_UUID = block_devices[block_device][UUID]
        print("block_device_UUID: " + block_device_UUID)
    elif "PARTUUID" in block_devices[block_device].keys():
        UUID = 'PARTUUID'
        print("Using PARTUUID")
        block_device_UUID = block_devices[block_device][UUID]
        print("block_device_UUID: " + block_device_UUID)

    #block_device_UUID = __salt__['disk.blkid'](block_device)[block_device][UUID]
    print("--- BLOCK DEVICE UUID --- : " + block_device_UUID)
    print("")
    print("")

    # /boot partition UUID match check (boot partitions can be not encrypted)
    if '/boot' in partitions:
        print("Checking /boot partition")
        log.info("Checking /boot partition")

        # Get and compare UUIDs from block partition and block device
        block_device_UUID = __salt__['disk.blkid'](block_device)[block_device][UUID]
        boot_UUID = mount_points['/boot']['device'].replace('UUID=', '')
        print("Block device " + block_device + " UUID: " + block_device_UUID)
        log.info("Block device " + block_device + " UUID: " + block_device_UUID)
        print("Boot /boot partition UUID: " + boot_UUID)
        log.info("Boot /boot partition UUID: " + boot_UUID)

        if boot_UUID == block_device_UUID:
            print("UUID MATCH for /boot partition and " + block_device + " device")
            log.info("UUID MATCH for /boot partition and " + block_device + " device")
            #return True
            IS_BOOT = True

    # /boot/efi partition UUID match check (boot partitions can be not encrypted)
    if '/boot/efi' in partitions:
        print("Checking /boot/efi partition")
        log.info("Checking /boot/efi partition")

        # Get and compare UUIDs from block partition and block device
        block_device_UUID = __salt__['disk.blkid'](block_device)[block_device][UUID]
        boot_UUID = mount_points['/boot/efi']['device'].replace('UUID=', '')
        print("Block device " + block_device + " UUID: " + block_device_UUID)
        log.info("Block device " + block_device + " UUID: " + block_device_UUID)
        print("Boot /boot/efi partition UUID: " + boot_UUID)
        log.info("Boot /boot/efi partition UUID: " + boot_UUID)

        if boot_UUID == block_device_UUID:
            print("UUID MATCH for /boot/efi partition and " + block_device + " device")
            log.info("UUID MATCH for /boot/efi partition and " + block_device + " device")
            #return True
            IS_BOOT = True

    if IS_BOOT:
        return True
    else:
        return False


def get_disks_encrypted():
    '''
    Checks all disks are encrypted
    '''
    skip_osfinger_list = ['Raspbian-9', 'Raspbian-10']

    luks_assessment_encrypted = []
    luks_assessment_NOT_encrypted = []
    luks_assessment_skipped = []
    luks_assessment = {}

    if __grains__['osfinger'] not in skip_osfinger_list:
        cryptsetup_bin = __salt__['cmd.which']('cryptsetup')
        if not cryptsetup_bin:
            log.warning("cryptsetup binary not found")
            return False

        # List devices
        block_devices = __salt__['disk.blkid']()
        # Some devices that can be ignored
        skip_block_device_names = ['/dev/loop', '/dev/mapper', '/dev/sr', '/dev/md']
        skip_partition_types = ['gpt', 'ntfs', 'dos']

        # ADRIAN - INFO
        print("BLOCK_DEVICES: " + json.dumps(block_devices, indent=4))

        # Verify if each disk is encrypted
        disks_encrypted = True

        # modified block_devices.iteritems() to block_devices.items()
        for block_device, value in block_devices.items():
            SKIP_DEVICE = False

            # Checking for keys inside block_device
            # could be TYPE, PTTYPE
            print("--------------->>>>>>>> block device: " + str(block_devices[block_device]))
            #time.sleep(1)

            if 'TYPE' in block_devices[block_device].keys():
                TYPE = 'TYPE'
            elif 'PTTYPE' in block_devices[block_device].keys():
                TYPE = 'PTTYPE'
            else:
                TYPE = 'NOT KNOWN'

            if TYPE != 'NOT KNOWN' and block_devices[block_device][TYPE].lower() != 'swap':
                print("Device is not swap, moving forward...")
                print("Device keys: " + str(block_devices[block_device].keys()))

                #IGNORE "vfat" "EFI System Partition"
                if 'PARTLABEL' in block_devices[block_device].keys():
                    print("PARTLABEL found in keys")
                    print("Checking if device is vfat and EFI System Partition")
                    print(block_devices[block_device][TYPE].lower())
                    print(block_devices[block_device]['PARTLABEL'])

                    if block_devices[block_device][TYPE].lower() == 'vfat' and block_devices[block_device]['PARTLABEL'].lower() == "efi system partition":
                        SKIP_DEVICE = True
                        print("")
                        print("")
                        print("")
                        print("++++++----->>>>>>>> IGNORING partition type " + block_devices[block_device][TYPE].lower() + " " + block_devices[block_device]['PARTLABEL'] + " in " + block_device)
                        print("")
                        log.warning("++++++----->>>>>>>> IGNORING partition type " + block_devices[block_device][TYPE].lower() + " " + block_devices[block_device]['PARTLABEL'] + " in " + block_device)
                        luks_assessment_skipped.append(block_device)

                # IGNORE PARTITION TYPES in skip_partition_types
                if block_devices[block_device][TYPE].lower() in skip_partition_types:
                    SKIP_DEVICE = True
                    print("")
                    print("")
                    print("++++++----->>>>>>>> IGNORING partition type " + block_devices[block_device][TYPE].lower() + " in " + block_device)
                    print("")
                    log.warning("IGNORING partition type " + block_devices[block_device][TYPE].lower() + " in " + block_device)
                    luks_assessment_skipped.append(block_device)
                elif not block_device.startswith(tuple(skip_block_device_names)):
                    if not SKIP_DEVICE:
                        print("")
                        print("")
                        print("")
                        print("Device not skipped")
                        print("Checking encryption on device: " + block_device)
                        log.warning("Checking encryption on device: " + block_device)

                        # INFO
                        print("BLOCK DEVICE: " + block_device)

                        if block_devices[block_device][TYPE] == 'crypto_LUKS':
                          print(block_device + " is encrypted")
                          log.warning(block_device + " is encrypted")
                          # Add device to luks_assessment_encrypted
                          luks_assessment_encrypted.append(block_device)
                        elif is_disk_encrypted(block_device, block_devices, TYPE) == 0:
                            print(block_device + " is encrypted")
                            log.warning(block_device + " is encrypted")
                            # Add device to luks_assessment_encrypted
                            luks_assessment_encrypted.append(block_device)
                        else:
                            # NEW - CHECKING BOOT PARTITION
                            if not is_boot_partition(block_device, block_devices):
                                print(block_device + " IS NOT encrypted!!")
                                log.warning(block_device + " IS NOT encrypted!!")
                                disks_encrypted = False
                                # Add device to luks_assessment_NOT_encrypted
                                luks_assessment_NOT_encrypted.append(block_device)
                                #return disks_encrypted
                            else:
                                print("IGNORING boot or similar partition in " + block_device)
                                log.warning("IGNORING boot or similar partition in " + block_device)
            # IGNORE SWAP PARTITIONS
            elif TYPE != 'NOT KNOWN' and block_devices[block_device][TYPE].lower() == 'swap':
                SKIP_DEVICE = True
                print("")
                print("IGNORING swap partition in " + block_device)
                log.warning("IGNORING swap partition in " + block_device)
                luks_assessment_skipped.append(block_device)
            # SKIP NOT KNOWN TYPE PARTITIONS
            elif TYPE == 'NOT KNOWN':
                SKIP_DEVICE = True
                print("")
                print("->->->->->-> SKIPPING NOT KNOWN TYPE PARTITION !!!!: " + block_device)
                log.warning("->->->->->-> SKIPPING NOT KNOWN TYPE PARTITION !!!!: " + block_device)
                luks_assessment_skipped.append(block_device)


        #return disks_encrypted

        print("")
        print("-------- LUKS ENCRYPTION RESULT --------")
        print("ENCRYPTED DEVICES: " + json.dumps(luks_assessment_encrypted, indent=4))
        print("")
        print("DEVICES NOT ENCRYPTED: " + json.dumps(luks_assessment_NOT_encrypted, indent=4))
        print("")
        print("SKIPPED: " + json.dumps(luks_assessment_skipped, indent=4))

        # Create return dictionary
        luks_assessment['encrypted devices'] = luks_assessment_encrypted
        luks_assessment['not encrypted devices'] = luks_assessment_NOT_encrypted


    
        # If there are items in NOT encrypted device, return False
        if len(luks_assessment_NOT_encrypted) > 0:
            grains = {'luks_encrypted_status': False, 'encrypted_devices': luks_assessment_encrypted, 'NOT_encrypted_devices': luks_assessment_NOT_encrypted}
            __salt__['grains.set']('luks_check', grains, force=True)
            luks_assessment['luks_encrypted_status'] = False
            return False, 
        else:
            grains = {'luks_encrypted_status': True, 'encrypted_devices': luks_assessment_encrypted, 'NOT_encrypted_devices': luks_assessment_NOT_encrypted}
            __salt__['grains.set']('luks_check', grains, force=True)
            luks_assessment['luks_encrypted_status'] = True
            return True
    else:
        print("********* SYSTEM IN LIST OF SKIP BY OSFINGER")
        log.warning("********* SYSTEM IN LIST OF SKIP BY OSFINGER")
        return True
