# X.org tips

## Boot into desktop or text console

- To boot into desktop: `sudo systemctl set-default graphical.target`
- To boot into console: `sudo systemctl set-default multi-user.target`
- Check current boot target: `sudo systemctl get-default`

## Automatically run a program or script after LXDE login

Edit `/etc/xdg/lxsession/LXDE-pi/autostart` and put the path to the program./script before `@xscreensaver -no-splash`. Change `pi` to the intended user if the name is not `pi`.

```txt
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
/home/pi/bin/homecam
@xscreensaver -no-splash
```

## Run an X application without desktop manager

Running an X application without a desktop manager like gdm, lightdm... means
there's only this application's GUI on display, no taskbar, no system menu, no
other windows... Sometime this is desirable, such as running a sole GUI
application in a low-end device like a Raspberry Pi Zero.

To do this, first exit or disable booting into any desktop manager. Then run
that app, for example, `xterm`, with this command as *root/sudo*:

```sh
/usr/bin/xinit /usr/bin/xterm -- :0
```

To run as a non-root user, use `su`. The following run `xterm` as `peter`:

```sh
/usr/bin/xinit /usr/bin/su peter -c /usr/bin/xterm -- :0
```

To run the application at boot, use `/etc/rc.local` or create a systemd service
with `Type=idle` in `[Service]` section (to make sure it run after everything
else).

## Set up X11VNC as a service

First, install x11vnc with `apt install -y x11vnc`. Then create the file `/etc/systemd/system/x11vnc.service` with the following content (change the PASSWORD if needed):

```systemd
[Unit] 
Description=x11vnc service 
After=display-manager.service network.target syslog.target 

[Service] 
Type=simple 
ExecStart=/usr/bin/x11vnc -forever -repeat -shared -o /var/log/x11vnc.log -display :0 -auth guess -passwd PASSWORD 
ExecStop=/usr/bin/killall x11vnc 
Restart=on-failure 

[Install] 
WantedBy=multi-user.target 
```

After that, reload systemd services, then enable and start this service to run at boot with the following commands:

```sh
systemctl daemon-reload
systemctl enable x11vnc
systemctl start x11vnc
```

Test the connection by connecting to the host by port `5900` using a VNC client, enter the given password.

NOTES:

- `x11vnc` doesn’t work well with `gdm`. Use `lightdm` instead. In Ubuntu, `sudo apt install lightdm` and choose to use `lightdm` instead of `gdm`.
- On Ubuntu GNOME desktop, disable Wayland first. Edit `/etc/gdm3/custom.conf` and uncomment line `WaylandEnable=false` and reboot to take effect.
- On Xubuntu/Xfce, to fix screen update delay (few seconds), disable display compositing by uncheck `Window Manager Tweaks\Compositor\Enable display compositing`.
- Test running `x11vnc` as root (use the command at `ExecStart`) first to make sure it work before setting it up as a service. If it failed with `xauth: file /root/.Xauthority does not exist`, then change `-auth guess` to `-auth /var/run/lightdm/root/:0` may help (this is for LightDM display manager, for other display manager, the actual path may change).
- If `x11vnc` failed with `shmget: Function not implemented`, then add `-noshm` argument will resolve this.
- Use `-rfbauth` option to read password from file instead of passing `-passwd PASSWORD` on the command line.
- Omit the `-passwd` if no authentication is needed.
