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
    print("__is_boot_partition_PARTITIONS: " + json.dumps(partitions, indent=4))
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
        if not block_device.startswith(tuple(skip_block_device_names)):
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
    return disks_encrypted


def test_data():
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
            "UUID": "9l6Kdr-ecpK-2q45-SRzl-IfUw-Rsfd-qA1EDm",
            "TYPE": "LVM2_member"
        },
        "/dev/mapper/ubuntu--vg-root": {
            "UUID": "e87684aa-5df6-4996-9b20-88010df066b3",
            "TYPE": "ext4"
        },
        "/dev/mapper/ubuntu--vg-swap_1": {
            "UUID": "7f009849-77ad-4581-8a02-6b35be060163",
            "TYPE": "swap"
        },
        "/dev/loop0": {
            "TYPE": "squashfs"
        },
        "/dev/loop1": {
            "TYPE": "squashfs"
        },
        "/dev/loop3": {
            "TYPE": "squashfs"
        },
        "/dev/loop4": {
            "TYPE": "squashfs"
        },
        "/dev/loop5": {
            "TYPE": "squashfs"
        },
        "/dev/loop6": {
            "TYPE": "squashfs"
        },
        "/dev/loop7": {
            "TYPE": "squashfs"
        },
        "/dev/nvme0n1p1": {
            "UUID": "5AE6-7C22",
            "TYPE": "vfat",
            "PARTLABEL": "EFI System Partition",
            "PARTUUID": "a763a766-e560-4345-b342-b4e1698a3a81"
        },
        "/dev/nvme0n1p2": {
            "UUID": "1849d6be-54e2-4832-9d23-472f6606bee0",
            "TYPE": "ext4",
            "PARTUUID": "3e175f69-cb33-4bc0-92a2-231feff6d535"
        },
        "/dev/nvme0n1p3": {
            "UUID": "8d7043e8-9c4e-4425-85eb-fa9b5a7720de",
            "TYPE": "crypto_LUKS",
            "PARTUUID": "082e3714-0cef-4ae7-b468-3ed4b2cca0b8"
        },
        "/dev/loop8": {
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
        "/dev/loop16": {
            "TYPE": "squashfs"
        },
        "/dev/loop18": {
            "TYPE": "squashfs"
        },
        "/dev/loop23": {
            "TYPE": "squashfs"
        },
        "/dev/loop17": {
            "TYPE": "squashfs"
        },
        "/dev/loop15": {
            "TYPE": "squashfs"
        },
        "/dev/loop9": {
            "TYPE": "squashfs"
        },
        "/dev/loop21": {
            "TYPE": "squashfs"
        },
        "/dev/nvme0n1": {
            "PTUUID": "a8b2719c-5a03-465b-bf55-79a66e858dbf",
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
            "device": "UUID=1849d6be-54e2-4832-9d23-472f6606bee0",
            "fstype": "ext4",
            "opts": [
                "defaults"
            ],
            "dump": "0",
            "pass": "2"
        },
        "/boot/efi": {
            "device": "UUID=5AE6-7C22",
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
        if not block_device.startswith(tuple(skip_block_device_names)):
            print("")
            print("")
            print("Checking encryption on device: " + block_device)
            print("BLOCK DEVICE: " + block_device)

            IS_BOOT = False
            UUID = 'UUID'

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

    return True
