# X.org tips

## Run an X application without desktop manager
Running an X application without a desktop manager like gdm, lightdm... means there's only this application's GUI on display, no taskbar, no system menu, no other windows... Sometime this is desirable, such as running a sole GUI application in a low-end device like a Raspberry Pi Zero.

To do this, first exit or disable booting into any desktop manager. Then run that app, for example, `xterm`, with this command as *root/sudo*:
```sh
/usr/bin/xinit /usr/bin/xterm -- :0
```
To run as a non-root user, use `su`. The following run `xterm` as `peter`:
```sh
/usr/bin/xinit /usr/bin/su peter -c /usr/bin/xterm -- :0
```
To run the application at boot, use `/etc/rc.local`.

