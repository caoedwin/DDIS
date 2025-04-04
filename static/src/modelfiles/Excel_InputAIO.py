# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Excel_InputAIO.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMessageBox
# from PyQt5.QtGui import QIcon
# from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from Progress import MyWindow, UI_Progress
# import pandas as pd
# import pprint
# from pathlib import Path
# import os
# import numpy as np

# import pandas as pd
# import pprint
# from pathlib import Path
# import os
# import numpy as np

class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(863, 752)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("QFrame {    background-color: rgb(56, 58, 89);    \n"
                                 "    color: rgb(220, 220, 220);\n"
                                 "    border-radius: 10px;\n"
                                 "}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 120))
        self.label_3.setStyleSheet("font: 28pt \"楷体\";\n"
                                   "color: rgb(255, 170, 255);\n"
                                   "font-weight:bold;\n"
                                   "text-align:center;")
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 7, QtCore.Qt.AlignHCenter)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setMinimumSize(QtCore.QSize(180, 60))
        self.label_5.setMaximumSize(QtCore.QSize(180, 60))
        self.label_5.setStyleSheet("font: 9pt \"楷体\";\n"
                                   "color: rgb(255, 255, 127);\n"
                                   "font-weight:bold;")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 8, 1, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line_2.setStyleSheet("background-color: rgb(85, 255, 255);")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 10, 0, 1, 7)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMinimumSize(QtCore.QSize(0, 60))
        self.label.setMaximumSize(QtCore.QSize(16777215, 60))
        self.label.setStyleSheet("font: 14pt \"楷体\";\n"
                                 "color: rgb(0, 255, 255);\n"
                                 "font-weight:bold;")
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line.setStyleSheet("background-color: rgb(85, 255, 255);")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 3, 0, 1, 7)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setMinimumSize(QtCore.QSize(60, 60))
        self.label_4.setMaximumSize(QtCore.QSize(100, 60))
        self.label_4.setStyleSheet("font: 9pt \"楷体\";\n"
                                   "color: rgb(0, 255, 255);\n"
                                   "font-weight:bold;")
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 8, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 140))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 140))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.radioButton_5 = QtWidgets.QRadioButton(self.frame_2)
        self.radioButton_5.setMinimumSize(QtCore.QSize(0, 80))
        self.radioButton_5.setStyleSheet("font: 11pt \"楷体\";\n"
                                         "color: rgb(255, 255, 255);")
        self.radioButton_5.setObjectName("radioButton_5")
        self.gridLayout_3.addWidget(self.radioButton_5, 0, 0, 1, 1)
        self.radioButton = QtWidgets.QRadioButton(self.frame_2)
        self.radioButton.setMinimumSize(QtCore.QSize(0, 80))
        self.radioButton.setStyleSheet("font: 11pt \"楷体\";\n"
                                       "color: rgb(255, 255, 255);")
        self.radioButton.setObjectName("radioButton")
        self.gridLayout_3.addWidget(self.radioButton, 0, 1, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 5, 0, 1, 7)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 140))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 150))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.radioButton_2 = QtWidgets.QRadioButton(self.frame_3)
        self.radioButton_2.setMinimumSize(QtCore.QSize(0, 80))
        self.radioButton_2.setStyleSheet("font: 11pt \"楷体\";\n"
                                         "color: rgb(255, 255, 255);")
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout_4.addWidget(self.radioButton_2, 0, 2, 1, 1)
        self.radioButton_4 = QtWidgets.QRadioButton(self.frame_3)
        self.radioButton_4.setMinimumSize(QtCore.QSize(0, 80))
        self.radioButton_4.setStyleSheet("font: 11pt \"楷体\";\n"
                                         "color: rgb(255, 255, 255);")
        self.radioButton_4.setObjectName("radioButton_4")
        self.gridLayout_4.addWidget(self.radioButton_4, 0, 1, 1, 1)
        self.radioButton_3 = QtWidgets.QRadioButton(self.frame_3)
        self.radioButton_3.setMinimumSize(QtCore.QSize(0, 80))
        self.radioButton_3.setStyleSheet("font: 11pt \"楷体\";\n"
                                         "color: rgb(255, 255, 255);")
        self.radioButton_3.setObjectName("radioButton_3")
        self.gridLayout_4.addWidget(self.radioButton_3, 0, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_3, 7, 0, 1, 7)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setStyleSheet("font: 9pt \"楷体\";")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 9, 6, 1, 1, QtCore.Qt.AlignRight)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(0, 60))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 60))
        self.label_2.setStyleSheet("font: 14pt \"楷体\";\n"
                                   "color: rgb(0, 255, 255);\n"
                                   "font-weight:bold;")
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 6, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setStyleSheet("font: 9pt \"楷体\";\n"
                                   "color: rgb(0, 255, 255);")
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 11, 0, 1, 7, QtCore.Qt.AlignHCenter)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 863, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionexit = QtWidgets.QAction(MainWindow)
        self.actionexit.setObjectName("actionexit")
        # self.menu.addAction(self.actionexit)
        # self.menubar.addAction(self.menu.menuAction())
        #
        # self.retranslateUi(MainWindow)
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.action = QAction('退出(&X)')  # 定义一个Action即动作
        self.action.setStatusTip('Exit application')  # 状态栏信息
        self.action.triggered.connect(MainWindow.close)  # 触发事件动作为"关闭窗口"
        self.action.setShortcut('Ctrl+Q')  # 快捷键设置
        # self.statusBar()  # 状态栏信

        self.menu.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "模板选择"))
        self.label.setText(_translate("MainWindow", "请选择客户别："))
        self.label_4.setText(_translate("MainWindow", "运行状态："))
        self.radioButton_5.setText(_translate("MainWindow", "C38(AIO)"))
        self.radioButton.setText(_translate("MainWindow", "T88(AIO)"))
        self.radioButton_2.setText(_translate("MainWindow", "EELP+"))
        self.radioButton_4.setText(_translate("MainWindow", "C(SIT)"))
        self.radioButton_3.setText(_translate("MainWindow", "B(SDV)"))
        self.pushButton.setText(_translate("MainWindow", "确认"))
        self.label_2.setText(_translate("MainWindow", "请选择Phase："))
        self.label_6.setText(_translate("MainWindow", "DDIS Ecel转换工具-AIO    版本：V1.0    开发者：DQA Auto Team"))
        self.menu.setTitle(_translate("MainWindow", "选项"))
        self.actionexit.setText(_translate("MainWindow", "exit"))
