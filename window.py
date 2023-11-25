# TODO xml ordering

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

class Interrupt(Gtk.Window):
    def __init__(self):
        super().__init__(title="Interrupt-GUI")
        self.set_border_width(10) # TODO CHECK
        self.set_default_size(600, 400) # TODO CHECK

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(500)

        checkbutton = Gtk.CheckButton(label="Click me!")
        self.stack.add_titled(checkbutton, "1", "Check Button")

        label = Gtk.Label()
        label.set_markup("<big>A fancy label</big>")
        self.stack.add_titled(label, "2", "A label")

        self.add(self.stack)

        # Headerbar
        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        headerbar.props.title = "Interrupt"
        self.set_titlebar(headerbar)

        # Right headerbar button
        button = Gtk.Button(label="right")
        button.get_style_context().add_class("suggested-action")
        button.connect("clicked", self.next_page)
        headerbar.pack_end(button)

        # Left headerbar buttons
        button = Gtk.Button(label="left")
        button.connect("clicked", self.previous_page)
        headerbar.pack_start(button)

        # TODO make this more efficient
        about = Gtk.AboutDialog()
        about.set_program_name("Interrupt-GUI"),
        about.set_version("0.0.1"),
        about.set_website("https://github.com/hiimsergey/interrupt-gui"),
        about.set_authors(["Sergey Lavrent"]),
        about.set_comments("Easily create \"X hours of silence occasionally broken by Y\" audios")
        about.connect("response", self.on_about_response)
        
        about_button = Gtk.Button(label="About")
        about_button.connect("clicked", self.on_about_button_clicked, about)
        
        headerbar.pack_end(about_button)

    def on_about_button_clicked(self, widget, about):
        about.run()

    def on_about_response(self, dialog, response_id):
        dialog.destroy()

    def greet(self, widget):
        print("Hello World")

    def next_page(self, widget):
        self.stack.set_visible_child_name(
            str(int(self.stack.get_visible_child_name()) + 1)
        )

    def previous_page(self, widget):
        self.stack.set_visible_child_name(
            str(int(self.stack.get_visible_child_name()) - 1)
        )

win = Interrupt()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
