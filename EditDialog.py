from gi.repository import Gtk

from QuickSSHEntry import QuickSSHEntry
from HostDialog import HostDialog
from GroupDialog import GroupDialog
from RmGroupConfirmDialog import RmGroupConfirmDialog


class EditDialog(Gtk.Dialog):
    def __init__(self, quick_menu):
        super(EditDialog, self).__init__("Edit", None, 0, ())

        self.__quick_menu = quick_menu
        self.__store = Gtk.TreeStore(str, str, str, str, str, str)
        self.__tree_view = None

        self.__build_store()

        self.__tree_view = Gtk.TreeView(self.__store)
        self.__tree_view.expand_all()
        self.__tree_view.set_headers_visible(False)

        renderer = Gtk.CellRendererText()
        connection_string_column = Gtk.TreeViewColumn('', renderer, text=5)
        self.__tree_view.append_column(connection_string_column)

        add_host_button = Gtk.Button('Add Host')
        add_group_button = Gtk.Button('Add Group')
        remove_button = Gtk.Button('Remove')
        edit_button = Gtk.Button('Edit')
        close_button = Gtk.Button('Close')
        right_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        right_box.pack_start(add_host_button, False, False, 0)
        right_box.pack_start(add_group_button, False, False, 0)
        right_box.pack_start(remove_button, False, False, 0)
        right_box.pack_start(edit_button, False, False, 0)
        right_box.pack_start(close_button, False, False, 0)

        add_host_button.connect('clicked', self.__add_host)
        add_group_button.connect('clicked', self.__add_group)
        remove_button.connect('clicked', self.__remove)
        edit_button.connect('clicked', self.__edit)
        close_button.connect('clicked', self.__destroy_callback)

        main_grid = Gtk.Grid.new()
        main_grid.attach(self.__tree_view, 0, 0, 5, 1)
        main_grid.attach(right_box, 6, 0, 1, 1)

        box = self.get_content_area()
        box.add(main_grid)
        box.show_all()

    def __get_selection(self):
        _, selected = self.__tree_view.get_selection().get_selected()
        if selected is None:
            return

        depth = self.__store.iter_depth(selected)

        return selected, depth

    def __build_store(self):
        self.__store.clear()

        for group_name, hosts in self.__quick_menu.groups.items():
            parent = self.__store.append(None, [None, None, None, None, None, group_name])

            for host in hosts:
                self.__store.append(parent, [host.id, host.username, host.hostname, host.port, host.label, host.label or host.get_connection_string(self.__quick_menu.default_user)])

        if len(self.__quick_menu.groups) == 0:
            self.__store.append(None, ['No groups or hosts defined'])

        if self.__tree_view is not None:
            self.__tree_view.expand_all()

    def __remove(self, button):
        result = self.__get_selection()
        if result is None:
            return

        selection, depth = result

        # group
        if depth == 0:
            group_name = self.__store[selection][5]
            if group_name == '':
                return

            if self.__store.iter_has_child(selection):
                dialog = RmGroupConfirmDialog()
                result = dialog.run()
                dialog.destroy()
                if result == Gtk.ResponseType.CANCEL:
                    return

            self.__quick_menu.remove(group_name)
        # ssh entry
        elif depth == 1:
            group_name = self.__store[self.__store.iter_parent(selection)][5]
            host_id = self.__store[selection][0]
            self.__quick_menu.remove(group_name, host_id)

        self.__build_store()

    def __edit(self, button):
        result = self.__get_selection()
        if result is None:
            return

        selection, depth = result

        # group
        if depth == 0:
            group_name = self.__store[selection][5]
            if group_name == '':
                return
            dialog = GroupDialog(group_name)
            result = dialog.prompt()
            if result is None:
                return
            self.__quick_menu.edit_group(group_name, result)

        # ssh entry
        elif depth == 1:
            group_name = self.__store[self.__store.iter_parent(selection)][5]
            host = self.__store[selection]
            host_id = host[0]
            host_username = host[1]
            host_hostname = host[2]
            host_port = host[3]
            host_label = host[4]

            dialog = HostDialog(self.__quick_menu.groups.keys(), host_username, host_hostname, host_port, host_label, group_name)
            result = dialog.prompt()

            if result is None:
                return
            new_group_name, hostname, username, port, label = result
            self.__quick_menu.edit_host(group_name, new_group_name, host_id, username, hostname, port, label)

        self.__build_store()

    def __add_host(self, button):
        result = self.__get_selection()

        selection, depth = result

        dialog = HostDialog(self.__quick_menu.groups.keys(), selected_group=self.__store[selection][5] if depth == 0 else '')
        result = dialog.prompt()
        if not result:
            return

        group_name, hostname, username, port, label = result
        new_host = QuickSSHEntry(hostname, username, port, label)

        self.__quick_menu.add_host(group_name, new_host)
        self.__build_store()

    def __add_group(self, button):
        dialog = GroupDialog()
        result = dialog.prompt()
        if result is None:
            return

        self.__quick_menu.add_group(result)
        self.__build_store()

    def __destroy_callback(self, button):
        self.destroy()


