# Retropie Tips

This includes other variants such as RetrOrangePi.

## Change ROMs directories in EmulationStatin (ES)

Edit the `path` tags in `/etc/emulationstation/es_systems.cfg file`, such as:

```xml
<?xml version="1.0"?>
<systemList>
	<system>
		<name>snes</name>
			<fullname>Super Nintendo</fullname>
			<path>/mnt/nas/RetroPie/roms/snes</path>
			<extension>.bin .smc .sfc .fig .swc .mgd .zip .BIN .SMC .SFC .FIG .SWC .MGD .ZIP</extension>
			<command>/opt/retropie/supplementary/runcommand/runcommand.sh 0 _SYS_ snes %ROM%</command>
			<platform>snes</platform>
			<theme>snes</theme>
			<directlaunch />
			<viewmode>DEFAULT</viewmode>
			<enabled>true</enabled>
			<gridsize>1</gridsize>
	</system>
</systemList>
```

## Change ES UI mode

Set the value of `UIMode` in `/opt/retropie/configs/all/emulationstation`, such as:

```xml
<string name="UIMode" value="Kiosk" />
```

The values can be `Full`, `Kiosk` or `Kid`.

Additionally, set the passkey sequence in the `UIMode_passkey` value, such as:

```xml
<string name="UIMode_passkey" value="uuddlrlrba" />
```

which stands for `UP, UP, DOWN, DOWN, LEFT, RIGHT, LEFT, RIGHT, B, A` (A famous Konami cheat code).

## Set video billinear filtering for all cores

Set `video_smooth = "true"` in `/opt/retropie/configs/all/retroarch.cfg`. This apply as default for all cores, effectively smooth image with very little performance hit.
