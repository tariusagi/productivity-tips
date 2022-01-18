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

### Remove Bluetooth device

Run the following commands:

- `bluetoothctl`. This open the Bluetooth controller prompt, `[bluetooth]`.
- `[bluetooth]paired-devices`. This command will list currently paired devices, such as:

```txt
Device 34:88:5D:7A:7C:A2 Keyboard K380 
Device 34:88:5D:56:46:33 Bluetooth Mouse M557
```

- To remove a paired device, run `[bluetooth]remove <address>`, where `<address>` is the address (MAC) of the device to be unpaired.

NOTE: bluetooth config is stored at `/var/lib/bluetooth`. In that directory, there’s a directory for each controller, named after their ID, such as `00:1A:7D:DA:71:15`, and in the controller directory store the paired devices info, each in a directory named after their ID, too.
