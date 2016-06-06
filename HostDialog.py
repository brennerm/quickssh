from gi.repository import Gtk, Gdk


class HostDialog(Gtk.Dialog):
    def __init__(self, groups, user='', host='', port='', label='', selected_group=''):
        super(HostDialog, self).__init__("Add Host", None, 0,
                                         (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                         Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.__groups = groups
        self.__error_message_displayed = False

        self.connect('key-release-event', self.__key_release)

        self.__content_area = self.get_content_area()

        user_label = Gtk.Label('Username (Default: Current User)')
        user_label.set_halign(Gtk.Align.START)
        self.__user_entry = Gtk.Entry()
        self.__user_entry.set_text(user or '')

        host_label = Gtk.Label('Hostname or IP address')
        host_label.set_halign(Gtk.Align.START)
        self.__host_entry = Gtk.Entry()
        self.__host_entry.set_text(host)

        port_label = Gtk.Label('Port (Default: 22)')
        port_label.set_halign(Gtk.Align.START)
        self.__port_entry = Gtk.Entry()
        self.__port_entry.set_text(port or '')
        self.__port_entry.connect('changed', HostDialog.only_allow_integer)

        label_label = Gtk.Label('Label')
        label_label.set_halign(Gtk.Align.START)
        self.__label_entry = Gtk.Entry()
        self.__label_entry.set_text(label or '')

        group_label = Gtk.Label('Group')
        group_label.set_halign(Gtk.Align.START)

        self.__group_combo = Gtk.ComboBoxText()
        for id, group in enumerate(self.__groups):
            id = str(id)
            self.__group_combo.append(id, group)
            if group == selected_group:
                self.__group_combo.set_active_id(id)

        self.__content_area.add(user_label)
        self.__content_area.add(self.__user_entry)
        self.__content_area.add(host_label)
        self.__content_area.add(self.__host_entry)
        self.__content_area.add(port_label)
        self.__content_area.add(self.__port_entry)
        self.__content_area.add(label_label)
        self.__content_area.add(self.__label_entry)
        self.__content_area.add(group_label)
        self.__content_area.add(self.__group_combo)

        self.__content_area.show_all()

    def prompt(self):
        while True:
            result = self.run()

            if result == Gtk.ResponseType.CANCEL:
                self.destroy()
                return

            if self.hostname:
                break

            self.show_error()

        hostname = self.hostname
        username = self.username
        port = self.port
        label = self.label
        group_name = self.group_name

        self.destroy()

        return group_name, hostname, username, port, label

    def __key_release(self, widget, event):
        if event.keyval == Gdk.KEY_Return:
            self.response(Gtk.ResponseType.OK)
            return True

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
    def label(self):
        return self.__label_entry.get_text()

    @property
    def group_name(self):
        return self.__group_combo.get_active_text()

    def show_error(self):
        if not self.__error_message_displayed:
                error_label = Gtk.Label('<span foreground="red">Hostname is required...</span>')
                error_label.set_use_markup(True)
                self.__content_area.add(error_label)
                self.__content_area.show_all()

    @staticmethod
    def only_allow_integer(entry):
        text = entry.get_text().strip()
        entry.set_text(''.join([i for i in text if i in '0123456789']))
