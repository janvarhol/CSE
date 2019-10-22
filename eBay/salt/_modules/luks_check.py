# -*- coding: utf-8 -*-
'''
Checking for LUKS encryption in all disks
:configuration:
    :depends: none
'''
import logging
import json
log = logging.getLogger(__name__)


def is_disk_encrypted(device):
    '''
    Run cryptsetup isLuks /dev/<device>
    retcode 0 = Disk Encrypted
    retcode 1 = Disk not encrypted
    '''
    cryptsetup_isLuks = __salt__['cmd.retcode']('cryptsetup isLuks ' + device, ignore_retcode=True)
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
    skip_osfinger_list = ['Raspbian-9']

    if __grains__['osfinger'] not in skip_osfinger_list:
        cryptsetup_bin = __salt__['cmd.which']('cryptsetup')
        if not cryptsetup_bin:
            log.warning("cryptsetup binary not found")
            return False

        # List devices
        block_devices = __salt__['disk.blkid']()
        # Some devices that can be ignored
        skip_block_device_names = ['/dev/loop', '/dev/mapper', '/dev/sr0']

        # ADRIAN - INFO
        print("BLOCK_DEVICES: " + json.dumps(block_devices, indent=4))

        # Verify if each disk is encrypted
        disks_encrypted = True

        # modified block_devices.iteritems() to block_devices.items()
        for block_device, value in block_devices.items():
        
            # Checking for keys inside block_device
            # could be TYPE, PTTYPE
            print("--------------->>>>>>>> block device: " + str(block_devices[block_device]))
            if 'TYPE' in block_devices[block_device].keys():
                TYPE = 'TYPE'
            elif 'PTTYPE' in block_devices[block_device].keys():
                TYPE = 'PTTYPE'
            else:
                TYPE = 'NOT KNOWN'

            if TYPE != 'NOT KNOWN' and block_devices[block_device][TYPE].lower() != 'swap':
                # IGNORE GPT PARTITIONS
                if block_devices[block_device][TYPE].lower() == 'gpt':
                    print("IGNORING gpt partition " + block_device)
                    log.warning("IGNORING gpt partition " + block_device)
                elif not block_device.startswith(tuple(skip_block_device_names)):
                    print("")
                    print("")
                    print("")
                    print("Checking encryption on device: " + block_device)
                    log.warning("Checking encryption on device: " + block_device)

                    # INFO
                    print("BLOCK DEVICE: " + block_device)

                    if is_disk_encrypted(block_device) == 0:
                        print(block_device + " is encrypted")
                        log.warning(block_device + " is encrypted")
                    else:
                        # NEW - CHECKING BOOT PARTITION
                        if not is_boot_partition(block_device, block_devices):
                            print(block_device + " IS NOT encrypted!!")
                            log.warning(block_device + " IS NOT encrypted!!")
                            disks_encrypted = False
                            return disks_encrypted
                        else:
                            print("IGNORING boot or similar partition in " + block_device)
                            log.warning("IGNORING boot or similar partition in " + block_device)
            # IGNORE SWAP PARTITIONS
            elif TYPE != 'NOT KNOWN' and block_devices[block_device][TYPE].lower() == 'swap':
                print("IGNORING swap partition in " + block_device)
                log.warning("IGNORING swap partition in " + block_device)
            # SKIP NOT KNOWN TYPE PARTITIONS 
            elif TYPE == 'NOT KNOWN':
                print("->->->->->-> SKIPPING NOT KNOWN TYPE PARTITION !!!!" + block_device)
                log.warning("->->->->->-> SKIPPING NOT KNOWN TYPE PARTITION !!!!" + block_device)


        return disks_encrypted
    else:
        print("********* SYSTEM IN LIST OF SKIP BY OSFINGER")
        log.warning("********* SYSTEM IN LIST OF SKIP BY OSFINGER")
        return True

def test_data():
    skip_osfinger_list = ['Raspbian-9']

    if __grains__['osfinger'] not in skip_osfinger_list:
        # List devices
        block_devices = __salt__['disk.blkid']()
        # Some devices that can be ignored
        skip_block_device_names = ['/dev/loop', '/dev/mapper', '/dev/sr0']


        # Read mount points from /etc/fstab
        mount_points = __salt__['mount.fstab']()
        partitions = mount_points.keys()

        # ADRIAN - INFO
        print("BLOCK_DEVICES: " + json.dumps(block_devices, indent=4))

        # TESTING DATA
        print("TESTING DATA ---- TEST BLOCK_DEVICES")
        block_devices = {
            "/dev/mapper/nvme0n1p3_crypt": {
                "UUID": "LgztHh-i26I-tnPy-9GN3-Wxsm-CkPx-fXNewJ",
                "TYPE": "LVM2_member"
            },
            "/dev/mapper/ubuntu--vg-root": {
                "UUID": "a1a7733b-8751-4df3-b572-e33809afe4a8",
                "TYPE": "ext4"
            },
            "/dev/mapper/ubuntu--vg-swap_1": {
                "UUID": "ce9882ec-6db3-44a1-94a6-5a1e57cde1de",
                "TYPE": "swap"
            },
            "/dev/loop0": {
                "TYPE": "squashfs"
            },
            "/dev/loop1": {
                "TYPE": "squashfs"
            },
            "/dev/loop2": {
                "TYPE": "squashfs"
            },
            "/dev/loop3": {
                "TYPE": "squashfs"
            },
            "/dev/loop4": {
                "TYPE": "squashfs"
            },
            "/dev/loop6": {
                "TYPE": "squashfs"
            },
            "/dev/loop7": {
                "TYPE": "squashfs"
            },
            "/dev/nvme0n1p1": {
                "UUID": "8ADA-A427",
                "TYPE": "vfat",
                "PARTLABEL": "EFI System Partition",
                "PARTUUID": "50dd1d2e-dc5b-4927-9487-969d639be4e6"
            },
            "/dev/nvme0n1p2": {
                "UUID": "2a21e580-3165-4774-bd89-677bc10677e6",
                "TYPE": "ext4",
                "PARTUUID": "73d128d1-cb17-468e-aaf4-b8f910f2c5dc"
            },
            "/dev/nvme0n1p3": {
                "UUID": "bba6f4f0-10c8-4064-8429-e5fa611e8532",
                "TYPE": "crypto_LUKS",
                "PARTUUID": "fa10044d-142d-473c-a4b3-d75b51cb663d"
            },
            "/dev/loop8": {
                "TYPE": "squashfs"
            },
            "/dev/loop9": {
                "TYPE": "squashfs"
            },
            "/dev/loop10": {
                "TYPE": "squashfs"
            },
            "/dev/loop11": {
                "TYPE": "squashfs"
            },
            "/dev/loop12": {
                "TYPE": "squashfs"
            },
            "/dev/loop13": {
                "TYPE": "squashfs"
            },
            "/dev/loop14": {
                "TYPE": "squashfs"
            },
            "/dev/loop15": {
                "TYPE": "squashfs"
            },
            "/dev/loop16": {
                "TYPE": "squashfs"
            },
            "/dev/loop17": {
                "TYPE": "squashfs"
            },
            "/dev/loop18": {
                "TYPE": "squashfs"
            },
            "/dev/nvme0n1": {
                "PTUUID": "feb7954a-46d4-4a6d-9a1b-3ce16801ef11",
                "PTTYPE": "gpt"
            }
        }

        mount_points = {
            "/": {
                "device": "/dev/mapper/ubuntu--vg-root",
                "fstype": "ext4",
                "opts": [
                    "errors=remount-ro"
                ],
                "dump": "0",
                "pass": "1"
            },
            "/boot": {
                "device": "UUID=2a21e580-3165-4774-bd89-677bc10677e6",
                "fstype": "ext4",
                "opts": [
                    "defaults"
                ],
                "dump": "0",
                "pass": "2"
            },
            "/boot/efi": {
                "device": "UUID=8ADA-A427",
                "fstype": "vfat",
                "opts": [
                    "umask=0077"
                ],
                "dump": "0",
                "pass": "1"
            },
            "none": {
                "device": "/dev/mapper/ubuntu--vg-swap_1",
                "fstype": "swap",
                "opts": [
                    "sw"
                ],
                "dump": "0",
                "pass": "0"
            }
        }
        
        partitions = mount_points.keys()
        # END TESTING DATA

        # TROUBLESHOOTING INFO
        print("TROUBLESHOOTING INFO_MOUNT_POINTS: " + json.dumps(mount_points, indent=4))
        print("TROUBLESHOOTING INFO_PARTITIONS: " + json.dumps(partitions, indent=4))
        print("TROUBLESHOOTING INFO_BLOCK_DEVICES: " + json.dumps(block_devices, indent=4))
        # END TROUBLESHOOTING INFO

        for block_device, value in block_devices.iteritems():
            print("TROUBLESHOOTING INFO_BLOCK_DEVICE: " + block_device)

            # Checking for keys inside block_device
            # could be TYPE, PTTYPE
            print("--------------->>>>>>>> block device: " + str(block_devices[block_device]))

            if 'TYPE' in block_devices[block_device].keys():
                TYPE = 'TYPE'
            elif 'PTTYPE' in block_devices[block_device].keys():
                TYPE = 'PTTYPE'
            else:
                TYPE = 'NOT KNOWN'

            if TYPE != 'NOT KNOWN' and block_devices[block_device][TYPE].lower() != 'swap':
                # IGNORE GPT PARTITIONS
                if block_devices[block_device][TYPE].lower() == 'gpt':
                    print("IGNORING gpt partition " + block_device)
                    log.warning("IGNORING gpt partition " + block_device)
                elif not block_device.startswith(tuple(skip_block_device_names)):
                    print("")
                    print("")
                    print("Checking encryption on device: " + block_device)
                    print("BLOCK DEVICE: " + block_device)

                    IS_BOOT = False
                    UUID = 'UUID'

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
                        try:
                            #block_device_UUID = __salt__['disk.blkid'](block_device)[block_device][UUID]
                            block_device_UUID = block_devices[block_device][UUID]
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
                        except:
                            print("EXCEPTION for /boot - NOT RUNNING CHECK ON TEST DATA")

                    # /boot/efi partition UUID match check
                    if '/boot/efi' in partitions:
                        print("Checking /boot/efi partition")
                        log.info("Checking /boot/efi partition")

                        # Get and compare UUIDs from block partition and block device
                        try:
                            #block_device_UUID = __salt__['disk.blkid'](block_device)[block_device][UUID]
                            block_device_UUID = block_devices[block_device][UUID]
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
                        except:
                            print("EXCEPTION for /boot/efi - NOT RUNNING CHECK ON TEST DATA")

                    #if IS_BOOT:
                    #    return True
                    #else:
                    #    return False
            elif TYPE != 'NOT KNOWN' and block_devices[block_device][TYPE].lower() == 'swap':
                print("IGNORING swap partition in " + block_device)
                log.warning("IGNORING swap partition in " + block_device)
            elif TYPE == 'NOT KNOWN':
                print("->->->->->-> SKIPPING NOT KNOWN TYPE PARTITION !!!!" + block_device)
                log.warning("->->->->->-> SKIPPING NOT KNOWN TYPE PARTITION !!!!" + block_device)

        return True
    else:
        print("********* SYSTEM IN LIST OF SKIP BY OSFINGER")
        log.warning("********* SYSTEM IN LIST OF SKIP BY OSFINGER")
        return True
