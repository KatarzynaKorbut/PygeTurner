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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QScrollArea,
    QSizePolicy, QSlider, QToolBar, QToolButton,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1037, 768)
        self.actionPlay = QAction(MainWindow)
        self.actionPlay.setObjectName(u"actionPlay")
        icon = QIcon()
        icon.addFile(u":/icons/feather icons/play.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionPlay.setIcon(icon)
        self.open_sheet = QAction(MainWindow)
        self.open_sheet.setObjectName(u"open_sheet")
        self.open_sound = QAction(MainWindow)
        self.open_sound.setObjectName(u"open_sound")
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        self.styleSheet.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.styleSheet)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.sheet_view = QGraphicsView(self.styleSheet)
        self.sheet_view.setObjectName(u"sheet_view")
        self.sheet_view.setStyleSheet(u"background:transparent")
        self.sheet_view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.sheet_view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self.verticalLayout.addWidget(self.sheet_view)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.play_pause_button = QToolButton(self.styleSheet)
        self.play_pause_button.setObjectName(u"play_pause_button")
        self.play_pause_button.setEnabled(False)
        icon1 = QIcon(QIcon.fromTheme(u"media-playback-start"))
        self.play_pause_button.setIcon(icon1)
        self.play_pause_button.setCheckable(True)

        self.horizontalLayout.addWidget(self.play_pause_button)

        self.time_slider = QSlider(self.styleSheet)
        self.time_slider.setObjectName(u"time_slider")
        self.time_slider.setEnabled(False)
        self.time_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.time_slider)

        self.time_label = QLabel(self.styleSheet)
        self.time_label.setObjectName(u"time_label")

        self.horizontalLayout.addWidget(self.time_label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.widget = QWidget(self.styleSheet)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.scrollArea_2 = QScrollArea(self.widget)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 496, 150))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.horizontalLayout_2.addWidget(self.scrollArea_2)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_4 = QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        self.horizontalLayout_2.addWidget(self.widget_3)


        self.verticalLayout.addWidget(self.widget)

        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(2, 1)
        MainWindow.setCentralWidget(self.styleSheet)
        self.menu_bar = QMenuBar(MainWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 1037, 22))
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

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PygeTurner", None))
        self.actionPlay.setText(QCoreApplication.translate("MainWindow", u"Play", None))
#if QT_CONFIG(shortcut)
        self.actionPlay.setShortcut(QCoreApplication.translate("MainWindow", u"P", None))
#endif // QT_CONFIG(shortcut)
        self.open_sheet.setText(QCoreApplication.translate("MainWindow", u"Otw\u00f3rz nuty", None))
        self.open_sound.setText(QCoreApplication.translate("MainWindow", u"Otw\u00f3rz d\u017awi\u0119k", None))
        self.time_label.setText(QCoreApplication.translate("MainWindow", u"00:00:00 / 00:00:00", None))
        self.file_menu.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi
