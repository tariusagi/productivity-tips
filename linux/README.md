# General Linux tips

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
```
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

To speed up, *compress* the file while sending and *decompress* it while receiving.
On the receiving end:
```sh
nc -l -p 1234 | gunzip -c > outfile
```

On the sending end:
```sh
gzip -c infile | nc -w3 <desctination host> 1234
```