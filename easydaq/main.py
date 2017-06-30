#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import glob
import fractions

import numpy as np
import serial
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
from matplotlib.figure import Figure
from opendaq import DAQ, ExpMode
from opendaq.models import DAQModel
from opendaq.daq import *

import easydaq
import config
import configurechart
import configwave


def list_serial_ports():
    #  Serial port names
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class MyApp(QtGui.QMainWindow, easydaq.Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.names = ['AGND', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'VREF']
        self.cfg = QtCore.QSettings('opendaq')
        self.X = [[], [], [], []]
        self.Y = [[], [], [], []]
        self.ch_pos = [1, 1, 1, 1]
        self.ch_neg = [0, 0, 0, 0]
        self.range = [0, 0, 0, 0]
        self.rate = [100, 100, 100, 100]
        self.samples = [20, 20, 20, 20]
        self.mode = [True, True, True, True]
        self.modeSE = [0, 0, 0, 0]
        self.num_points = [0, 0, 0, 0]
        self.experiments = [0, 0, 0, 0]
        self.color_curve = ['#ff0000', '#55aa00', '#0000ff', '#e3e300']
        port_opendaq = str(self.cfg.value('port').toString())
        self.wave_mode = 0
        self.wave_period = 15
        self.wave_offset = 1
        self.wave_amplitude = 1
        self.wave_timeon = 0
        self.wave_risetime = 0
        try:
            self.daq = DAQ(port_opendaq)
        except:
            port_opendaq = ''
            for p in [self.Bconfigure1, self.Bconfigure2, self.Bconfigure3, self.Bconfigure4, self.Bconfigure5, self.Bplay]:
                p.setEnabled(False)
        self.toolBar.actionTriggered.connect(self.GetPort)
        self.Bconfigure1.clicked.connect(lambda: self.configureChart(0))
        self.Bconfigure2.clicked.connect(lambda: self.configureChart(1))
        self.Bconfigure3.clicked.connect(lambda: self.configureChart(2))
        self.Bconfigure4.clicked.connect(lambda: self.configureChart(3))
        self.Bconfigure5.clicked.connect(self.Configurewave)
        self.Bplay.clicked.connect(self.plot)
        self.Bstop.clicked.connect(self.stop)
        try:
            self.statusBar.showMessage("Hardware Version: %s   Firmware Version: %s" % (self.daq.hw_ver[1], self.daq.fw_ver))
        except:
            pass

    def stop(self):
        self.daq.stop(clear=True)

    def plot(self):
        self.daq.stop(clear=True)
        self.plotWidget.canvas.ax.cla()
        self.plotWidget.canvas.ax.grid(True)
        self.X = [[], [], [], []]
        self.Y = [[], [], [], []]
        self.experiments = [0, 0, 0, 0]
        for i, p in enumerate([self.cBenable1, self.cBenable2, self.cBenable3, self.cBenable4]):
            if p.isChecked():
                if self.modeSE[i]:
                    self.experiments[i] = self.daq.create_external(mode=ExpMode.ANALOG_IN, clock_input=i+1, edge=0, npoints=self.num_points[i], continuous=self.mode[i])
                else:
                    self.experiments[i] = self.daq.create_stream(mode=ExpMode.ANALOG_IN, period=self.rate[i], npoints=self.num_points[i], continuous=self.mode[i])
                self.experiments[i].analog_setup(pinput=self.ch_pos[i], ninput=self.ch_neg[i], gain=self.range[i], nsamples=self.samples[i])

        if self.cBenable5.isChecked():
            self.Waves()
            self.experiments[3] = self.daq.create_stream(mode=ExpMode.ANALOG_OUT, period=self.interval, npoints=len(self.buffer))
            self.experiments[3].load_signal(self.buffer)
            print(len(self.buffer))
        self.daq.start()
        self.update()

    def update(self):
        for i in range(4):
            if self.experiments[i] and self.experiments[i].get_mode() == ExpMode.ANALOG_IN:
                new_data = self.experiments[i].read()
                for d in new_data:
                    self.time = self.rate[i]/1000.0*len(self.Y[i])
                    self.X[i].append(self.time)
                    self.Y[i].append(float(d))
                self.plotWidget.canvas.ax.plot(self.X[i], self.Y[i], color=self.color_curve[i], linewidth=0.7)
                self.plotWidget.canvas.draw()

        if self.Bplay.isChecked():
            timer = QtCore.QTimer()
            timer.timeout.connect(self.update)
            timer.start(0.5)
            QtCore.QTimer.singleShot(500, self.update)

    def Configurewave(self):
        dlg = Configure_Wave(self)
        if dlg.exec_():
            self.wave_mode, self.wave_period, self.wave_offset, self.wave_amplitude, self.wave_timeon, self.wave_risetime = dlg.conf_wave()
            print(self.wave_mode, self.wave_period, self.wave_offset, self.wave_amplitude, self.wave_timeon, self.wave_risetime)

    def Waves(self):
        self.buffer = []
        #  Square
        if self.wave_mode == 0:
            self.interval = fractions.gcd(self.wave_period, self.wave_timeon)
            print(self.interval)
            points_up = int(self.wave_timeon / self.interval)
            points_down = int(self.wave_period / self.interval) - points_up
            print(points_up, points_down)
            for i in range(points_up):
                self.buffer.append(self.wave_amplitude/2.0 + self.wave_offset)
            for v in range(points_down):
                self.buffer.append(-(self.wave_amplitude/2.0 + self.wave_offset))
        #  Triangle
        elif self.wave_mode == 1:
            if self.wave_period < 140:
                self.interval = 1
                points_up = int(self.wave_risetime)
                points_down = int(self.wave_period - points_up)
                increment = self.wave_amplitude / self.wave_risetime
            else:
                #  Ideal number points
                points_up = int(140 / (self.wave_period / self.wave_risetime))
                if points_up == 0:
                    points_up = 1
                points_down = 140 - points_up
                self.interval = int(self.wave_risetime / points_up) + 1
                points_up = int(self.wave_risetime / self.interval)
                if points_up == 0:
                    points_up = 1
                increment = self.wave_amplitude / points_up
            for i in range(points_up):
                self.buffer.append(round((self.wave_offset + increment * i),2))
            if self.wave_period >= 140:
                self.interval = int((self.wave_period - self.wave_risetime) / points_down) + 1
                points_down = int((self.wave_period - self.wave_risetime) / self.interval)
            increment = self.wave_amplitude / points_down
            init = self.wave_offset + self.wave_amplitude
            for i in range(points_down):
                self.buffer.append(round((init - increment*i),2))
        #  Sine
        elif self.wave_mode == 2:
            self.interval = 1 if self.wave_period < 140 else (self.wave_period/140 + 1)
            t = np.arange(0, self.wave_period, self.interval)
            self.buffer = np.sin(2 * np.pi / self.wave_period * t) * (self.wave_amplitude)
            for i, v in enumerate(self.buffer):
                self.buffer[i] = v + self.wave_offset
        #  Sawtooth
        elif self.wave_mode == 3:
            if self.wave_period < 140:
                self.interval = 1
                points = int(self.wave_period)
                increment = self.wave_amplitude / points
            else:
                self.interval = int(self.wave_period / 140) + 1
                points = int(self.wave_period / self.interval)
                if points == 0:
                    points = 1
                increment = self.wave_amplitude / points
            for i in range(points):
                self.buffer.append(self.wave_offset + increment * i)
        #  Fixed potential
        elif self.wave_mode == 4:
            self.buffer.append(self.wave_offset)

        if len(self.buffer) >= 140:
            self.buffer = self.buffer[:140]
        print(self.buffer)

    def configureChart(self, i):
        dlg = Configure_chart(self.daq)
        if dlg.exec_():
            values = dlg.update_conf()
            self.ch_pos[i] = self.names.index(str(values[0]))
            self.ch_neg[i] = self.names.index(str(values[1]))
            self.range[i] = values[2]
            self.rate[i] = values[3]
            self.samples[i] = values[4]
            self.mode[i] = values[5]
            self.modeSE[i] = values[6]
            self.num_points[i] = 0 if self.mode[i] else 20
            print(self.ch_pos, self.ch_neg)
            print(self.range, self.rate, self.samples)
            print(self.mode, self.modeSE, self.num_points)

    def GetPort(self):
        dlg = Configuration(self)
        dlg.exec_()
        port_opendaq = dlg.ReturnPort()
        if port_opendaq != '':
            self.cfg.setValue('port', port_opendaq)
            self.daq = DAQ(str(port_opendaq))
            for p in [self.Bconfigure1, self.Bconfigure2, self.Bconfigure3, self.Bconfigure4, self.Bconfigure5, self.Bplay]:
                p.setEnabled(True)
            self.statusBar.showMessage("Hardware Version: %s   Firmware Version: %s" % (self.daq.hw_ver[1], self.daq.fw_ver))
        else:
            for p in [self.Bconfigure1, self.Bconfigure2, self.Bconfigure3, self.Bconfigure4, self.Bconfigure5, self.Bplay]:
                p.setEnabled(False)
            self.statusBar.showMessage("")


class Configure_Wave(QtGui.QDialog, configwave.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Configure_Wave, self).__init__(parent)
        self.setupUi(self)
        self.cBmode.currentIndexChanged.connect(self.change)
        self.Bsubmit.clicked.connect(self.conf_wave)

    def conf_wave(self):
        mode_wave = self.cBmode.currentIndex()
        period = self.sBperiodus.value()*1000 if self.cBmodoPeriod.currentIndex() else self.sBperiodms.value()
        offset = self.sBoffset.value()
        amplitude = self.sBamplitude.value()
        time_on = self.sBtimeon.value() if mode_wave == 0 else 0
        rise_time = self.sBriseTime.value() if mode_wave == 1 else 0
        self.accept()
        self.close()
        return mode_wave, period, offset, amplitude, time_on, rise_time

    def change(self):
        self.sBamplitude.setEnabled(False if int(self.cBmode.currentIndex()) == 4 else True)


class Configure_chart(QtGui.QDialog, configurechart.Ui_MainWindow):
    def __init__(self, daq, parent=None):
        super(Configure_chart, self).__init__(parent)
        self.daq = daq
        self.names = ['AGND', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'VREF']
        self.setupUi(self)
        self.GetcbValues()
        self.pBconfirm.clicked.connect(self.update_conf)

    def update_conf(self):
        pos_channel = self.cBposchannel.currentText()
        neg_channel = self.cBnegchannel.currentText()
        Range = self.cBrange.currentIndex()
        Rate = self.sBrate.value()
        samples = self.sBsamples.value()
        mode = False if self.cBmode.currentIndex() else True
        mode_SE = 1 if self.rBextern.isChecked() else 0
        self.accept()
        self.close()
        return pos_channel, neg_channel, Range, Rate, samples, mode, mode_SE

    def GetcbValues(self):
        model = DAQModel.new(*self.daq.get_info())
        for ninput in model.adc.ninputs:
            self.cBnegchannel.addItem(self.names[ninput] if ninput < 9 else self.names[9])
        for pinput in model.adc.pinputs:
            self.cBposchannel.addItem(self.names[pinput] if pinput < 9 else self.names[9])
        for gain in model.adc.pga_gains:
            self.cBrange.addItem(str(gain))


class Configuration(QtGui.QDialog, config.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Configuration, self).__init__(parent)
        self.setupUi(self)
        for portO in list_serial_ports():
            self.cbport.addItem(portO)
        self.connectButton.clicked.connect(self.ReturnPort)

    def ReturnPort(self):
        port = self.cbport.currentText()
        self.close()
        return port


def main():
    app = QtGui.QApplication(sys.argv)
    dlg = MyApp()
    dlg.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
