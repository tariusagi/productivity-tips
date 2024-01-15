# General Linux tips

## Mount a partition in a disk image

To mount a partiton in a disk image, we need to find the start offset of that partition with `fdisk`, then use `losetup` to bind the partition into a loopback device, and finally, use `mount` to mount that loopback device to a mount point and start using it.

First, find the start offset of the partition with `fdisk`, example:

```sh
$ sudo fdisk -lu disk.img
Disk disk.img: 6.65 GiB, 7141847552 bytes, 13948921 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x735894a1

Device                        Boot  Start      End  Sectors  Size Id Type
disk.img1        8192   532479   524288  256M  c W95 FAT32 (LBA)
disk.img2      532480 13948920 13416441  6.4G 83 Linux
```

Now, we want to mount the second partition, which starts at sector `532480`. Times it with sector size, which is `512` bytes, to get the start offset in bytes. Then use it with `losetup`, like this:

```sh
sudo losetup -o $((532480 * 512)) /dev/loop0 disk.img
```

Finally, mount and start using it:

```sh
sudo mkdir /mnt/loop
sudo mount /dev/loop0 /mnt/loop/
```

When we're done with it, umount and unbind:

```sh
sudo umount /dev/loop0
sudo losetup -d /dev/loop0
```

## Mount any block device with fstab

To make a block device mount permanent at boot, edit the `/etc/fstab` and add:

```fstab
UUID=<UUID> <mount point> <fs type> uid=1000,gid=1000,umask=0022,sync,auto,rw 0 0
```

where:

- `UUID` is the UUID of the disk or partition to mount. Use `blkid` to view a list of available block devices along with their UUID. Instead of UUID, `PARTUUID` can also be used.
- `mount point` is a directory where the block device will be mounted. This directory must be created first.
- `fs type` is the type of file system (exfat, ntfs, ext4...). Use `blkid` to check.
- `uid`, `gid` are the user's ID and group's ID to be set as the owner of the mount.
- `umask` is the default file permission mask.

Example:

```fstab
UUID=E34F-5608 /home/phuong/usb/WD6T01 exfat uid=1000,gid=1000,umask=0022,sync,auto,rw 0 0
```

or

```fstab
PARTUUID=d9d5f18c-01 /mnt/EXT-WD2T ntfs uid=1000,gid=1000,umask=0022,sync,auto,rw 0 0
```

## Mount a Samba/CIFS network share

Samba/CIFS requires `cifs-utils` package. Install it with `sudo apt install cifs-utils`.

Now, create the mount point:

```sh
sudo mkdir /mnt/cifs
```

Then, run this command to mount:

```sh
sudo mount -t cifs //server/share/peter /mnt/cifs -ouid=peter,gid=peter,vers=1.0,rw,username=peter,password=peterpassword
```

## Mount a SAMBA/CIFS network share at boot

Put this line in `/etc/fstab`:

```fstab
//server/share/peter /mnt/cifs cifs uid=peter,gid=peter,vers=1.0,rw,username=peter,password=peterpassword,x-systemd.automount,noauto 0 0
```

And the system will create the mount point `/mnt/cifs` which bind to `/share/peter/` directory on `server`.

NOTE:

- Normally the network is not ready yet when the system reboot and carry out the mount points in `fstab`, which certainly cause network dependent mount point such as CIFS to fail. So here we use the `x-systemd.automount` option tells the system to delay mounting until the first access, which usually happen after the network has become available.
- We don't have to create the mount point (`/mnt/cifs`) first, the system will create it if it doesn't exist yet.
- The option `vers=1.0` is for compatibility. Recent Samba/CIFS may support newer version, thus this option can be removed.

## Transfer file over the network with netcat (nc)

On the receiving end run:

```sh
nc -l -p 1234 > outfile
```

`nc` will listen on port 1234 and write received data to `outfile`.

On the sending end run:

```sh
nc -w 3 <destination host> 1234 < infile
```

`nc` will read `infile` (redirected to its stdin) and send to the receving end.

To speed up, *compress* the file while sending and *decompress* it while
receiving. On the receiving end:

```sh
nc -l -p 1234 | gunzip -c > outfile
```

On the sending end:

```sh
gzip -c infile | nc -w3 <desctination host> 1234
```

Or to show transfer speed, include `pv`:

```sh
gzip -c infile | pv | nc -w3 <desctination host> 1234
```

## Truncate or write to privileged file with sudo

If we have a `/var/log/myprog.log` which only `root` have write access, and we try to truncate it with `sudo cat /dev/null > /var/log/myprog.log`, we will get the "permission denied" error. Why?

It's because `sudo` only applies to the fist command, which is `cat`, after that , `sudo` terminate and return to shell, which does not have root privilege, therefore the redirection will fail.

To achieve the desirable result, use this command instead:

```sh
sudo tee /var/log/myprog.log < /dev/null
```

In this command, shell will redirect `/dev/null` as the input of `sudo`, which execute `tee` and `tee` will write the input, which is `null`, to the log file.

Similarly, to write something to that log file, use this:

```sh
echo Some text | sudo tee /var/log/myprog.log
```

## Capture output as a terminal

Some programs behave differently if it knows the output is not a terminal, such as discarding all ANSI color codes. Therefore if we redirect its output to a file, the ANSI color codes will not be there. To capture that program's output into a file while make it think it's still output to a terminal, we use the `script` program (should be readily available in all distros).

For example:

```sh
sudo script -aefqc 'dmesg -w' /tmp/dmesg.log
```

The above command run `dmesg -w` command and continuously append its output to `/tmp/dmesg.log` as if it was running in a normal terminal, thus the log file will retains all of its ANSI colors output. This log file can be monitored with `tail -f /tmp/dmesg.log` or `less -R +F /tmp/dmesg.log`. The additonal options are:

- a: append to log file.
- e: use exit code of the child command.
- f: flush writes to log file immediately (no buffering).
- q: do not print script start and end message.

## Use less instead of tail

`tail -f` is usually used to monitor log file in real time. But it doesn't have sophisticated search and filter functionality of `less`. Use `less -R +F` to have the same effect as `tail -f`. For example:

```sh
less -R +F /var/log/dmesg
```

The `-R` option tell `less` to inteprete ANSI codes, while `+F` tell it to continuously follow that log file's updates.

Another use case is to use less to filter and hight light search pattern all while monitoring a file. For example:

```sh
sudo less -R +\&CRON^M/$USER^MSF /var/log/syslog
```

will filter out just lines that have "CRON" in them, and within the result, high light current user name, all while monitoring `/var/log/syslog`. In the above example, `^M` means `Ctrl-M` (you literally press `Ctrl-M` while typing that command).

## Remote control a physical console (YAY!)

The `conspy` program allow you to take control of a Linux virtual console, including the physical one (real keyboard, real monitor). Install it with `sudo apt install conspy`, and simply run:

```sh
sudo conspy
```

to take control of the physical console. This trick is perfect for working with a Linux computer that you don't have access to its keyboard.

## Quietly check service status

Use `systemctl is-active --quiet myservice`. It will return with zero exit code if `myservice` is active, or non-zero otherwise. See this systemd manual [section](https://www.freedesktop.org/software/systemd/man/systemctl.html#is-active%20PATTERN%E2%80%A6)

## Working with Bluetooth in CLI

### Connect Bluetooth keyboard

Input the following commands:

1. `bluetoothctl`
2. `pairable on`
3. `scan on`. Then wait until BT device (keyboard) is shown (don’t forget to turn on the keyboard pairing mode now). You should see it's address as `xx:xx:xx:xx:xx:xx`.
4. `scan off`
5. `agent on`
6. `pair xx:xx:xx:xx:xx:xx`. Now you are requested to input a number (6 digits) using your BT keyboard, ended with `Enter` key! A *"pairing successful"* should be displayed.
7. `trust xx:xx:xx:xx:xx:xx`
8. `connect xx:xx:xx:xx:xx:xx`. A *"connection successful"* message should be displayed.
9. Finally, run `info xx:xx:xx:xx:xx:xx` to view connection info.
10. Exit and reboot.

### Connect Bluetooth game controller

For a game controller that support Bluetooth, such as the PlayStation 3/4 Dualshock wireless controller, run `bluetoothctl` and  enter these commands at its prompt:

```txt
[bluetooth]# agent DisplayYesNo
Agent registered
[bluetooth]# default-agent
Default agent request successful
[bluetooth]# power on
Changing power on succeeded
[CHG] Controller 00:1A:7D:DA:71:15 Powered: yes
[bluetooth]# discoverable on
Changing discoverable on succeeded
[CHG] Controller 00:1A:7D:DA:71:15 Discoverable: yes
[bluetooth]# pairable on
Changing pairable on succeeded
[bluetooth]# scan on
Discovery started
[CHG] Device 98:B6:E9:5C:D2:DC RSSI: -68
[CHG] Device 98:B6:E9:5C:D2:DC UUIDs:
        00001124-0000-1000-8000-00805f9b34fb
        00001200-0000-1000-8000-00805f9b34fb
[bluetooth]# devices
Device 98:B6:E9:5C:D2:DC Wireless Controller
[bluetooth]# pair 98:B6:E9:5C:D2:DC
Attempting to pair with 98:B6:E9:5C:D2:DC
[CHG] Device 98:B6:E9:5C:D2:DC Connected: yes
[CHG] Device 98:B6:E9:5C:D2:DC UUIDs:
        00001124-0000-1000-8000-00805f9b34fb
        00001200-0000-1000-8000-00805f9b34fb
[CHG] Device 98:B6:E9:5C:D2:DC Paired: yes
Pairing successful
[CHG] Device 98:B6:E9:5C:D2:DC Connected: no
[bluetooth]# trust 98:B6:E9:5C:D2:DC
[CHG] Device 98:B6:E9:5C:D2:DC Trusted: yes
Changing 98:B6:E9:5C:D2:DC trust succeeded
[bluetooth]# info 98:B6:E9:5C:D2:DC
Device 98:B6:E9:5C:D2:DC
        Name: Wireless Controller
        Alias: Wireless Controller
        Class: 0x002508
        Icon: input-gaming
        Paired: yes
        Trusted: yes
        Blocked: no
        Connected: no
        LegacyPairing: no
        UUID: Human Interface Device... (00001124-0000-1000-8000-00805f9b34fb)
        UUID: PnP Information           (00001200-0000-1000-8000-00805f9b34fb)
        Modalias: usb:v054Cp09CCd0100
[bluetooth]# scan off
[bluetooth]# quit
```

Note that the pair command may fail with "AuthenticationTimeout" error. Wait until the controller is off, then turn its pairing mode on and try again. It may work after several attempts.

### Remove Bluetooth device

Run the following commands at the `bluetoothctl` prompt:

```txt
[bluetooth]# paired-devices
Device 34:88:5D:7A:7C:A2 Keyboard K380 
Device 34:88:5D:56:46:33 Bluetooth Mouse M557
[bluetooth]# remove 34:88:5D:56:46:33
[bluetooth]# quit
```

- To remove a paired device, run `[bluetooth]remove <address>`, where `<address>` is the address (MAC) of the device to be unpaired.

NOTE: bluetooth config is stored at `/var/lib/bluetooth`. In that directory, there’s a directory for each controller, named after their ID, such as `00:1A:7D:DA:71:15`, and in the controller directory store the paired devices info, each in a directory named after their ID, too.

## Force display mode with EDID

Normally, when being connected to an HDMI monitor/TV, Linux will try to get the monitor/TV info from EDID, and will try to set the maximum resolution available. To force different resolution, for example, 720p on a Sony 4K TV, we will have to clone that TV's EDID firmware, tell kernel to load it, and set the desired mode.

First, run the following command to get a list of display connections and their statuses.

```sh
$ for p in /sys/class/drm/*/status; do con=${p%/status}; echo -n "${con#*/card?-}: "; cat $p; done
HDMI-A-1: connected
```

In this example, we have `HDMI-A-1` connected to the TV. Now clone the EDID firmware:

```sh
sudo cat /sys/class/drm/card0-HDMI-A-1/edid > /lib/firmware/edid/sony4ktv.bin
```

Note: Create `/lib/firmware/edid` directory first if it does not exist yet.

Now create a initramfs hook to include this firmware in the initramfs so the kernel can find it during boot. Create the file `/etc/initramfs-tools/hooks/edid` with this content:

```sh
#!/bin/sh
PREREQ=""
prereqs()
{
    echo "$PREREQ"
}

case $1 in
prereqs)
    prereqs
    exit 0
    ;;
esac

. /usr/share/initramfs-tools/hook-functions
# Begin real processing below this line
mkdir -p "${DESTDIR}/lib/firmware/edid"
cp -a /lib/firmware/edid/sony4ktv.bin "${DESTDIR}/lib/firmware/edid/sony4ktv.bin"
exit 0
```

Then, update the initramfs with `sudo update-initramfs -u`.

Finally, force the setting with this kernel command line (for Armbian based OS, put in `/boot/armbianEnv.txt`):

```txt
extraargs=drm.edid_firmware=HDMI-A-1:edid/sony4ktv.bin video=HDMI-A-1:1280x720D
```

## Transmission Bitorrent installation

This guide uses the `pi` user and target directory is `/mnt/nas`. Change them if needed.

First, install it with `sudo apt install transmission-daemon`.

Then run `sudo systemctl edit transmission-daemon` and put in the following section:

```txt
[Service]
User=pi
Group=pi
```

After that, create a `/home/pi/.config/transmission-daemon/settings.json` with this content, then start the service with `sudo systemctl start transmission-daemon`:

```json
{
    "alt-speed-down": 50,
    "alt-speed-enabled": false,
    "alt-speed-time-begin": 540,
    "alt-speed-time-day": 127,
    "alt-speed-time-enabled": false,
    "alt-speed-time-end": 1020,
    "alt-speed-up": 50,
    "bind-address-ipv4": "0.0.0.0",
    "bind-address-ipv6": "::",
    "blocklist-enabled": false,
    "blocklist-url": "http://www.example.com/blocklist",
    "cache-size-mb": 4,
    "dht-enabled": true,
    "download-dir": "/mnt/nas/Torrents/Completed",
    "download-queue-enabled": true,
    "download-queue-size": 5,
    "encryption": 1,
    "idle-seeding-limit": 30,
    "idle-seeding-limit-enabled": false,
    "incomplete-dir": "/mnt/nas/Torrents/Downloading",
    "incomplete-dir-enabled": true,
    "lpd-enabled": false,
    "message-level": 1,
    "peer-congestion-algorithm": "",
    "peer-id-ttl-hours": 6,
    "peer-limit-global": 200,
    "peer-limit-per-torrent": 50,
    "peer-port": 51413,
    "peer-port-random-high": 65535,
    "peer-port-random-low": 49152,
    "peer-port-random-on-start": false,
    "peer-socket-tos": "default",
    "pex-enabled": true,
    "port-forwarding-enabled": true,
    "preallocation": 1,
    "prefetch-enabled": true,
    "queue-stalled-enabled": true,
    "queue-stalled-minutes": 30,
    "ratio-limit": 2,
    "ratio-limit-enabled": false,
    "rename-partial-files": true,
    "rpc-authentication-required": true,
    "rpc-bind-address": "0.0.0.0",
    "rpc-enabled": true,
    "rpc-host-whitelist": "",
    "rpc-host-whitelist-enabled": true,
    "rpc-password": "{e7da0f2ae5e32c7019b5a5c60b8f0d3fb677cfb5i0QKw//5",
    "rpc-port": 9091,
    "rpc-url": "/transmission/",
    "rpc-username": "phuong",
    "rpc-whitelist": "*.*.*.*",
    "rpc-whitelist-enabled": true,
    "scrape-paused-torrents-enabled": true,
    "script-torrent-done-enabled": false,
    "script-torrent-done-filename": "",
    "seed-queue-enabled": false,
    "seed-queue-size": 10,
    "speed-limit-down": 100,
    "speed-limit-down-enabled": false,
    "speed-limit-up": 100,
    "speed-limit-up-enabled": false,
    "start-added-torrents": true,
    "trash-original-torrent-files": false,
    "umask": 18,
    "upload-slots-per-torrent": 14,
    "utp-enabled": true
}
```

Finally, start it with `sudo systemctl start transmission-daemon`.

For more info on this kernel setting, see this [link](https://wiki.archlinux.org/title/kernel_mode_setting), and this [link](https://forums.raspberrypi.com/viewtopic.php?t=327875).

Now, reboot, and the new resolution should be enforced.
