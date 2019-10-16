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
        "/dev/mapper/sda3_crypt": {
            "UUID": "iqx2uU-zvtb-thBP-Cj5W-cm7f-TYuY-gzC4PA",
            "TYPE": "LVM2_member"
        },
        "/dev/mapper/ubuntu--vg-root": {
            "UUID": "9f2aa3e3-5cf2-43bc-8ec4-449b48d669bf",
            "TYPE": "ext4"
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
        "/dev/loop5": {
            "TYPE": "squashfs"
        },
        "/dev/loop6": {
            "TYPE": "squashfs"
        },
        "/dev/loop7": {
            "TYPE": "squashfs"
        },
        "/dev/sda1": {
            "UUID": "35A5-46F3",
            "TYPE": "vfat",
            "PARTLABEL": "EFI System Partition",
            "PARTUUID": "6361cd04-bca4-4b90-b52d-edf96e032233"
        },
        "/dev/sda2": {
            "UUID": "17db5c7a-f330-4a1d-85a6-b658bdf2a9fc",
            "TYPE": "ext4",
            "PARTUUID": "f50f1bff-4e4d-44dd-b037-f55cf340e1f8"
        },
        "/dev/sda3": {
            "UUID": "829793e4-70d6-4577-864c-352e6461f40b",
            "TYPE": "crypto_LUKS",
            "PARTUUID": "662e6850-17a7-4d07-87dc-85f31d2995d6"
        },
        "/dev/sdb1": {
            "LABEL": "Windows RE Tools",
            "UUID": "1EA62A93A62A6B89",
            "TYPE": "ntfs",
            "PARTLABEL": "Basic data partition",
            "PARTUUID": "ced5ee38-10a3-4007-81b6-d8dc4fd1f2eb"
        },
        "/dev/sdb2": {
            "UUID": "FE2D-3BAD",
            "TYPE": "vfat",
            "PARTLABEL": "EFI system partition",
            "PARTUUID": "ad74bfd0-aa74-40ef-8c15-b943b444cc3e"
        },
        "/dev/sdc1": {
            "LABEL": "SSD",
            "UUID": "C89C3E479C3E2FF4",
            "TYPE": "ntfs",
            "PARTUUID": "149fdb39-01"
        },
        "/dev/sdc5": {
            "UUID": "6b86f871-bcb4-4f27-a663-c2b1ab6936f8",
            "TYPE": "ext4",
            "PARTUUID": "149fdb39-05"
        },
        "/dev/sdc6": {
            "UUID": "1aa62b05-80ae-4021-b63b-f50486d6d5e1",
            "TYPE": "swap",
            "PARTUUID": "149fdb39-06"
        },
        "/dev/mapper/ubuntu--vg-swap_1": {
            "UUID": "50f8d4e4-fc97-4333-8baa-18a4a7e75429",
            "TYPE": "swap"
        },
        "/dev/loop8": {
            "TYPE": "squashfs"
        },
        "/dev/loop9": {
            "TYPE": "squashfs"
        },
        "/dev/loop11": {
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
        "/dev/loop20": {
            "TYPE": "squashfs"
        },
        "/dev/loop21": {
            "TYPE": "squashfs"
        },
        "/dev/loop22": {
            "TYPE": "squashfs"
        },
        "/dev/loop24": {
            "TYPE": "squashfs"
        },
        "/dev/loop25": {
            "TYPE": "squashfs"
        },
        "/dev/loop26": {
            "TYPE": "squashfs"
        },
        "/dev/loop10": {
            "TYPE": "squashfs"
        },
        "/dev/loop0": {
            "TYPE": "squashfs"
        },
        "/dev/loop19": {
            "TYPE": "squashfs"
        },
        "/dev/sdb3": {
            "PARTLABEL": "Microsoft reserved partition",
            "PARTUUID": "f7522d02-5960-4a24-a870-fb73baa4112c"
        },
        "/dev/sdb4": {
            "PARTLABEL": "Basic data partition",
            "PARTUUID": "966c356c-43cb-497e-ae85-aa205302f506"
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
            "device": "UUID=17db5c7a-f330-4a1d-85a6-b658bdf2a9fc",
            "fstype": "ext4",
            "opts": [
                "defaults"
            ],
            "dump": "0",
            "pass": "2"
        },
        "/boot/efi": {
            "device": "UUID=35A5-46F3",
            "fstype": "vfat",
            "opts": [
                "umask=0077"
            ],
            "dump": "0",
            "pass": "1"
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
