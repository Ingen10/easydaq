# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'easydaq/config.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(240, 101)
        MainWindow.setMinimumSize(QtCore.QSize(240, 100))
        MainWindow.setMaximumSize(QtCore.QSize(250, 120))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setMinimumSize(QtCore.QSize(70, 27))
        self.connectButton.setMaximumSize(QtCore.QSize(70, 27))
        self.connectButton.setObjectName("connectButton")
        self.gridLayout.addWidget(self.connectButton, 2, 1, 1, 1)
        self.cbport = QtWidgets.QComboBox(self.centralwidget)
        self.cbport.setObjectName("cbport")
        self.gridLayout.addWidget(self.cbport, 1, 0, 1, 2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Configuration"))
        self.label.setText(_translate("MainWindow", "Select Serial Port: "))
        self.connectButton.setText(_translate("MainWindow", "Connect"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QDialog()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

