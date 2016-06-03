from gi.repository import Gtk


class RmGroupConfirmDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self, "Remove Group", None, 0,
            (Gtk.STOCK_DELETE, Gtk.ResponseType.DELETE_EVENT,
             Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        self.set_default_size(150, 100)

        label = Gtk.Label("The group you want to remove still contains entries.\nDo you want to delete the group including it's content?")

        box = self.get_content_area()
        box.add(label)
        self.show_all()


