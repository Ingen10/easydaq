# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'easydaq/configwave.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(260, 213)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(260, 0))
        MainWindow.setMaximumSize(QtCore.QSize(260, 260))
        self.formLayout = QtGui.QFormLayout(MainWindow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(100, 27))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.cBmode = QtGui.QComboBox(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cBmode.sizePolicy().hasHeightForWidth())
        self.cBmode.setSizePolicy(sizePolicy)
        self.cBmode.setMinimumSize(QtCore.QSize(130, 27))
        self.cBmode.setMaximumSize(QtCore.QSize(120, 27))
        self.cBmode.setObjectName(_fromUtf8("cBmode"))
        self.cBmode.addItem(_fromUtf8(""))
        self.cBmode.addItem(_fromUtf8(""))
        self.cBmode.addItem(_fromUtf8(""))
        self.cBmode.addItem(_fromUtf8(""))
        self.cBmode.addItem(_fromUtf8(""))
        self.cBmode.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cBmode)
        self.sWDC = QtGui.QStackedWidget(MainWindow)
        self.sWDC.setMinimumSize(QtCore.QSize(100, 27))
        self.sWDC.setObjectName(_fromUtf8("sWDC"))
        self.page_21 = QtGui.QWidget()
        self.page_21.setObjectName(_fromUtf8("page_21"))
        self.label_4 = QtGui.QLabel(self.page_21)
        self.label_4.setGeometry(QtCore.QRect(0, 0, 100, 27))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(100, 27))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.sWDC.addWidget(self.page_21)
        self.page_22 = QtGui.QWidget()
        self.page_22.setObjectName(_fromUtf8("page_22"))
        self.label_2 = QtGui.QLabel(self.page_22)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 100, 27))
        self.label_2.setMinimumSize(QtCore.QSize(100, 27))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.sWDC.addWidget(self.page_22)
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.sWDC)
        self.sWDC2 = QtGui.QStackedWidget(MainWindow)
        self.sWDC2.setObjectName(_fromUtf8("sWDC2"))
        self.page_23 = QtGui.QWidget()
        self.page_23.setObjectName(_fromUtf8("page_23"))
        self.sBoffset = QtGui.QDoubleSpinBox(self.page_23)
        self.sBoffset.setGeometry(QtCore.QRect(0, 0, 130, 27))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sBoffset.sizePolicy().hasHeightForWidth())
        self.sBoffset.setSizePolicy(sizePolicy)
        self.sBoffset.setMinimumSize(QtCore.QSize(130, 27))
        self.sBoffset.setDecimals(3)
        self.sBoffset.setMinimum(-4.0)
        self.sBoffset.setMaximum(4.0)
        self.sBoffset.setSingleStep(0.1)
        self.sBoffset.setProperty("value", 0.0)
        self.sBoffset.setObjectName(_fromUtf8("sBoffset"))
        self.sWDC2.addWidget(self.page_23)
        self.page_24 = QtGui.QWidget()
        self.page_24.setObjectName(_fromUtf8("page_24"))
        self.Bchoose = QtGui.QPushButton(self.page_24)
        self.Bchoose.setGeometry(QtCore.QRect(0, 0, 130, 27))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Bchoose.sizePolicy().hasHeightForWidth())
        self.Bchoose.setSizePolicy(sizePolicy)
        self.Bchoose.setMinimumSize(QtCore.QSize(130, 27))
        self.Bchoose.setObjectName(_fromUtf8("Bchoose"))
        self.sWDC2.addWidget(self.page_24)
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.sWDC2)
        self.sWamp1 = QtGui.QStackedWidget(MainWindow)
        self.sWamp1.setMinimumSize(QtCore.QSize(100, 27))
        self.sWamp1.setObjectName(_fromUtf8("sWamp1"))
        self.page_17 = QtGui.QWidget()
        self.page_17.setObjectName(_fromUtf8("page_17"))
        self.lb_amplitude = QtGui.QLabel(self.page_17)
        self.lb_amplitude.setGeometry(QtCore.QRect(0, 0, 100, 27))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_amplitude.sizePolicy().hasHeightForWidth())
        self.lb_amplitude.setSizePolicy(sizePolicy)
        self.lb_amplitude.setMinimumSize(QtCore.QSize(100, 27))
        self.lb_amplitude.setObjectName(_fromUtf8("lb_amplitude"))
        self.sWamp1.addWidget(self.page_17)
        self.page_18 = QtGui.QWidget()
        self.page_18.setObjectName(_fromUtf8("page_18"))
        self.sWamp1.addWidget(self.page_18)
        self.page_26 = QtGui.QWidget()
        self.page_26.setObjectName(_fromUtf8("page_26"))
        self.sWamp1.addWidget(self.page_26)
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.sWamp1)
        self.sWamp2 = QtGui.QStackedWidget(MainWindow)
        self.sWamp2.setObjectName(_fromUtf8("sWamp2"))
        self.page_19 = QtGui.QWidget()
        self.page_19.setObjectName(_fromUtf8("page_19"))
        self.sBamplitude = QtGui.QDoubleSpinBox(self.page_19)
        self.sBamplitude.setGeometry(QtCore.QRect(0, 0, 130, 27))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sBamplitude.sizePolicy().hasHeightForWidth())
        self.sBamplitude.setSizePolicy(sizePolicy)
        self.sBamplitude.setMinimumSize(QtCore.QSize(130, 27))
        self.sBamplitude.setDecimals(3)
        self.sBamplitude.setMaximum(8.0)
        self.sBamplitude.setSingleStep(0.1)
        self.sBamplitude.setProperty("value", 1.0)
        self.sBamplitude.setObjectName(_fromUtf8("sBamplitude"))
        self.sWamp2.addWidget(self.page_19)
        self.page_20 = QtGui.QWidget()
        self.page_20.setObjectName(_fromUtf8("page_20"))
        self.sWamp2.addWidget(self.page_20)
        self.page_25 = QtGui.QWidget()
        self.page_25.setObjectName(_fromUtf8("page_25"))
        self.lb_namefile = QtGui.QLabel(self.page_25)
        self.lb_namefile.setGeometry(QtCore.QRect(0, 0, 130, 27))
        self.lb_namefile.setMinimumSize(QtCore.QSize(130, 27))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lb_namefile.setFont(font)
        self.lb_namefile.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_namefile.setObjectName(_fromUtf8("lb_namefile"))
        self.sWamp2.addWidget(self.page_25)
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.sWamp2)
        self.sWperiod1 = QtGui.QStackedWidget(MainWindow)
        self.sWperiod1.setMinimumSize(QtCore.QSize(100, 27))
        self.sWperiod1.setObjectName(_fromUtf8("sWperiod1"))
        self.page_13 = QtGui.QWidget()
        self.page_13.setObjectName(_fromUtf8("page_13"))
        self.lb_period = QtGui.QLabel(self.page_13)
        self.lb_period.setGeometry(QtCore.QRect(0, 0, 100, 27))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_period.sizePolicy().hasHeightForWidth())
        self.lb_period.setSizePolicy(sizePolicy)
        self.lb_period.setMinimumSize(QtCore.QSize(100, 27))
        self.lb_period.setObjectName(_fromUtf8("lb_period"))
        self.sWperiod1.addWidget(self.page_13)
        self.page_14 = QtGui.QWidget()
        self.page_14.setObjectName(_fromUtf8("page_14"))
        self.sWperiod1.addWidget(self.page_14)
        self.page_27 = QtGui.QWidget()
        self.page_27.setObjectName(_fromUtf8("page_27"))
        self.sWperiod1.addWidget(self.page_27)
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.sWperiod1)
        self.sWperiod2 = QtGui.QStackedWidget(MainWindow)
        self.sWperiod2.setMinimumSize(QtCore.QSize(100, 27))
        self.sWperiod2.setObjectName(_fromUtf8("sWperiod2"))
        self.page_15 = QtGui.QWidget()
        self.page_15.setObjectName(_fromUtf8("page_15"))
        self.sBperiodms = QtGui.QDoubleSpinBox(self.page_15)
        self.sBperiodms.setGeometry(QtCore.QRect(0, 0, 130, 27))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sBperiodms.sizePolicy().hasHeightForWidth())
        self.sBperiodms.setSizePolicy(sizePolicy)
        self.sBperiodms.setMinimumSize(QtCore.QSize(130, 27))
        self.sBperiodms.setDecimals(3)
        self.sBperiodms.setMinimum(1.0)
        self.sBperiodms.setMaximum(65536.0)
        self.sBperiodms.setSingleStep(0.1)
        self.sBperiodms.setProperty("value", 200.0)
        self.sBperiodms.setObjectName(_fromUtf8("sBperiodms"))
        self.sWperiod2.addWidget(self.page_15)
        self.page_16 = QtGui.QWidget()
        self.page_16.setObjectName(_fromUtf8("page_16"))
        self.sWperiod2.addWidget(self.page_16)
        self.page_28 = QtGui.QWidget()
        self.page_28.setObjectName(_fromUtf8("page_28"))
        self.sWperiod2.addWidget(self.page_28)
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.sWperiod2)
        self.stackedWidget = QtGui.QStackedWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QtCore.QSize(100, 30))
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.label_6 = QtGui.QLabel(self.page)
        self.label_6.setGeometry(QtCore.QRect(0, 0, 100, 27))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(100, 27))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.label_5 = QtGui.QLabel(self.page_2)
        self.label_5.setGeometry(QtCore.QRect(0, 0, 100, 27))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(100, 27))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.stackedWidget.addWidget(self.page_2)
        self.page_10 = QtGui.QWidget()
        self.page_10.setObjectName(_fromUtf8("page_10"))
        self.stackedWidget.addWidget(self.page_10)
        self.page_9 = QtGui.QWidget()
        self.page_9.setObjectName(_fromUtf8("page_9"))
        self.stackedWidget.addWidget(self.page_9)
        self.page_5 = QtGui.QWidget()
        self.page_5.setObjectName(_fromUtf8("page_5"))
        self.stackedWidget.addWidget(self.page_5)
        self.page_11 = QtGui.QWidget()
        self.page_11.setObjectName(_fromUtf8("page_11"))
        self.stackedWidget.addWidget(self.page_11)
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.stackedWidget)
        self.stackedWidget_2 = QtGui.QStackedWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget_2.sizePolicy().hasHeightForWidth())
        self.stackedWidget_2.setSizePolicy(sizePolicy)
        self.stackedWidget_2.setMinimumSize(QtCore.QSize(130, 30))
        self.stackedWidget_2.setObjectName(_fromUtf8("stackedWidget_2"))
        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName(_fromUtf8("page_3"))
        self.sBtimeon = QtGui.QDoubleSpinBox(self.page_3)
        self.sBtimeon.setGeometry(QtCore.QRect(0, 0, 130, 27))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sBtimeon.sizePolicy().hasHeightForWidth())
        self.sBtimeon.setSizePolicy(sizePolicy)
        self.sBtimeon.setMinimumSize(QtCore.QSize(130, 27))
        self.sBtimeon.setDecimals(3)
        self.sBtimeon.setMinimum(0.0)
        self.sBtimeon.setMaximum(65536.0)
        self.sBtimeon.setSingleStep(1.0)
        self.sBtimeon.setProperty("value", 40.0)
        self.sBtimeon.setObjectName(_fromUtf8("sBtimeon"))
        self.stackedWidget_2.addWidget(self.page_3)
        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName(_fromUtf8("page_4"))
        self.sBriseTime = QtGui.QDoubleSpinBox(self.page_4)
        self.sBriseTime.setGeometry(QtCore.QRect(0, 0, 130, 27))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sBriseTime.sizePolicy().hasHeightForWidth())
        self.sBriseTime.setSizePolicy(sizePolicy)
        self.sBriseTime.setMinimumSize(QtCore.QSize(130, 27))
        self.sBriseTime.setDecimals(3)
        self.sBriseTime.setMaximum(65536.0)
        self.sBriseTime.setProperty("value", 40.0)
        self.sBriseTime.setObjectName(_fromUtf8("sBriseTime"))
        self.stackedWidget_2.addWidget(self.page_4)
        self.page_8 = QtGui.QWidget()
        self.page_8.setObjectName(_fromUtf8("page_8"))
        self.stackedWidget_2.addWidget(self.page_8)
        self.page_7 = QtGui.QWidget()
        self.page_7.setObjectName(_fromUtf8("page_7"))
        self.stackedWidget_2.addWidget(self.page_7)
        self.page_6 = QtGui.QWidget()
        self.page_6.setObjectName(_fromUtf8("page_6"))
        self.stackedWidget_2.addWidget(self.page_6)
        self.page_12 = QtGui.QWidget()
        self.page_12.setObjectName(_fromUtf8("page_12"))
        self.stackedWidget_2.addWidget(self.page_12)
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.stackedWidget_2)
        self.Bsubmit = QtGui.QPushButton(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Bsubmit.sizePolicy().hasHeightForWidth())
        self.Bsubmit.setSizePolicy(sizePolicy)
        self.Bsubmit.setMinimumSize(QtCore.QSize(130, 27))
        self.Bsubmit.setObjectName(_fromUtf8("Bsubmit"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.Bsubmit)

        self.retranslateUi(MainWindow)
        self.sWDC.setCurrentIndex(0)
        self.sWDC2.setCurrentIndex(0)
        self.sWamp1.setCurrentIndex(0)
        self.sWamp2.setCurrentIndex(0)
        self.sWperiod1.setCurrentIndex(0)
        self.sWperiod2.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
        QtCore.QObject.connect(self.cBmode,
                               QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")),
                               self.stackedWidget.setCurrentIndex)
        QtCore.QObject.connect(self.cBmode,
                               QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")),
                               self.stackedWidget_2.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Waveform Configuration", None))
        self.label.setText(_translate("MainWindow", "Select mode", None))
        self.cBmode.setItemText(0, _translate("MainWindow", "Square", None))
        self.cBmode.setItemText(1, _translate("MainWindow", "Triangle", None))
        self.cBmode.setItemText(2, _translate("MainWindow", "Sine", None))
        self.cBmode.setItemText(3, _translate("MainWindow", "Sawtooth", None))
        self.cBmode.setItemText(4, _translate("MainWindow", "Fixed potential", None))
        self.cBmode.setItemText(5, _translate("MainWindow", "Import CSV", None))
        self.label_4.setText(_translate("MainWindow", "DC Value (V)", None))
        self.label_2.setText(_translate("MainWindow", "Select file", None))
        self.Bchoose.setText(_translate("MainWindow", "Choose", None))
        self.lb_amplitude.setText(_translate("MainWindow", "Amplitude (V)", None))
        self.lb_namefile.setText(_translate("MainWindow", "no file chosen", None))
        self.lb_period.setText(_translate("MainWindow", " Period (ms)", None))
        self.label_6.setText(_translate("MainWindow", "Time On (ms)", None))
        self.label_5.setText(_translate("MainWindow", "Rise Time", None))
        self.Bsubmit.setText(_translate("MainWindow", "Submit", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QDialog()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
