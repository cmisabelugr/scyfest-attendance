#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPL 2

Control de accesos app for SCYFEST 2023
Javier Sáez <jscoba@gmail.com>

"""
import os
import pathlib
import platform
import signal
import struct
import sys
import time
import threading
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

from widgets import statusbar

signal.signal(signal.SIGINT, signal.SIG_DFL)

HEIGHT = 720
WIDTH = 1280

if platform.machine() != 'x86_64':
    os.environ["QT_QPA_EVDEV_TOUCHSCREEN_PARAMETERS"] = "/dev/input/event1:rotate=90:invertx:inverty"
    os.environ["QT_QPA_PLATFORM"] = "linuxfb:tty=/dev/fb0:rotation=90"
    os.environ["QT_QPA_FONTDIR"] = "/usr/share/fonts/dejavu/"


class Color(qtw.QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(qtg.QPalette.Window, qtg.QColor(color))
        self.setPalette(palette)


class Worker(qtc.QThread):
    """ Reads from the kernel input file """
    inputn = '4'
    codes = {
        114: "vol_down",
        115: "vol_up",
        113: "mute"
    }
    eformat = "llHHI"
    pressed = qtc.pyqtSignal(str)

    def run(self):
        print("Event worker running")
        infile_path = '/dev/input/event' + self.inputn
        self.in_file = open(infile_path, 'rb')
        event_size = struct.calcsize(self.eformat)
        event = self.in_file.read(event_size)
        while event:
            (tv_sec, tv_usec, etype, code, value) = struct.unpack(
                self.eformat, event)
            if etype != 0 or code != 0 or value != 0:
                if code in self.codes and value == 1:
                    print(f"Detected down event for {self.codes[code]} key: {tv_sec}.{tv_usec}")
                    if self.codes[code] == "vol_down":
                        self.pressed.emit("vol_down")
                    elif self.codes[code] == "vol_up":
                        self.pressed.emit("vol_up")
                    elif self.codes[code] == "mute":
                        self.pressed.emit("mute")
            event = self.in_file.read(event_size)
        self.in_file.close()


class Exiter(threading.Thread):
    def __init__(self, app):
        self.app = app
        super().__init__()

    def run(self, *args, **kwargs):
        time.sleep(1)
        self.app.quit()


class ControlAccesos(qtw.QWidget):
    """ Test window """
    lbl_css = """
    border-radius:5px;
    color: white;
    font-size: 48px;
    font-weight: 600;
    padding: 20px;
    """

    def __init__(self, app):
        super().__init__()
        self.setFixedHeight(HEIGHT)
        self.setFixedWidth(WIDTH)
        self.layout = qtw.QGridLayout()
        self.app = app
        self.state = 0
        self.passed = False
        self.in_file = None
        self.mute_down = False
        self.vol_down_down = False
        self.vol_up_down = False

        self.worker = Worker()
        self.worker.pressed.connect(self.button_pressed)
        #self.worker.start()

        self.button = qtw.QLabel("Pulsa aquí para<br/> imprimir un ticket")
        self.button.setTextFormat(qtc.Qt.RichText)
        self.button.setAlignment(qtc.Qt.AlignCenter)
        self.button.setStyleSheet(self.lbl_css + "background-color:black;")
        self.button.setSizePolicy(qtw.QSizePolicy.Expanding,
                                  qtw.QSizePolicy.Expanding)
        self.layout.addWidget(self.button, 0, 1, 3, 2)
        self.setLayout(self.layout)
        self.show()


    def button_pressed(self, button: str):
        """ What to do when the button is pressed """
        print("Button pressed signal received: %s" % button)
        if button == "vol_down":
            self.vol_down_down = True
            self.eventFilter(None, None)
        elif button == "vol_up":
            self.vol_up_down = True
            self.eventFilter(None, None)
        elif button == "mute":
            self.mute_down = True
            self.eventFilter(None, None)

    def eventFilter(self, obj, event):
        """ Manages window events """
        x = None
        y = None
        if self.passed:
            t = Exiter(self.app)
            t.start()
            self.passed = False
        if (not obj and not event) or \
                event.type() == qtc.QEvent.MouseButtonPress:
            if event:
                x = event.pos().x()
                y = event.pos().y()
                print("Event position: X: %s, Y: %s" % (x, y))
            else:
                x = 0
                y = 0

            # Start position
            os.popen("rm /tmp/ticket.pdf").read()
            os.popen("curl localhost:8000/generate_one --output /tmp/ticket.pdf").read()
            os.popen("pdf2ps /tmp/ticket.pdf /tmp/ticket.ps").read()
            os.popen("lp -d QL-600 /tmp/ticket.ps").read()
                

        return super().eventFilter(obj, event)


def main():
    app = qtw.QApplication(sys.argv)
    window = ControlAccesos(app)
    window.setAttribute(qtc.Qt.WA_AcceptTouchEvents, True)
    window.installEventFilter(window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()