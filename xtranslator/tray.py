import sys
import os

from PySide2.QtWidgets import (QApplication, QWidget, QSystemTrayIcon, QLabel, QPushButton,
                               QMenu, QTextBrowser, QVBoxLayout, QGridLayout, QLineEdit, QMessageBox)
from PySide2.QtGui import QIcon
from PySide2.QtCore import QCoreApplication, QSettings
from PIL import ImageGrab
import numpy as np

# from xtranslator.recognition import imageToText
# from xtranslator.translator import get_translator
from xtranslator.constants import (ORGANIZATION_DOMAIN, ORGANIZATION_NAME,
                                   APPLICATION_NAME, SETTINGS_PATH_MODEL)


class WidgetPref(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)

        self._settings = QSettings()

        self._layout = QVBoxLayout()
        self._fields_layout = QGridLayout()

        self._path_title = QLabel('Path to model:')
        path_model = self._settings.value(SETTINGS_PATH_MODEL, '', type=str)
        self._path_model = QLineEdit(path_model)

        self.setLayout(self._layout)
        self._layout.addLayout(self._fields_layout)

        self._fields_layout.addWidget(self._path_title, 0, 0)
        self._fields_layout.addWidget(self._path_model, 0, 1)

        self._save_button = QPushButton('Save')
        self._save_button.pressed.connect(self.save)
        self._layout.addWidget(self._save_button)

    def save(self):
        self._settings.setValue(SETTINGS_PATH_MODEL, self._path_model.text())

    def closeEvent(self, event):
        self.hide()
        event.ignore()


class WidgetTranslator(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self._output = QTextBrowser()
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._output)

        self.setLayout(self._layout)

    def translate(self):
        path_model = QSettings().value(SETTINGS_PATH_MODEL, '')

        if not os.path.exists(path_model):
            QMessageBox.critical(self, 'Error', 'Model path is incorrect')
            return

        content_clip = ImageGrab.grabclipboard()
        if content_clip is None:
            QMessageBox.information(self, '', 'No images found in the buffer')
            return

        image = np.array(content_clip.convert('RGB'))
        # text = imageToText(image)
        # translator = get_translator(path_model)
        # translated = translator(text)
        translated = 'Test'
        self._output.setText(translated)

    def closeEvent(self, event):
        self.hide()
        event.ignore()


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)

        self._widget = WidgetTranslator()
        self._widget.resize(800, 600)

        self._prefs = WidgetPref()
        self._prefs.resize(800, 600)

        translate_action = menu.addAction("Translate image from clibpboard")
        translate_action.triggered.connect(self.translate)

        settings_action = menu.addAction('Settings')
        settings_action.triggered.connect(self._prefs.show)

        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.exit)

        self.setContextMenu(menu)

    def exit(self):
        QCoreApplication.quit()

    def translate(self):
        self._widget.translate()
        self._widget.show()


def main():
    QCoreApplication.setApplicationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    app = QApplication(sys.argv)

    w = QWidget()
    trayIcon = SystemTrayIcon(QIcon("./assets/icon.png"), w)

    trayIcon.show()
    sys.exit(app.exec_())