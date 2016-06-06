#!/usr/bin/env python3
import getpass
import os

from gi.repository import Gtk
from gi.repository import AppIndicator3

import subprocess
import json

from EditDialog import EditDialog
from QuickSSHEntry import QuickSSHEntry

QUICKSSH_FILE_PATH = os.path.expanduser('~/.quickssh')


class QuickSSH(object):
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new('QuickSSH', 'icon.jpg', AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_icon('icon.jpg')

        self.__main_menu = None

        try:
            self.__load()
        except:
            print('Failed to load configuration file ' + QUICKSSH_FILE_PATH + '. Please fix or remove it.')
            exit(1)
        self.construct_main_menu()

    @property
    def default_user(self):
        return self.__default_user or getpass.getuser()

    def __save(self):
        json_settings = {'default_user': self.__default_user}
        json_groups = {}

        for group, hosts in self.groups.items():
            json_groups[group] = []
            for host in hosts:
                json_groups[group].append(host.to_dict())

        json_content = [json_settings, json_groups]

        with open(QUICKSSH_FILE_PATH, 'w') as f:
            f.write(json.dumps(json_content))

    def __load(self):
        self.groups = {'': []}
        self.__default_user = None
        if not os.path.exists(QUICKSSH_FILE_PATH):
            return

        with open(QUICKSSH_FILE_PATH, 'r') as f:
            json_content = json.load(f)

        json_settings = json_content[0]
        json_groups = json_content[1]

        self.__default_user = json_settings.get('default_user', None)

        for group_name, hosts in json_groups.items():
            self.groups[group_name] = []

            for host in hosts:
                self.groups[group_name].append(
                    QuickSSHEntry(**host)
                )

    def construct_main_menu(self):
        self.__main_menu = Gtk.Menu()
        item = Gtk.MenuItem('QuickSSH')
        item.show()
        self.__main_menu.append(item)

        item = Gtk.SeparatorMenuItem()
        item.show()
        self.__main_menu.append(item)

        for group, hosts in self.groups.items():
            if group != '':
                submenu_item = Gtk.MenuItem(group)
                self.__main_menu.append(submenu_item)

                submenu = Gtk.Menu()
                submenu_item.set_submenu(submenu)
                submenu.show()

            for host in hosts:
                item = Gtk.MenuItem(host.label or host.get_connection_string(self.default_user))
                item.show()
                item.connect('activate', self.ssh_into, host)

                if group != '':
                    submenu_item.show()
                    submenu.append(item)
                else:
                    self.__main_menu.append(item)

        item = Gtk.SeparatorMenuItem()
        item.show()
        self.__main_menu.append(item)

        item = Gtk.MenuItem('Edit')
        item.show()
        item.connect('activate', self.show_edit_dialog)
        self.__main_menu.append(item)

        item = Gtk.MenuItem('Exit')
        item.show()
        item.connect('activate', self.quit)
        self.__main_menu.append(item)

        self.__main_menu.show()
        self.indicator.set_menu(self.__main_menu)

    def run(self):
        Gtk.main()

    def add_host(self, group, new_host):
        group = group or ''
        self.groups[group].append(new_host)
        self.__save()
        self.construct_main_menu()

    def remove(self, group, id_of_host_to_remove=None):
        if group not in self.groups:
            return

        if id_of_host_to_remove:
            for host in self.groups[group]:
                if host.id == id_of_host_to_remove:
                    self.groups[group].remove(host)
                    break
        else:
            del self.groups[group]

        self.__save()
        self.construct_main_menu()

    def add_group(self, group_name):
        self.groups[group_name] = []
        self.__save()

    def edit_group(self, old_name, new_name):
        if old_name not in self.groups:
            return

        self.groups[new_name] = self.groups[old_name]
        del self.groups[old_name]
        self.__save()
        self.construct_main_menu()

    def edit_host(self, group_name, new_group_name, host_id, new_username, new_hostname, new_port, new_label):
        if group_name not in self.groups:
            return

        for host in self.groups[group_name]:
            if host.id != host_id:
                continue

            host.username = new_username
            host.hostname = new_hostname
            host.port = new_port
            host.label = new_label

            if group_name == new_group_name:
                break

            self.groups[new_group_name].append(host)
            self.groups[group_name].remove(host)

            break

        self.__save()
        self.construct_main_menu()

    def ssh_into(self, entry, ssh_host):
        cmd = "gnome-terminal -e 'bash -c \"ssh -p " + (ssh_host.port or '22') + " " + ssh_host.get_user(self.default_user) + "@" + ssh_host.hostname + "; exec bash\"'"
        print('Executing', '"', cmd, '"')
        subprocess.Popen(cmd, shell=True)

    def show_edit_dialog(self, widget):
        dialog = EditDialog(self)
        dialog.show()

    @staticmethod
    def quit(widget):
        Gtk.main_quit()


if __name__ == '__main__':
    app = QuickSSH()
    app.run()
