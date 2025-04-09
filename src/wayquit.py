# Wayquit
# Copyright (C) 2025  Dino Duratović <dinomol at mail dot com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk

import os
import os.path
import configparser
import subprocess
import atexit
import shlex
import sys

PROG_NAME = "Wayquit"
ID = "prog.dglava.wayquit"

def parse_config():
    """Parses config file.

    Returns a configparger object containing all our options.
    It looks for config files in different locations, by priority:
    XDG_CONFIG_HOME, ~/.config and /etc.

    The "Cancel" button is always provided.
    The opacity option is always provided, i.e. has a default value
    unless overwritten.
    """
    default_options = {
        "commands": {
            "cancel": ""
            },
        "shortcuts": {
            "cancel": "Escape"
            },
        "options": {
            "opacity": "0.5"
            }
        }

    config = configparser.ConfigParser()
    config.read_dict(default_options)

    config_name = "wayquit.conf"
    user_config_dir = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config/"))
    user_config_path = os.path.join(user_config_dir, config_name)
    system_config_path = os.path.join("/etc", config_name)

    if os.path.exists(user_config_path):
        config.read(user_config_path)
    elif os.path.exists(system_config_path):
        config.read(system_config_path)

    try:
        float(config["options"]["opacity"])
    except ValueError:
        print("Error: Opacity value not valid. Must be float between 0 and 1.")
        sys.exit(1)

    return config

def execute_command(command):
    """Executes the provided command (program)."""
    try:
        subprocess.Popen(shlex.split(command))
    except FileNotFoundError:
        pass

class Wayquit(Gtk.ApplicationWindow):
    def __init__(self, config, **kargs):
        super().__init__(
            **kargs,
            title=PROG_NAME,
            decorated=False,
            fullscreened=True
            )
        self.config = config
        self.make_transparent()
        self.handle_shortcuts()
        self.create_holding_box()
        self.add_buttons()

    def make_transparent(self):
        """Makes the window transparent."""
        self.add_css_class("transparent-window")
        css = ".transparent-window {{ background-color: rgba(0, 0, 0, {opacity}); }}"
        css_with_transparency_value = css.format(opacity=self.config["options"]["opacity"])
        css_provider = Gtk.CssProvider()
        css_provider.load_from_string(css_with_transparency_value)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def handle_shortcuts(self):
        """Add keyboard shortcuts from config file."""
        shortcuts = Gtk.ShortcutController()
        self.add_controller(shortcuts)

        for command_name in self.config["shortcuts"]:
            if command_name in self.config["commands"]:
                shortcut_key = self.config["shortcuts"][command_name]
                command = self.config["commands"][command_name]

                shortcut = Gtk.Shortcut(
                    trigger=Gtk.ShortcutTrigger.parse_string(shortcut_key),
                    action=Gtk.CallbackAction.new(self.on_key_pressed, command)
                )
                shortcuts.add_shortcut(shortcut)

    def create_holding_box(self):
        """Creates the base layout.

        It consists of a horizontal box which eventualy holds the
        button/label widgets (both inside a box).
        """
        self.button_line = Gtk.Box(
            spacing=10,
            orientation=Gtk.Orientation.HORIZONTAL
            )
        self.button_line.set_halign(Gtk.Align.CENTER)
        self.button_line.set_valign(Gtk.Align.CENTER)
        self.button_line.set_homogeneous(True)
        self.set_child(self.button_line)

    def create_button(self, command_name, command):
        """Creates a button/label combo.

        Groups a button together with a label inside a Gtk.Box() and
        returns it.
        """
        box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)

        button = Gtk.Button()
        button.connect("clicked", self.on_button_clicked, command)

        label = Gtk.Label()
        label.set_markup(
            "<span fgcolor='white' size='large'>{}</span>".format(
                command_name.capitalize()
                )
            )

        box.append(button)
        box.append(label)

        return box

    def add_buttons(self):
        """Adds the buttons into a line.

        Goes through every command in the [commands] section and
        adds a button for it, appending it to the button_line Gtk.Box().
        """
        for command_name in self.config["commands"]:
            command = self.config["commands"][command_name]
            self.button_line.append(
                self.create_button(command_name, command)
                )

    def on_button_clicked(self, _gobject, command):
        """Handles button clicks.

        Runs the passed command just before the program terminates.
        """
        if command and command != "":
            atexit.register(execute_command, command)
        self.get_application().quit()

    def on_key_pressed(self, _widget, _variant, command):
        """Handles keyboard presses.

        Runs the passed command just before the program terminates.
        """
        if command and command != "":
            atexit.register(execute_command, command)
        self.get_application().quit()

def on_activate(prog, options):
    wayquit = Wayquit(options, application=prog)
    wayquit.present()

def run():
    config = parse_config()
    prog = Gtk.Application(application_id=ID)
    prog.connect("activate", on_activate, config)
    prog.run()

if __name__ == "__main__":
    run()
