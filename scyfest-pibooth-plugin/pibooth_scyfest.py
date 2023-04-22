"""Plugin to implement the qr code management for scyfest."""

import pibooth
from pibooth.utils import LOGGER
from pibooth.view.background import Background, ARROW_BOTTOM, ARROW_HIDDEN, ARROW_TOP, ARROW_TOUCH
from pibooth.booth import PiApplication
from pibooth.plugins.hookspecs import hookspec
import requests
import pygame

BASE = "http://localhost:8000/booth/{}/{}"

__version__ = "1.0.0"

class QrPlugin(object):

    def __init__(self):
        self.last_qr = ""
        self.text = ""

@pibooth.hookimpl
def state_wait_enter(cfg, app, win):
    LOGGER.info("Hey from wait enter")


@pibooth.hookimpl
def state_wait_validate(cfg, app, win, events):
    LOGGER.info("Hey from wait validate")
    #Clear last qr scanned and validated
    return 'qr'


@pibooth.hookimpl(optionalhook=True)
def state_qr_enter(cfg, app, win):
    """When qr scan is entered"""
    win._update_background(QrBackground(win.arrow_location, win.arrow_offset))
    pass

@pibooth.hookimpl(optionalhook=True)
def state_qr_do(cfg, app, win, events):
    """Called while in qr screen with events"""
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(app.qrscan.text)
                app.qrscan.text = ''
            elif event.key == pygame.K_BACKSPACE:
                app.qrscan.text = app.qrscan.text[:-1]
            else:
                app.qrscan.text += event.unicode
    pass

@pibooth.hookimpl
def state_qr_validate(cfg, app, win, events):
    """Called every loop to see next step"""
    print("HOLAA")
    pass

@pibooth.hookimpl(optionalhook=True)
def state_qr_exit(cfg, app, win):
    """When qr scan is exited"""
    pass

@pibooth.hookimpl
def state_print_validate(app, win, events):
    printed = app.find_print_event(events)
    if printed:
        ## Decrease the booth points of the user.
        pass


class QrBackground(Background):

    def __init__(self, arrow_location=ARROW_BOTTOM, arrow_offset=0):
        Background.__init__(self, "Escanea tu código para empezar")
        self.arrow_location = arrow_location
        self.arrow_offset = arrow_offset
        self.left_arrow = None
        self.left_arrow_pos = None

    def resize(self, screen):
        Background.resize(self, screen)
        if self._need_update and self.arrow_location != ARROW_HIDDEN:
            if self.arrow_location == ARROW_TOUCH:
                size = (self._rect.width * 0.2, self._rect.height * 0.2)

                self.left_arrow = pibooth.pictures.get_pygame_image("camera.png", size, vflip=False, color=self._text_color)

                x = int(self._rect.width * 0.2)
                y = int(self._rect.height // 2)
            else:
                size = (self._rect.width * 0.3, self._rect.height * 0.3)

                vflip = True if self.arrow_location == ARROW_TOP else False
                self.left_arrow = pibooth.pictures.get_pygame_image("arrow.png", size, vflip=vflip, color=self._text_color)

                x = int(self._rect.left + self._rect.width // 4
                        - self.left_arrow.get_rect().width // 2)
                if self.arrow_location == ARROW_TOP:
                    y = self._rect.top + 10
                else:
                    y = int(self._rect.top + 2 * self._rect.height // 3)

            self.left_arrow_pos = (x - self.arrow_offset, y)

    def resize_texts(self):
        """Update text surfaces.
        """
        if self.arrow_location == ARROW_HIDDEN:
            rect = pygame.Rect(self._text_border, self._text_border,
                               self._rect.width / 2 - 2 * self._text_border,
                               self._rect.height - 2 * self._text_border)
            align = 'center'
        elif self.arrow_location == ARROW_BOTTOM:
            rect = pygame.Rect(self._text_border, self._text_border,
                               self._rect.width / 2 - 2 * self._text_border,
                               self._rect.height * 0.6 - self._text_border)
            align = 'bottom-center'
        elif self.arrow_location == ARROW_TOUCH:
            rect = pygame.Rect(self._text_border, self._text_border,
                               self._rect.width / 2 - 2 * self._text_border,
                               self._rect.height * 0.4 - self._text_border)
            align = 'bottom-center'
        else:
            rect = pygame.Rect(self._text_border, self._rect.height * 0.4,
                               self._rect.width / 2 - 2 * self._text_border,
                               self._rect.height * 0.6 - self._text_border)
            align = 'top-center'
        self._texts = []
        text = self._name
        if text:
            self._write_text(text, rect, align)

    def paint(self, screen):
        Background.paint(self, screen)
        if self.arrow_location != ARROW_HIDDEN:
            screen.blit(self.left_arrow, self.left_arrow_pos)

@pibooth.hookimpl
def pibooth_startup(cfg, app:PiApplication):
    app.qrscan = QrPlugin()
    print("Adding machine state qr")
    app._machine.add_state('qr')
    LOGGER.info("Hello from '%s' plugin", __name__)
    #app._pm.add_hook
    print(app._machine)