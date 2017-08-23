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
import matplotlib
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

def displace(vector):
        for i in range(len(vector)-1):
            vector[i] = vector[i+1]
        return vector

class MyApp(QtGui.QMainWindow, easydaq.Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.names = ['AGND', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'VREF']
        self.cfg = QtCore.QSettings('opendaq')

        #  Configuracion inicial experimentos
        exp_parameters = ["type_index", "mode_index", "posch_index", "negch_index", "range_index", "samples", "rate"]
        values = [0, 0, 0, 0, 0, 200, 10]
        for i, p in enumerate(exp_parameters):          
            self.cfg.beginWriteArray(p)
            for j in range(3):
                self.cfg.setArrayIndex(j)
                self.cfg.setValue(p,values[i])
            self.cfg.endArray()

        #  Configuracion inicial waveform
        wave_param = ["wmode_index", "period_index", "period", "perios_us", "offset", "amplitude", "time", "rise_time"]
        wvalues = [0, 0, 100, 100000, 0, 1, 40, 40]
        for i, p in enumerate(wave_param):
            self.cfg.setValue(p, wvalues[i])

        self.tam_buff = 60
        self.tam_values = 100

        #  Experiments
        self.ch_pos = [1, 1, 1]
        self.ch_neg = [0, 0, 0]
        self.range = [0, 0, 0]
        self.rate = [10, 10, 10]
        self.samples = [20, 20, 20]
        self.mode = [True, True, True]
        self.modeSE = [0, 0, 0]
        self.num_points = [0, 0, 0]
        self.experiments = [0, 0, 0, 0]
        self.color_curve = ['#ff0000', '#55aa00', '#0000ff']
        port_opendaq = str(self.cfg.value('port').toString())

        #  Wave
        self.wave_mode = 0
        self.wave_period = 100
        self.wave_offset = 0
        self.wave_amplitude = 1
        self.wave_timeon = 40
        self.wave_risetime = 40
        self.buffer = np.zeros(self.tam_buff)

        self.coef = [0, 0, 0]
        self.time = 0

        try:
            self.daq = DAQ(port_opendaq)
            self.model = DAQModel.new(*self.daq.get_info())
        except:
            port_opendaq = ''
            for p in [self.Bconfigure1, self.Bconfigure2, self.Bconfigure3, self.Bconfigure4, self.Bplay]:
                p.setEnabled(False)
        self.toolBar.actionTriggered.connect(self.GetPort)
        self.Bconfigure1.clicked.connect(lambda: self.configureChart(0))
        self.Bconfigure2.clicked.connect(lambda: self.configureChart(1))
        self.Bconfigure3.clicked.connect(lambda: self.configureChart(2))
        self.Bconfigure4.clicked.connect(self.Configurewave)
        self.Bplay.clicked.connect(self.play)
        self.Bstop.clicked.connect(self.stop)
        try:
            self.statusBar.showMessage("Hardware Version: %s   Firmware Version: %s" % (self.daq.hw_ver[1], self.daq.fw_ver))
        except:
            pass

    def stop(self):
        conf_buttons = [self.Bconfigure1, self.Bconfigure2, self.Bconfigure3, self.Bconfigure4]
        for i, p in enumerate([self.cBenable1, self.cBenable2, self.cBenable3, self.cBenable4]):
            conf_buttons[i].setEnabled(True if p.isChecked() else False)
        for i in range(3):
            self.plotWidget.canvas.ax.plot(self.X[i], self.Y[i], color=self.color_curve[i], linewidth=0.7)
        self.daq.stop()

    def play(self):
        self.daq.clear_experiments()
        self.plotWidget.canvas.ax.cla()
        self.plotWidget.canvas.ax.grid(True)
        self.X = np.zeros((3, self.tam_values))
        self.Y = np.zeros((3, self.tam_values))
        self.coef = [0, 0, 0]
        self.time = 0
        self.buffer = np.zeros(self.tam_buff)
        self.experiments = [0, 0, 0, 0]
        self.get_buffer()
        self.conf_experiments()
        self.update()

    def get_buffer(self):
        #  Square
        if self.wave_mode == 0:
            self.interval = self.wave_period / float(self.tam_buff)
            points_up = int(self.wave_timeon / self.interval)
            points_down = int(self.wave_period / self.interval) - points_up
            for i in range(self.tam_buff):
                if i > points_up:
                    self.buffer[i] = -(self.wave_amplitude/2.0) + self.wave_offset
                else:
                    self.buffer[i] = self.wave_amplitude/2.0 + self.wave_offset
        #  Triangle
        elif self.wave_mode == 1:
            points_up = int(self.tam_buff * self.wave_risetime / self.wave_period)
            if points_up == 0:
                points_up = 1
            points_down = self.tam_buff - points_up
            increment = float(self.wave_amplitude) / float(points_up - 1)
            for i in range(points_up):
                self.buffer[i] = round((self.wave_offset + increment * i), 2)
            self.interval = int((self.wave_period - self.wave_risetime) / points_down) + 1
            init = self.wave_offset + self.wave_amplitude
            increment = float(self.wave_amplitude) / float(points_down - 1)
            for i in range(points_down):
                self.buffer[i + points_up] = round((init - increment * i), 2)
        #  Sine
        elif self.wave_mode == 2:
            self.interval = (self.wave_period/self.tam_buff + 1)
            t = np.arange(0, self.wave_period, self.interval)
            self.buffer = np.sin(2 * np.pi / self.wave_period * t) * (self.wave_amplitude)
            for i, v in enumerate(self.buffer):
                self.buffer[i] = v + self.wave_offset
        #  Sawtooth
        elif self.wave_mode == 3:
            self.interval = self.wave_period/(self.tam_buff + 1)
            increment = float(self.wave_amplitude) / (self.tam_buff - 1)
            for i in range(self.tam_buff):
                self.buffer[i] = self.wave_offset + increment * i
        #  Fixed potential
        elif self.wave_mode == 4:
            self.interval = self.wave_period
            for i in range(self.tam_buff):
                self.buffer[i] = self.wave_offset

    def conf_experiments(self):
        for i, p in enumerate([self.cBenable1, self.cBenable2, self.cBenable3]):
            if p.isChecked():
                if self.modeSE[i]:
                    self.experiments[i] = self.daq.create_external(mode=ExpMode.ANALOG_IN, clock_input=i+1, edge=0, npoints=self.num_points[i], continuous=self.mode[i])
                else:
                    self.experiments[i] = self.daq.create_stream(mode=ExpMode.ANALOG_IN, period=self.rate[i], npoints=self.num_points[i], continuous=self.mode[i])
                self.experiments[i].analog_setup(pinput=self.ch_pos[i], ninput=self.ch_neg[i], gain=self.range[i], nsamples=self.samples[i])
        if self.cBenable4.isChecked():
            self.experiments[3] = self.daq.create_stream(mode=ExpMode.ANALOG_OUT, period=self.interval, npoints=len(self.buffer), continuous=True)
            self.experiments[3].load_signal(self.buffer)

    def update(self):
        play_status = self.cBenable1.isChecked() | self.cBenable2.isChecked() | self.cBenable3.isChecked()
        if self.Bplay.isChecked() and play_status:
            self.daq.start()
            self.plot()
            timer = QtCore.QTimer()
            timer.timeout.connect(self.update)
            timer.start(0.01)
            QtCore.QTimer.singleShot(10, self.update)

    def plot(self):
        for i in range(4):
            if self.experiments[i] and self.experiments[i].get_mode() == ExpMode.ANALOG_IN:
                new_data = self.experiments[i].read()
                for j, d in enumerate(new_data):
                    if self.coef[i] >= self.tam_values:
                        self.coef[i] = self.tam_values - 1
                        displace(self.X[i])
                        displace(self.Y[i])
                    self.X[i][self.coef[i]] = self.time
                    self.Y[i][self.coef[i]] = float(d)
                    self.coef[i] = self.coef[i] + 1
                    self.time = self.time + self.rate[i]/1000.0
                if self.coef[i]:
                    self.plotWidget.canvas.ax.plot(self.X[i][:self.coef[i]], self.Y[i][:self.coef[i]], color=self.color_curve[i], linewidth=0.7)
                    self.plotWidget.canvas.draw()

    def Configurewave(self):
        dlg = Configure_Wave(self.cfg)
        if dlg.exec_():
            self.wave_mode, self.wave_period, self.wave_offset, self.wave_amplitude, self.wave_timeon, self.wave_risetime = dlg.conf_wave(self.cfg)

    def configureChart(self, i):
        dlg = Configure_chart(self.model, self.cfg, i)
        if dlg.exec_():
            values = dlg.update_conf(self.cfg, i)
            self.ch_pos[i] = self.names.index(str(values[0]))
            self.ch_neg[i] = self.names.index(str(values[1]))
            self.range[i] = values[2]
            self.rate[i] = values[3]
            self.samples[i] = values[4]
            self.mode[i] = values[5]
            self.modeSE[i] = values[6]
            self.num_points[i] = 0 if self.mode[i] else 20

    def GetPort(self):
        dlg = Configuration(self)
        dlg.exec_()
        port_opendaq = dlg.ReturnPort()
        if port_opendaq != '':
            self.cfg.setValue('port', port_opendaq)
            self.daq = DAQ(str(port_opendaq))
            self.model = DAQModel.new(*self.daq.get_info())
            for p in [self.cBenable1, self.cBenable2, self.cBenable3, self.cBenable4, self.Bplay]:
                p.setEnabled(True)
            self.statusBar.showMessage("Hardware Version: %s   Firmware Version: %s" % (self.daq.hw_ver[1], self.daq.fw_ver))
        else:
            for p in [self.cBenable1, self.cBenable2, self.cBenable3, self.cBenable4, self.Bplay]:
                p.setEnabled(False)
            self.statusBar.showMessage("")


class Configure_Wave(QtGui.QDialog, configwave.Ui_MainWindow):
    def __init__(self, cfg, parent=None):
        super(Configure_Wave, self).__init__(parent)
        self.setupUi(self)
        self.initialize(cfg)
        self.cBmode.currentIndexChanged.connect(self.change)
        self.Bsubmit.clicked.connect(lambda: self.conf_wave(cfg))

    def initialize(self, cfg):
        wave_param = ["wmode_index", "period_index", "period", "perios_us", "offset", "amplitude", "time", "rise_time"]
        wave_wid = [self.cBmode, self.cBmodoPeriod, self.sBperiodms, self.sBperiodus, self.sBoffset, self.sBamplitude, self.sBtimeon, self.sBriseTime]
        for i, p in enumerate(wave_param):
            if i > 1:
                wave_wid[i].setValue(cfg.value(p).toInt()[0])
            else:
                wave_wid[i].setCurrentIndex(cfg.value(p).toInt()[0])

    def conf_wave(self, cfg):
        mode_wave = self.cBmode.currentIndex()
        period = self.sBperiodus.value()*1000 if self.cBmodoPeriod.currentIndex() else self.sBperiodms.value()
        offset = self.sBoffset.value()
        amplitude = self.sBamplitude.value()
        time_on = self.sBtimeon.value() if mode_wave == 0 else 0
        rise_time = self.sBriseTime.value() if mode_wave == 1 else 0

        wave_param = ["wmode_index", "period_index", "period", "perios_us", "offset", "amplitude", "time", "rise_time"]
        wave_wid = [self.cBmode, self.cBmodoPeriod, self.sBperiodms, self.sBperiodus, self.sBoffset, self.sBamplitude, self.sBtimeon, self.sBriseTime]
        for i, p in enumerate(wave_param):
            if i > 1:
                cfg.setValue(p, wave_wid[i].value())
            else:
                cfg.setValue(p, wave_wid[i].currentIndex())

        self.accept()
        self.close()
        return mode_wave, period, offset, amplitude, time_on, rise_time

    def change(self):
        self.sBamplitude.setEnabled(False if int(self.cBmode.currentIndex()) == 4 else True)


class Configure_chart(QtGui.QDialog, configurechart.Ui_MainWindow):
    def __init__(self, model, cfg, exp, parent=None):
        super(Configure_chart, self).__init__(parent)
        self.model = model
        self.names = ['AGND', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'VREF']
        self.setupUi(self)
        self.GetcbValues(cfg, exp)
        self.pBconfirm.clicked.connect(lambda: self.update_conf(cfg, exp))
        self.cBtype.currentIndexChanged.connect(self.status_period)


    def update_conf(self, cfg, exp):
        pos_channel = self.cBposchannel.currentText()
        neg_channel = self.cBnegchannel.currentText()
        Range = self.cBrange.currentIndex()
        Rate = self.sBrate.value()
        samples = self.sBsamples.value()
        mode = False if self.cBmode.currentIndex() else True
        mode_SE = self.cBtype.currentIndex()

        exp_parameters = ["type_index", "mode_index", "posch_index", "negch_index", "range_index", "samples", "rate"]
        values = [mode_SE, self.cBmode.currentIndex(), self.cBposchannel.currentIndex(), self.cBnegchannel.currentIndex(), Range, samples, Rate]
        for i, p in enumerate(exp_parameters):       
            cfg.beginWriteArray(p)
            cfg.setArrayIndex(exp)
            cfg.setValue(p,values[i])
            cfg.endArray()

        self.accept()
        self.close()
        return pos_channel, neg_channel, Range, Rate, samples, mode, mode_SE

    def GetcbValues(self, cfg, exp):
        for ninput in self.model.adc.ninputs:
            self.cBnegchannel.addItem(self.names[ninput] if ninput < 9 else self.names[9])
        for pinput in self.model.adc.pinputs:
            self.cBposchannel.addItem(self.names[pinput] if pinput < 9 else self.names[9])
        for gain in self.model.adc.pga_gains:
            self.cBrange.addItem(str(gain))

        exp_param = ["type_index", "mode_index", "posch_index", "negch_index", "range_index", "samples", "rate"]
        gui_w = [self.cBtype, self.cBmode, self.cBposchannel, self.cBnegchannel, self.cBrange, self.sBsamples, self.sBrate]
        for i, p in enumerate(exp_param):
            a = []
            cfg.beginReadArray(p)
            for j in range(3):
                cfg.setArrayIndex(j)
                a.append(cfg.value(p).toInt())
            cfg.endArray()
            if i > 4:
                gui_w[i].setValue(a[exp][0])
            else:
                gui_w[i].setCurrentIndex(a[exp][0])

    def status_period(self):
        self.sBrate.setEnabled(False if self.cBtype.currentIndex() else True)


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
