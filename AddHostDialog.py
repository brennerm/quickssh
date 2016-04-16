from gi.repository import Gtk


class AddHostDialog(Gtk.Dialog):
    def __init__(self, groups):
        super(AddHostDialog, self).__init__("Add Host", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.__groups = groups
        self.__error_message_displayed = False

        self.__content_area = self.get_content_area()

        user_label = Gtk.Label('Username (Default: Current User)')
        user_label.set_halign(Gtk.Align.START)
        self.__user_entry = Gtk.Entry()

        host_label = Gtk.Label('Hostname')
        host_label.set_halign(Gtk.Align.START)
        self.__host_entry = Gtk.Entry()

        port_label = Gtk.Label('Port (Default: 22)')
        port_label.set_halign(Gtk.Align.START)
        self.__port_entry = Gtk.Entry()
        self.__port_entry.connect('changed', AddHostDialog.only_allow_integer)

        group_label = Gtk.Label('Group')
        group_label.set_halign(Gtk.Align.START)

        self.__group_combo = Gtk.ComboBoxText()
        for group in self.__groups:
            self.__group_combo.append_text(group)

        self.__content_area.add(user_label)
        self.__content_area.add(self.__user_entry)
        self.__content_area.add(host_label)
        self.__content_area.add(self.__host_entry)
        self.__content_area.add(port_label)
        self.__content_area.add(self.__port_entry)
        self.__content_area.add(group_label)
        self.__content_area.add(self.__group_combo)

        self.__content_area.show_all()

    @property
    def username(self):
        return self.__user_entry.get_text()

    @property
    def hostname(self):
        return self.__host_entry.get_text()

    @property
    def port(self):
        return self.__port_entry.get_text()

    @property
    def group_name(self):
        return self.__group_combo.get_active_text()

    def show_error(self):
        if not self.__error_message_displayed:
                error_label = Gtk.Label('<span foreground="red">Hostname is required!</span>')
                error_label.set_use_markup(True)
                self.__content_area.add(error_label)
                self.__content_area.show_all()


    @staticmethod
    def only_allow_integer(entry):
        text = entry.get_text().strip()
        entry.set_text(''.join([i for i in text if i in '0123456789']))
