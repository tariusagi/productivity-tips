# Tips for Windows Subsystem for Linux

## Mount Windows drive
To mount an existing drive, such as E:, to a mount point, such as `/mnt/e`, in WSL, run this command:
```sh
sudo mount -t drvfs e: \mnt\e
```
Note that mount point `\mnt\e` must be created first.

This also work with external drives such as USB flash disks, but not mapped network share. For network share, use the next tip.

## Mount a network share
Mounting a SMB/CIFS network share in WSL is exactly the same as with a real Linux system. Thus, follow the SMB/CIFS sections in this [File system tips](../fs/README.md#mount-a-samba-cifs-network-share) document.