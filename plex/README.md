# Plex.tv

## Change user that Plex Media Server run on Linux

Follow these steps to run plexmediaserver as `pi`:

- Stop plexmediaserver service: `sudo systemctl stop plexmediaserver`.
- Run `sudo systemctl edit plexmediaserver` and put these lines in:

```service
[Service]
User=pi
Group=pi
```

then save it and run `sudo systemctl daemon-reload` to update changes.

- Run `sudo chown -R pi:pi /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/`. Plex server need full permission on this directory.
- Run `sudo systemctl start plexmediaserver` to start the server.

And that's it.
