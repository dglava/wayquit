# Wayquit
Utility script for logging out of a session. Continuation of
[Obquit](https://github.com/dglava/obquit), but this one works with
Wayland and uses Gtk4.

![](https://raw.githubusercontent.com/dglava/wayquit/master/screen.png)

##### Dependencies (Arch package names)
* python
* python-gobject
* gtk4

##### What works
- Custom command assignment (uses systemd by default)
- Keyboard shortcuts

##### How to use
- Build and install
- Edit the config file (`/etc/wayquit.conf` or `~/.config/wayquit.conf`)
- Run `wayquit`

Arch Linux users can use the [PKGBUILD from here](https://raw.githubusercontent.com/dglava/pkgbuilds/refs/heads/master/wayquit-git/PKGBUILD).
