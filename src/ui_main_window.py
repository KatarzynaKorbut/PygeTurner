# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QTextBrowser, QToolBar,
    QVBoxLayout, QWidget)

from audio_player import AudioPlayer
from sheet_viewer import SheetViewer
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1037, 768)
        self.open_sheet = QAction(MainWindow)
        self.open_sheet.setObjectName(u"open_sheet")
        self.open_sound = QAction(MainWindow)
        self.open_sound.setObjectName(u"open_sound")
        self.open_sound.setEnabled(False)
        self.set_musescore_path = QAction(MainWindow)
        self.set_musescore_path.setObjectName(u"set_musescore_path")
        self.main_area = QWidget(MainWindow)
        self.main_area.setObjectName(u"main_area")
        self.main_area.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.main_area)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.sheet_view = SheetViewer(self.main_area)
        self.sheet_view.setObjectName(u"sheet_view")
        self.sheet_view.setStyleSheet(u"background:transparent")
        self.sheet_view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.sheet_view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self.verticalLayout.addWidget(self.sheet_view)

        self.audio_player = AudioPlayer(self.main_area)
        self.audio_player.setObjectName(u"audio_player")

        self.verticalLayout.addWidget(self.audio_player)

        self.results_textbox = QTextBrowser(self.main_area)
        self.results_textbox.setObjectName(u"results_textbox")

        self.verticalLayout.addWidget(self.results_textbox)

        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(2, 2)
        MainWindow.setCentralWidget(self.main_area)
        self.menu_bar = QMenuBar(MainWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 1037, 21))
        self.file_menu = QMenu(self.menu_bar)
        self.file_menu.setObjectName(u"file_menu")
        MainWindow.setMenuBar(self.menu_bar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menu_bar.addAction(self.file_menu.menuAction())
        self.file_menu.addAction(self.open_sheet)
        self.file_menu.addAction(self.open_sound)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.set_musescore_path)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PygeTurner", None))
        self.open_sheet.setText(QCoreApplication.translate("MainWindow", u"Otw\u00f3rz &nuty", None))
        self.open_sound.setText(QCoreApplication.translate("MainWindow", u"Otw\u00f3rz &d\u017awi\u0119k", None))
        self.set_musescore_path.setText(QCoreApplication.translate("MainWindow", u"Ustaw \u015bcie\u017ck\u0119 do MuseScore", None))
        self.file_menu.setTitle(QCoreApplication.translate("MainWindow", u"&Plik", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

