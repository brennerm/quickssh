from gi.repository import Gtk


class GroupDialog(Gtk.Dialog):
    def __init__(self, group_name=''):
        super(GroupDialog, self).__init__("Add Group", None, 0,
                                          (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.__error_message_displayed = False

        self.__content_area = self.get_content_area()

        name_label = Gtk.Label('Group Name')
        name_label.set_halign(Gtk.Align.START)
        self.__name_entry = Gtk.Entry()
        self.__name_entry.set_text(group_name)

        self.__content_area.add(name_label)
        self.__content_area.add(self.__name_entry)

        self.__content_area.show_all()

    @property
    def name(self):
        return self.__name_entry.get_text()

    def show_error(self):
        if not self.__error_message_displayed:
                error_label = Gtk.Label('<span foreground="red">Group name is required...</span>')
                error_label.set_use_markup(True)
                self.__content_area.add(error_label)
                self.__content_area.show_all()