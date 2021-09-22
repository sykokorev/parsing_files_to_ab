# -*- coding: utf-8 -*- #

import sys
import os

from PySide6.QtCore import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import functions as fnc


def get_text(obj):
    text = obj.textCursor().selectedText()
    text = text.strip()
    return text


def change_text_background_color(obj, color=Qt.yellow):
    color = QColor(color)
    obj.setTextBackgroundColor(color)


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

        self.obj = obj
        self.widgets = tuple()
        self.main_menu = None
        self.file_source = None
        self.text_browser = None
        self.variables = {}

    def _widgets_initial_states(self):

        for widget in self.widgets:
            if type(widget) == QDockWidget:
                widget.hide()

    def _create_action(self):

        self.open_action = self.main_menu.addAction('Open File ...')
        self.open_action.triggered.connect(self.open_file)

        self.close_action = self.main_menu.addAction('Close File ...')
        self.close_action.triggered.connect(self.close_file)

    def _get_file_data(self):

        file_source = os.path.join(self.file_source[0], self.file_source[1])

        try:
            with open(file_source, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return False

    def get_widgets(self):
        w = []
        for child in self.obj.children():
            if type(child) != QObject:
                w.append(child)
        self.widgets = tuple(w)

        for widget in self.widgets:
            if type(widget) == QDockWidget and \
                    widget.objectName() == 'dockWidgetText':
                self.text_browser = fnc.add_widget(
                    widget,
                    QTextBrowser, 'textBrowser'
                )

        self._widgets_initial_states()

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

        if file_data:
            q_text_document = QTextDocument(file_data)
            for widget in self.widgets:
                if type(widget) == QDockWidget and \
                        widget.objectName() == 'dockWidgetText':
                    widget.show()
                    if self.text_browser:
                        self.text_browser.clear()
                        self.text_browser.setDocument(q_text_document)
                        self.text_browser.setContextMenuPolicy(
                            Qt.CustomContextMenu)
                        self.text_browser.setSearchPaths(['1', '2'])
                        self.text_browser.customContextMenuRequested.\
                            connect(self.add_variable)

    def close_file(self):

        for widget in self.widgets:
            if type(widget) == QDockWidget:
                widget.hide()
                if self.text_browser:
                    self.text_browser.clear()

    def add_variable(self):

        menu = QMenu(self.text_browser)
        add_num_var = menu.addAction("Add numerical variable...")
        add_str_var = menu.addAction("Add string variable...")
        action = menu.exec(QCursor.pos())

        msg = QInputDialog()
        msg.setLabelText("Input variable name")
        msg.setOkButtonText("Add")
        msg.setWindowTitle("Add variable")

        if action == add_num_var:
            if msg.exec():
                text = get_text(self.text_browser)
                try:
                    text = float(text)
                    self.variables[msg.textValue()] = text
                    change_text_background_color(self.text_browser)
                except (ValueError, TypeError):
                    err_title = 'TypeError'
                    err_text = 'Unavailable data type for numerical data. ' \
                               'Do you want ddd variable as a string value?'
                    err_msg = QMessageBox().question(self.text_browser,
                                                     err_title, err_text,
                                                     QMessageBox.StandardButton.Ok,
                                                     QMessageBox.StandardButton.Cancel)
                    if err_msg == 1024:
                        change_text_background_color(self.text_browser, Qt.magenta)
                        self.variables[msg.textValue()] = text

        elif action == add_str_var:
            if msg.exec():
                text = get_text(self.text_browser)
                change_text_background_color(self.text_browser, Qt.magenta)
                self.variables[msg.textValue()] = text

        print(self.variables)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    parser_form = LoadParserForm('text_parsing_main_window.ui')
    parse_file = ParseTxt(parser_form.parser_window)

    parse_file.get_widgets()
    parse_file.main_menu_actions()

    sys.exit(app.exec())
