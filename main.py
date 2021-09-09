# -*- coding: utf-8 -*-#

import sys
import os

from PySide6.QtCore import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *
from PySide6.QtGui import *


import functions as fnc


class LoadParserForm(QMainWindow):

    def __init__(self, ui_file, parent=None):
        super(LoadParserForm, self).__init__(parent)
        ui_file = QFile(ui_file)

        if not ui_file.open(QIODevice.ReadOnly):
            print(f'Cannot open {ui_file}: {ui_file.errorString}')

        loader = QUiLoader()
        self.parser_window = loader.load(ui_file)

        if not self.parser_window:
            print(loader.errorString())
            sys.exit(-1)

        self.parser_window.show()


class ParseTxt(object):

    def __init__(self, obj=None, parent=None):
        # super(ParseTxt, self).__init__(parent)

        self.obj = obj
        self.widgets = tuple()
        self.main_menu = None
        self.file_source = None
        self.text_browser = None

    def _create_action(self):

        self.open_action = self.main_menu.addAction('Open File ...')
        self.close_file = self.main_menu.addAction('Close File ...')

        self.open_action.triggered.connect(self.open_file)

    def get_widgets(self):
        w = []
        for child in self.obj.children():
            if type(child) != QObject:
                w.append(child)
        self.widgets = tuple(w)

        # for widget in self.widgets:
        #     print(f'{widget}: {widget.objectName()}')

    def main_menu_actions(self):

        for widget in self.widgets:
            if widget.objectName() == 'menubar':
                self.main_menu = fnc.add_widget(self.obj, QMenu, 'mainMenu')
                self._create_action()

    def open_file(self):
        file_ = QFileDialog.getOpenFileName(self.obj, "Select File to Open",
                                               "\\", "Text file (*.txt);;"
                                                     "Csv file (*.csv);;"
                                                     "Data file (*.dat);;"
                                                     "Results file (*.res *.rez)")

        self.file_source = (
            os.path.split(file_[0])[0],
            os.path.split(file_[0])[1]
        )

        file_data = self._get_file_data()
        q_text_document = QTextDocument(file_data)

        for widget in self.widgets:
            if type(widget) == QDockWidget:
                self.text_browser = fnc.add_widget(widget, QTextBrowser, 'textBrowser')
                if self.text_browser:
                    print('Yes')
                    self.text_browser.setDocument(q_text_document)

    def _get_file_data(self):

        file_source =os.path.join(self.file_source[0], self.file_source[1])
        with open(file_source, 'r') as f:
            return f.read()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    parser_form = LoadParserForm('text_parsing_main_window.ui')
    parse_file = ParseTxt(parser_form.parser_window)

    parse_file.get_widgets()
    parse_file.main_menu_actions()

    sys.exit(app.exec())
