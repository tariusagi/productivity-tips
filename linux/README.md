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

```fstab
//server/share/peter /mnt/cifs cifs uid=peter,gid=peter,vers=1.0,rw,username=peter,password=peterpassword,x-systemd.automount,noauto 0 0
```

And the system will create the mount point `/mnt/cifs` which bind to
`/share/peter/` directory on `server`.

NOTE:

- Normally the network is not ready yet when the system reboot and carry out the
mount points in `fstab`, which certainly cause network dependent mount point
such as CIFS to fail. So here we use the `x-systemd.automount` option tells the
system to delay mounting until the first access, which usually happen after the
network has become available.
- We don't have to create the mount point (`/mnt/cifs`) first, the system will
create it if it doesn't exist yet.
- The option `vers=1.0` is for compatibility. Recent Samba/CIFS may support
newer version, thus this option can be removed.

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

If we have a `/var/log/myprog.log` which only `root` have write access, and we
try to truncate it with `sudo cat /dev/null > /var/log/myprog.log`, we will get
the "permission denied" error. Why?

It's because `sudo` only applies to the fist command, which is `cat`, after that
, `sudo` terminate and return to shell, which does not have root privilege,
therefore the redirection will fail.

To achieve the desirable result, use this command instead:

```sh
sudo tee /var/log/myprog.log < /dev/null
```

In this command, shell will redirect `/dev/null` as the input of `sudo`, which
execute `tee` and `tee` will write the input, which is `null`, to the log file.

Similarly, to write something to that log file, use this:

```sh
echo Some text | sudo tee /var/log/myprog.log
```

## Capture output as a terminal

Some programs behave differently if it knows the output is not a terminal, such
as discarding all ANSI color codes. Therefore if we redirect its output to a
file, the ANSI color codes will not be there. To capture that program's output
into a file while make it think it's still output to a terminal, we use the
`script` program (should be readily available in all distros).

For example:

```sh
sudo script -a -f -q -c 'dmesg -w' /tmp/dmesg.log
```

The above command run `dmesg -w` command and continuously append its output to
`/tmp/dmesg.log` as if it was running in a normal terminal, thus the log file
will retains all of its ANSI colors output. The `-f` option make sure the log
file is updated immediately after each write from the output. This log file can
be monitored with `tail -f /tmp/dmesg.log` or `less -R +F /tmp/dmesg.log`.

## Use less instead of tail

`tail -f` is usually used to monitor log file in real time. But it doesn't have
sophisticated search and filter functionality of `less`. Use `less -R +F` to
have the same effect as `tail -f`. For example:

```sh
less -R +F /var/log/dmesg
```

The `-R` option tell `less` to inteprete ANSI codes, while `+F` tell it to
continuously follow that log file's updates.
