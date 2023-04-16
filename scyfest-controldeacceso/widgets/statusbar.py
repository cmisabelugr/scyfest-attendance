#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPL 2

Control de accesos app for SCYFEST 2023
Javier Sáez <jscoba@gmail.com>

"""
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg


class StatusBar(qtw.QWidget):

    visitors_text = "{} personas en recinto"

    def __init__(self):
        super().__init__()
        self.num_visitors = 0
        self.init_layout()
        


    def init_layout(self):
        self.layout = qtw.QHBoxLayout()
        self.name_label = qtw.QLabel("SCYFest: Control de accesos")
        self.visitors_counter = qtw.QLabel(self.visitors_text.format(self.num_visitors))

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.visitors_counter)
        self.layout.setAlignment(qtc.Qt.AlignCenter)
        self.setLayout(self.layout)