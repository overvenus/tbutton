#!/usr/bin/env python2
# coding:utf-8

__version__ = '0.1'

LOGO_DATA = """\
iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAQAAABIkb+zAAACPElEQVR4Ae3XA6xsRxzA4bk8u6
lt221s1bZt27Zt20EZ1LZt27rm1zjNuVst3nuT/L/Y+Y0nNUMIIYTgcSulnIFnrJ53ALxgnbwD
4FUbass5AN60mfacA+BdW+vIOQA+tIPOnAPgU7vqzjkAvrCXIucA+Mb+qjkHwPcOMXXOAfCTI0
2bcwD84jjT5xwAvzvZTDkHQI8zzJpzAPQ5JOeAHxygmmvATw41Va574BdHmSbXU+h3x5su13ug
x8lmyPUm7nOGmXN9Cw0412y5vkYHXWjOXP8Dwy4zT64/shFXmz/XP/Go6y2UcqHsFoulnChJWY
mAxkVABERABERABERABERABERABERABERABERABERABERABERABESADz3vXpc70mZWUEn/g6qD
vGLQoJcdoJKayVy2daU3Uol/NupNV9nGXOlfmc87/uot86RmMLfDvAKQSvxXLzvUnP84+u9AKa
FIjbGU241CwwEw4lZLppocpJb9U/0UzjYKTQuAUWfoShN4RS0vpXqpegyaHgAPqaQSg2rpT/Vy
Li0L4IzWB/zS0oAfU4mX1fJiqpcftdIPqcQBatk31cuZWum0VKLiLWVvKFK9FB7SKvfrThOYp5
TwhrlTI3Q7zYhmG3ayrlSTiv29pF+/F+2rSI2zmJsMa5ZhN1okTWrmcJAXjWvEuBccZPY0+ZjD
lq7wmhH/x4hXXW4Ls6cphcIyNnGoS9zlGe/7Ro8hY8YM6fGN9z3jTpc41CaWUaQQQgihBf4Eps
Cc6fXHDoQAAAAASUVORK5CYII="""

DEFAULT_CONFIG = """\
{
    "tbutton": {
        "hide": true
    },

    "commands": {
        "Pause vmware": "killall -s STOP vmware-vmx",
        "Continue vmware": "killall -s CONT vmware-vmx"
    }
}
"""

import sys
import os
import base64
import json
import threading

try:
    import pygtk
    pygtk.require('2.0')
    import gtk
except Exception:
    sys.exit(os.system(u'gdialog --title "TButton" --msgbox "\u8bf7\u5b89\u88c5 python-gtk2" 15 60'.encode(
        sys.getfilesystemencoding() or sys.getdefaultencoding(), 'replace')))
try:
    import pynotify
    pynotify.init('TButton')
except ImportError:
    pynotify = None
try:
    import appindicator
except ImportError:
    sys.exit(
        gtk.MessageDialog(
            None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, u'请安装 python appindicator').run())


class TButton:
    def __init__(self, window, config_dir='./.TButton', config_name='config.json'):
        self.config_dir = config_dir
        self.config_name = config_name

        # main window
        self.window = window
        self.window.set_size_request(652, 447)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect('delete-event', self.delete_event)

        # main box container
        self.box = gtk.HBox(False, 0)
        self.window.add(self.box)

        # add button
        self.add_button = gtk.Button('Add')
        self.add_button.connect('clicked', self.on_add_clicked)
        self.box.pack_start(self.add_button, True, True, 0)
        self.add_button.show()

        # remove button
        self.remove_button = gtk.Button('Remove')
        self.remove_button.connect('clicked', self.on_remove_clicked)
        self.box.pack_start(self.remove_button, True, True, 0)
        self.remove_button.show()

        self.window.connect('delete-event', lambda w, e: gtk.main_quit())

        # configures
        j = json.load(file(os.path.join(self.config_dir, self.config_name)))
        self.config = j['tbutton']
        self.commands = j['commands']

        # visible on setup?
        if not self.config['hide']:
            self.window.show_all()

        # logo
        self.logo_path = os.path.join(self.config_dir, 'tbutton-logo.png')
        if not os.path.isfile(self.logo_path):
            with open(self.logo_path, 'wb') as fp:
                fp.write(base64.b64decode(LOGO_DATA))
        self.window.set_icon_from_file(self.logo_path)

        # tray
        self.tray = appindicator.Indicator('TButton', 'indicator-messages',
                                               appindicator.CATEGORY_APPLICATION_STATUS)
        self.tray.set_status(appindicator.STATUS_ACTIVE)
        self.tray.set_attention_icon('indicator-messages-new')
        self.tray.set_icon(self.logo_path)
        self.tray.set_menu(self.make_menu())

    def make_menu(self):
        menu = gtk.Menu()

        for k, v in self.commands.iteritems():
            item = gtk.MenuItem(k)
            item.connect('activate', self.on_menu_item_activate, v)
            item.show()
            menu.append(item)

        specialitem = list()
        specialitem.append((u'显示', self.on_show))
        specialitem.append((u'隐藏', self.on_hide))
        specialitem.append((u'退出', self.on_quit))

        for text, callback in specialitem:
            item = gtk.MenuItem(text)
            item.connect('activate', callback)
            item.show()
            menu.append(item)

        menu.show()
        return menu

    def on_menu_item_activate(self, widget, data=None):
        if data:
            self.exec_command(data)
            message = u'%s executed' % widget.get_label()
            self.show_notify(message, 3)

    @staticmethod
    def exec_command(cmd):
        if cmd == '':
            return

        def wrap():
            os.system(cmd)
            # os.system(u'gdialog --title "TButton" --msgbox "%s" 15 60' % cmd)

        # running in a new thread.
        try:
            threading.Thread(target=wrap).start()
        except RuntimeError:
            pass

        print('exec_command stub: %s' % cmd)

    def show_notify(self, message=None, timeout=None):
        if pynotify and message:
            notification = pynotify.Notification('TButton', message, icon=self.logo_path)
            notification.set_hint('x', 200)
            notification.set_hint('y', 400)
            if timeout:
                notification.set_timeout(timeout * 1000)  # make it ms
            notification.show()

    def on_add_clicked(self, widget, data=None):
        print('add_command stub')

    def on_remove_clicked(self, widget, data=None):
        print('remove_command stub')

    def on_show(self, widget, data=None):
        self.window.show_all()
        self.window.present()
        print('on_show')

    def on_hide(self, widget, data=None):
        self.window.hide_all()
        print('on_hide')

    def delete_event(self, widget, data=None):
        self.on_hide(widget, data)
        # 默认最小化至托盘
        return True

    def on_quit(self, widget, data=None):
        gtk.main_quit()


def main():
    # create config dir
    config_dir = os.environ['HOME'] + '/.config/TButton'
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    # dump default config.json
    config_name = 'config.json'
    filename = os.path.join(config_dir, config_name)
    if not os.path.exists(filename):
        with open(filename, 'w') as fp:
            fp.write(DEFAULT_CONFIG)
        os.chmod(filename, 0755)

    window = gtk.Window()
    TButton(window, config_dir, config_name)
    gtk.gdk.threads_init()  # allow multiple threads to serialize access
                            # to the Python interpreter
    gtk.main()


if __name__ == '__main__':
    main()
