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

PROG_NAME = "Wayquit"

class Wayquit(Gtk.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title=PROG_NAME)
        self.fullscreen()
        self.create_holding_box()
        self.make_transparent()

    def make_transparent(self):
        """Makes the window transparent."""
        self.add_css_class("transparent-window")
        css_provider = Gtk.CssProvider()
        css_provider.load_from_string(
            ".transparent-window { background-color: rgba(255, 255, 255, 0.2); }"
        )
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

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
        # testing buttons
        for i in range(5):
            self.button_line.append(self.create_button(i))

    def create_button(self, name):
        """Creates a button/label combo.

        Groups a button together with a label inside a Gtk.Box() and
        returns it.
        """
        box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        button = Gtk.Button()
        button.set_opacity(1)
        label = Gtk.Label(label=str(name))
        box.append(button)
        box.append(label)
        return box

def on_activate(prog):
    wayquit = Wayquit(application=prog)
    wayquit.present()

def run():
    prog = Gtk.Application(application_id="test.test")
    prog.connect("activate", on_activate)
    prog.run()

if __name__ == "__main__":
    run()
