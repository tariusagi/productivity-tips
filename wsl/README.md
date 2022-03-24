# Tips for Windows Subsystem for Linux

## Disable beep

To disable the beep in bash you need to uncomment (or add if not already there) the line `set bell-style none` in your `/etc/inputrc` file. It will take effect next time using the shell.

## Mount Windows drive

To mount an existing drive, such as E:, to a mount point, such as `/mnt/e`, in
WSL, run this command:

```sh
sudo mount -t drvfs e: \mnt\e
```

Note that mount point `\mnt\e` must be created first.

This also work with external drives such as USB flash disks, but not mapped
network share. For network share, use the next tip.

## Mount a network share

Mounting a SMB/CIFS network share in WSL is exactly the same as with a real
Linux system. Thus, follow the SMB/CIFS sections in this
[File system tips](../linux/README.md#mount-a-sambacifs-network-share) document.

## Add/delete port forwarding rule to WSL

See [wslportfwd.cmd](https://github.com/tariusagi/shellutils/blob/main/win/wslportfwd.cmd).

## View port forwarding rules

Run this command in Windows as an admin:

```cmd
netsh interface portproxy show v4tov4
```

It should return something like:

```cmd
Listen on ipv4:             Connect to ipv4:

Address         Port        Address         Port
--------------- ----------  --------------- ----------
0.0.0.0         1234        172.20.33.157   1234
```

Which means there's a rule to forward host port 1234 to WSL port 1234 on
interface 172.20.33.157 (this is the IP of a WSL distro NIC).
