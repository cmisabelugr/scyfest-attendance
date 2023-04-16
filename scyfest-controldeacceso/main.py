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

        red_label = qtw.QLabel("Red")
        red_label.setStyleSheet(self.lbl_css + "background-color:red;")
        red_label.setAlignment(qtc.Qt.AlignCenter)
        blue_label = qtw.QLabel("Blue")
        blue_label.setStyleSheet(self.lbl_css + "background-color:blue;")
        blue_label.setAlignment(qtc.Qt.AlignCenter)
        green_label = qtw.QLabel("Green")
        green_label.setStyleSheet(self.lbl_css + "background-color:green;")
        green_label.setAlignment(qtc.Qt.AlignCenter)
        cyan_label = qtw.QLabel("Cyan")
        cyan_label.setAlignment(qtc.Qt.AlignCenter)
        cyan_label.setStyleSheet(
            self.lbl_css + "background-color:cyan; color: black;")
        magenta_label = qtw.QLabel("Magenta")
        magenta_label.setAlignment(qtc.Qt.AlignCenter)
        magenta_label.setStyleSheet(
            self.lbl_css + "background-color:magenta; color: black;")
        yellow_label = qtw.QLabel("Yellow")
        yellow_label.setAlignment(qtc.Qt.AlignCenter)
        yellow_label.setStyleSheet(
            self.lbl_css + "background-color:yellow; color: black;")

        self.layout.addWidget(red_label, 0, 0)
        self.layout.addWidget(green_label, 1, 0)
        self.layout.addWidget(blue_label, 2, 0)
        self.layout.addWidget(cyan_label, 0, 3)
        self.layout.addWidget(magenta_label, 1, 3)
        self.layout.addWidget(yellow_label, 2, 3)
        self.button = qtw.QLabel("Touch here<br/> to start the test")
        self.button.setTextFormat(qtc.Qt.RichText)
        self.button.setAlignment(qtc.Qt.AlignCenter)
        self.button.setStyleSheet(self.lbl_css + "background-color:black;")
        self.button.setSizePolicy(qtw.QSizePolicy.Expanding,
                                  qtw.QSizePolicy.Expanding)
        self.layout.addWidget(self.button, 0, 1, 3, 2)
        self.vbox = qtw.QVBoxLayout()
        self.statusbar = statusbar.StatusBar()
        self.vbox.addWidget(self.statusbar)
        #self.vbox.addChildLayout(self.layout)
        self.setLayout(self.vbox)
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
            if self.state == 0 and \
                    x > 300 and \
                    x < 900:
                self.state = 1
                self.button.setText("\
    Please touch the <br /><font color=\"red\">Red</font> square")
            # Red
            elif self.state == 1 and \
                    x < 300 and \
                    y < 235:
                self.state = 2
                self.button.setText("\
    Please touch the <br /><font color=\"green\">Green</font> square")
            elif self.state == 2 and \
                    x < 300 and \
                    y > 240 and \
                    y < 470:
                self.state = 3
                self.button.setText("\
    Please touch the <br /><font color=\"blue\">Blue</font> square")
            elif self.state == 3 and \
                    x < 300 and \
                    y > 470:
                self.state = 4
                self.button.setText("\
    Please touch the <br /><font color=\"cyan\">Cyan</font> square")
            elif self.state == 4 and \
                    x > 900 and \
                    y < 235:
                self.state = 5
                self.button.setText("\
    Please touch the <br /><font color=\"magenta\">Magenta</font> square")
            elif self.state == 5 and \
                    x > 900 and \
                    y > 240 and \
                    y < 470:
                self.state = 6
                self.button.setText("\
    Please touch the <br /><font color=\"yellow\">Yellow</font> square")
            elif self.state == 6 and \
                    x > 900 and \
                    y > 470:
                self.state = 7
                self.button.setText("\
    Please press the <br /><font color=\"white\">Mute Button</font>")
            elif self.state == 7:
                if self.mute_down:
                    self.state = 8
                    self.button.setText("\
        Please press the <br /><font color=\"white\">VolUp Button</font>")
            elif self.state == 8:
                self.button.setStyleSheet(
                    self.lbl_css + "background-color: LimeGreen;")
                self.button.setText("Test passed!")
                try:
                    pathlib.Path('/mnt/os/screen_test_passed').touch()
                    print("Starting uuid fresh")
                    os.remove("/mnt/os/uuid")
                    self.passed = True
                except:
                    print("Error while trying to touch the test passed file")

        return super().eventFilter(obj, event)


def main():
    app = qtw.QApplication(sys.argv)
    window = ControlAccesos(app)
    window.setAttribute(qtc.Qt.WA_AcceptTouchEvents, True)
    window.installEventFilter(window)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()