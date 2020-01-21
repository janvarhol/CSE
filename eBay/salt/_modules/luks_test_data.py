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
    '''

    # IMPORTANT: REPLACE device by block_device !!!

    print("--->>> Checking disk encrypted on device: " + device)
    log.info("--->>> Checking disk encrypted on device: " + device)
    # Check if device name ends with partition number, like /dev/sda5
    if device[-1:].isdigit():
        # BEING EXTRA CAREFUL, REDUNDANT, WIH STR AND UNICODE STRINGS
        # IF THIS FIXES THE ISSUE, LATER POLISH THE CODE
        cryptsetup_bin = __salt__['cmd.which']('cryptsetup')
        cryptsetup_bin = str(cryptsetup_bin)
        log.info("cryptsetup_bin: " + str(cryptsetup_bin))
        log.info(type(cryptsetup_bin))
        if cryptsetup_bin != None and len(cryptsetup_bin) > 9:
            log.info("--->> cryptsetup_bin: " + str(cryptsetup_bin))
            cryptsetup_isLuks_cmd = cryptsetup_bin + ' isLuks ' + str(device)
            log.info("Running cryptsetup command: " + cryptsetup_isLuks_cmd)
            cryptsetup_isLuks = __salt__['cmd.retcode'](cryptsetup_isLuks_cmd, ignore_retcode=True)
        else:
            log.warning("cryptsetup binary was not found in path!!!")
            return 1

    elif device[-1:].isalpha():
    # if device name ends with alpha, meaning it's a disk, like /dev/sdb
        print("--->>> Scanning disk for LVM information")
        log.info("--->>> Scanning disk for LVM information")
        try:
            lvm_pv_info = __salt__['lvm.pvdisplay'](device)
            lvm_vol_group_name = lvm_pv_info[device]['Volume Group Name']
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
    '''

    # Testing fix for linux_raid_member
    if block_devices[block_device][TYPE] == 'linux_raid_member':
        # assuming it is encrypted
        print("--->>> linux_raid_member device: " + block_device)
        log.info("--->>> linux_raid_member device: " + block_device)

        return 0

    return 1

def is_boot_partition(block_device, block_devices, mount_points, partitions):
    '''
    Check if a non encrypted device is the boot partition
    True = the non encrypted device is the boot partition
    False = the non encrypted device IS NOT the boot partition
    '''

    # Read mount points from /etc/fstab
    # mount_points = __salt__['mount.fstab']()
    # partitions = mount_points.keys()
    # Note: in testing function mount_points and partition
    # are passed from main

    # TROUBLESHOOTING INFO
    #print("__is_boot_partition_MOUNT_POINTS: " + json.dumps(mount_points, indent=4))
    #print("__is_boot_partition_PARTITIONS: " + str(partitions))
    #print("__is_boot_partition_BLOCK_DEVICE: " + block_device)
    #print("__is_boot_partition_BLOCK_DEVICES: " + json.dumps(block_devices, indent=4))
    # END TROUBLESHOOTING INFO

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
        #--block_device_UUID = __salt__['disk.blkid'](block_device)[block_device][UUID]
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

    # /boot/efi partition UUID match check (boot partitions can be not encrypted)
    if '/boot/efi' in partitions:
        print("Checking /boot/efi partition")
        log.info("Checking /boot/efi partition")

        # Get and compare UUIDs from block partition and block device
        #--block_device_UUID = __salt__['disk.blkid'](block_device)[block_device][UUID]
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

    if IS_BOOT:
        return True
    else:
        return False


def test_data():
    skip_osfinger_list = ['Raspbian-9', 'Raspbian-10']
    #--skip_partition_types = ['gpt', 'ntfs', 'dos']

    luks_assessment_encrypted = []
    luks_assessment_NOT_encrypted = []

    if __grains__['osfinger'] not in skip_osfinger_list:
        # List devices
        block_devices = __salt__['disk.blkid']()
        # Some devices that can be ignored
        skip_block_device_names = ['/dev/loop', '/dev/mapper', '/dev/sr0', '/dev/md']
        skip_partition_types = ['gpt', 'ntfs', 'dos']

        # Read mount points from /etc/fstab
        #--mount_points = __salt__['mount.fstab']()
        #--partitions = mount_points.keys()

        # ADRIAN - INFO
        #--print("BLOCK_DEVICES: " + json.dumps(block_devices, indent=4))

        # TESTING DATA
        print("TESTING DATA ---- TEST BLOCK_DEVICES")
        block_devices =  {
        "/dev/mapper/encsharedev": {
            "TYPE": "ext4",
            "UUID": "decbfbd0-9944-442b-a181-d694f97bb775"
        },
        "/dev/sde1": {
            "UUID_SUB": "00e8834b-4a82-1882-a19c-54696eaef06a",
            "TYPE": "linux_raid_member",
            "UUID": "ea373f54-b3eb-8233-5e79-c747a10008b9",
            "PARTUUID": "c436f82b-09e7-834a-b2df-79b5301c087a",
            "LABEL": "marco-server:0"
        },
        "/dev/sdb1": {
            "UUID_SUB": "9afd71ca-080a-fc41-31ea-e0b46ebc6f93",
            "TYPE": "linux_raid_member",
            "UUID": "ea373f54-b3eb-8233-5e79-c747a10008b9",
            "PARTUUID": "4600c73f-bcdf-ec46-abb6-b362c4d97013",
            "LABEL": "marco-server:0"
        },
        "/dev/loop0": {
            "TYPE": "squashfs"
        },
        "/dev/loop3": {
            "TYPE": "squashfs"
        },
        "/dev/sdc1": {
            "TYPE": "swap",
            "UUID": "c647ea3a-9696-470e-a452-bfea5e9a61cf",
            "PARTUUID": "b360dd74-0223-4737-91be-24e430f70a97"
        },
        "/dev/mapper/encdatadev": {
            "TYPE": "ext4",
            "UUID": "1724982e-0d65-46ab-ba82-b1bbf5c10175"
        },
        "/dev/loop2": {
            "TYPE": "squashfs"
        },
        "/dev/sdd3": {
            "TYPE": "crypto_LUKS",
            "UUID": "b107b832-3842-4b76-9002-b77b34b7f5f1",
            "PARTUUID": "a8594341-d6d2-4076-8f8a-5ef19ecb4064"
        },
        "/dev/sdd2": {
            "TYPE": "ext4",
            "UUID": "baeda7fe-535c-4153-b438-986b2e150743",
            "PARTUUID": "585a1df1-ee90-49c0-8a2d-6e5395488ed3"
        },
        "/dev/sdd1": {
            "TYPE": "vfat",
            "UUID": "6DA1-1CE0",
            "PARTUUID": "1cbc6691-1c46-4ebb-a947-b2057f3449f3"
        },
        "/dev/sdc2": {
            "TYPE": "crypto_LUKS",
            "UUID": "fa90abde-0028-423e-9ec1-bdd1eb07c328",
            "PARTUUID": "87545be6-98ec-40e5-b1b3-b7b5781664e8"
        },
        "/dev/mapper/ubuntu--vg-lv--0": {
            "TYPE": "ext4",
            "UUID": "44003342-49b1-469e-8d4e-fcd064584644"
        },
        "/dev/mapper/rawlargevg-rawdatalv": {
            "TYPE": "crypto_LUKS",
            "UUID": "2f221e57-8dbf-4947-b5d0-f838e1b67c76"
        },
        "/dev/md0": {
            "TYPE": "LVM2_member",
            "UUID": "DuQzfS-fCu2-H0FZ-Sdt4-oVth-YLgF-25Q3En"
        },
        "/dev/loop1": {
            "TYPE": "squashfs"
        },
        "/dev/mapper/dm_crypt-0": {
            "TYPE": "LVM2_member",
            "UUID": "kx6qTc-egzq-iJHg-f8QZ-OHXS-1Ysc-xJMSdi"
        },
        "/dev/sda1": {
            "UUID_SUB": "59cef624-36f1-8ef1-8cca-cbeefef259ab",
            "TYPE": "linux_raid_member",
            "UUID": "ea373f54-b3eb-8233-5e79-c747a10008b9",
            "PARTUUID": "26ed1305-f3c6-4346-89bd-a055ff1b6d61",
            "LABEL": "marco-server:0"
        },
        "/dev/mapper/rawlargevg-rawsharelv": {
            "TYPE": "crypto_LUKS",
            "UUID": "63911a11-be3a-4db3-abd3-978acea768fc"
        },
        "/dev/mapper/homefs": {
            "TYPE": "LVM2_member",
            "UUID": "gmErcT-lAFn-2Ved-ynoO-kk3m-EfRN-t1Wd3O"
        }
        }

        mount_points = {
        "none": {
            "device": "UUID=c647ea3a-9696-470e-a452-bfea5e9a61cf",
            "pass": "0",
            "dump": "0",
            "opts": [
                "sw"
            ],
            "fstype": "swap"
        },
        "/boot": {
            "device": "UUID=baeda7fe-535c-4153-b438-986b2e150743",
            "pass": "0",
            "dump": "0",
            "opts": [
                "defaults"
            ],
            "fstype": "ext4"
        },
        "/": {
            "device": "UUID=44003342-49b1-469e-8d4e-fcd064584644",
            "pass": "0",
            "dump": "0",
            "opts": [
                "defaults"
            ],
            "fstype": "ext4"
        },
        "/boot/efi": {
            "device": "UUID=6DA1-1CE0",
            "pass": "0",
            "dump": "0",
            "opts": [
                "defaults"
            ],
            "fstype": "vfat"
        }
        }

        partitions = mount_points.keys()
        # END TESTING DATA

        # TROUBLESHOOTING INFO
        print("TROUBLESHOOTING INFO_MOUNT_POINTS: " + json.dumps(mount_points, indent=4))
        print("TROUBLESHOOTING INFO_PARTITIONS: " + str(partitions))
        print("TROUBLESHOOTING INFO_BLOCK_DEVICES: " + json.dumps(block_devices, indent=4))
        # END TROUBLESHOOTING INFO



        for block_device, value in block_devices.items():
            SKIP_DEVICE = False
            #--print("TROUBLESHOOTING INFO_BLOCK_DEVICE: " + block_device)
            print("--------------->>>>>>>> block device: " + str(block_devices[block_device]))

            # Checking for keys inside block_device
            # could be TYPE, PTTYPE
            #print("--------------->>>>>>>> block device: " + str(block_devices[block_device]))

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

                # IGNORE PARTITION TYPES in skip_partition_types
                if block_devices[block_device][TYPE].lower() in skip_partition_types:
                    SKIP_DEVICE = True
                    print("")
                    print("")
                    print("")
                    print("++++++----->>>>>>>> IGNORING partition type " + block_devices[block_device][TYPE].lower() + " in " + block_device)
                    print("")
                    log.warning("IGNORING partition type " + block_devices[block_device][TYPE].lower() + " in " + block_device)
                elif not block_device.startswith(tuple(skip_block_device_names)):
                    if not SKIP_DEVICE:
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
                            # for testing, mount_points and partitions
                            # are passed from here
                            # in real is_boot_partition function it's resolved inside
                            # the funtion itself
                            if not is_boot_partition(block_device, block_devices, mount_points, partitions):
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
            # SKIP NOT KNOWN TYPE PARTITIONS
            elif TYPE == 'NOT KNOWN':
                SKIP_DEVICE = True
                print("")
                print("->->->->->-> SKIPPING NOT KNOWN TYPE PARTITION !!!!: " + block_device)
                log.warning("->->->->->-> SKIPPING NOT KNOWN TYPE PARTITION !!!!: " + block_device)

        #return True
        print("")
        print("-------- LUKS ENCRYPTION RESULT --------")
        print("ENCRYPTED DEVICES: " + json.dumps(luks_assessment_encrypted, indent=4))
        print("")
        print("DEVICES NOT ENCRYPTED: " + json.dumps(luks_assessment_NOT_encrypted, indent=4))



        # If there are items in NOT encrypted device, return False
        if len(luks_assessment_NOT_encrypted) > 0:
            grains = {'luks_encrypted': False, 'encrypted_devices': luks_assessment_encrypted, 'NOT_encrypted_devices': luks_assessment_NOT_encrypted}
            __salt__['grains.set']('luks', grains, force=True)
            return False
        else:
            grains = {'luks_encrypted': True, 'encrypted_devices': luks_assessment_encrypted, 'NOT_encrypted_devices': luks_assessment_NOT_encrypted}
            __salt__['grains.set']('luks', grains, force=True)
            return True
    else:
        print("********* SYSTEM IN LIST OF SKIP BY OSFINGER")
        log.warning("********* SYSTEM IN LIST OF SKIP BY OSFINGER")
        return True
