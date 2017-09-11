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

from . import easydaq
from . import config
from . import configurechart
from . import configwave


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
        self.cfg = QtCore.QSettings('opendaq')
        self.tam_values = 100
        #  Experiments
        self.experiments = [0, 0, 0, 0]
        self.color_curve = ['#ff0000', '#55aa00', '#0000ff']
        if sys.version[0] == '3':
            port_opendaq = self.cfg.value('port')
        else:
            port_opendaq = self.cfg.value('port').toString()
        #  Plot parameters
        self.rate = [10, 10, 10]
        try:
            self.daq = DAQ(str(port_opendaq))
            self.model = DAQModel.new(*self.daq.get_info())
            self.dlg1 = ConfigExperiment(self.model, self.cfg, 0)
            self.dlg2 = ConfigExperiment(self.model, self.cfg, 1)
            self.dlg3 = ConfigExperiment(self.model, self.cfg, 2)
        except:
            port_opendaq = ''
            for p in [self.Bplay, self.cBenable1, self.cBenable2, self.cBenable3, self.cBenable4]:
                p.setEnabled(False)
        #  Experiments windows
        self.toolBar.actionTriggered.connect(self.get_port)
        self.Bconfigure1.clicked.connect(lambda: self.configure_experiment(0))
        self.Bconfigure2.clicked.connect(lambda: self.configure_experiment(1))
        self.Bconfigure3.clicked.connect(lambda: self.configure_experiment(2))
        self.Bconfigure4.clicked.connect(self.configure_wave)
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
        self.time = [0, 0, 0]
        self.experiments = [0, 0, 0, 0]
        self.create_experiments()
        self.update()

    def get_buffer(self):
        #  Obtener parametros
        wave_param = ['wmode_index', 'period', 'offset', 'amplitude', 'time', 'rise_time']
        param = {}
        for p in wave_param:
            if sys.version[0] == 3:
                param[p] = int(self.cfg.value(p))
            else:
                param[p] = self.cfg.value(p).toInt()[0]

        self.tam_buff = 300
        if param['wmode_index'] == 4:
            self.interval = int(param['period'])
        else:
            self.interval = int(param['period'] / (self.tam_buff + 1))
        if self.interval < 1:
            self.interval = 1
        self.tam_buff = int(param['period'] / self.interval)
        self.buffer = np.zeros(self.tam_buff)
        #  Square
        if param['wmode_index'] == 0:
            points_up = int(param['time'] / self.interval)
            points_down = int(param['period'] / self.interval) - points_up
            for i in range(self.tam_buff):
                if i > points_up:
                    self.buffer[i] = -(param['amplitude']/2.0) + param['offset']
                else:
                    self.buffer[i] = param['amplitude']/2.0 + param['offset']
        #  Triangle
        elif param['wmode_index'] == 1:
            points_up = int(self.tam_buff * param['rise_time'] / param['period'])
            if points_up == 0:
                points_up = 1
            points_down = self.tam_buff - points_up
            increment = float(param['amplitude']) / float(points_up - 1)
            for i in range(points_up):
                self.buffer[i] = round((param['offset'] + increment * i), 2)
            init = param['offset'] + param['amplitude']
            increment = float(param['amplitude']) / float(points_down - 1)
            for i in range(points_down):
                self.buffer[i + points_up] = round((init - increment * i), 2)
        #  Sine
        elif param['wmode_index'] == 2:
            t = np.arange(0, param['period'], self.interval)
            self.buffer = np.sin(2 * np.pi / param['period'] * t) * param['amplitude']
            for i, v in enumerate(self.buffer):
                self.buffer[i] = v + param['offset']
        #  Sawtooth
        elif param['wmode_index'] == 3:
            increment = float(param['amplitude']) / (self.tam_buff - 1)
            for i in range(self.tam_buff):
                self.buffer[i] = param['offset'] + increment * i
        #  Fixed potential
        elif param['wmode_index'] == 4:
            for i in range(self.tam_buff):
                self.buffer[i] = param['offset']

    def create_experiments(self):
        exp_param = ['type_index', 'mode_index', 'posch', 'negch', 'range_index',
                     'samples', 'rate']
        for i, p in enumerate([self.cBenable1, self.cBenable2, self.cBenable3]):
            if p.isChecked():
                # Obtener los parametros
                param = {}
                for j, p in enumerate(exp_param):
                    self.cfg.beginReadArray(p)
                    self.cfg.setArrayIndex(i)
                    if sys.version[0] == '3':
                        param[p] = self.cfg.value(p)
                    else:
                        param[p] = self.cfg.value(p).toInt()[0]
                    self.cfg.endArray()
                self.num_points = 0 if param['mode_index'] else 20
                #  Crear exp
                if param['type_index']:
                    self.experiments[i] = self.daq.create_external(mode=ExpMode.ANALOG_IN, clock_input=i+1, edge=0, npoints=self.num_points, continuous=not(param['mode_index']))
                else:
                    self.experiments[i] = self.daq.create_stream(mode=ExpMode.ANALOG_IN, period=param['rate'], npoints=self.num_points, continuous=not(param['mode_index']))
                self.experiments[i].analog_setup(pinput=param['posch'], ninput=param['negch'], gain=param['range_index'], nsamples=param['samples'])
        if self.cBenable4.isChecked():
            self.get_buffer()
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
        for i in range(3):
            if self.experiments[i] and self.experiments[i].get_mode() == ExpMode.ANALOG_IN:
                new_data = self.experiments[i].read()
                for j, d in enumerate(new_data):
                    if self.coef[i] >= self.tam_values:
                        self.coef[i] = self.tam_values - 1
                        displace(self.X[i])
                        displace(self.Y[i])
                    self.X[i][self.coef[i]] = self.time[i]
                    self.Y[i][self.coef[i]] = float(d)
                    self.coef[i] = self.coef[i] + 1
                    self.time[i] = self.time[i] + self.rate[i]/1000.0
                if self.coef[i]:
                    self.plotWidget.canvas.ax.plot(self.X[i][:self.coef[i]], self.Y[i][:self.coef[i]], color=self.color_curve[i], linewidth=0.7)
                    self.plotWidget.canvas.draw()

    def configure_wave(self):
        try:
            self.dlg_wave.show()
        except:
            self.dlg_wave = ConfigureWave(self.cfg)
            self.dlg_wave.exec_()

    def configure_experiment(self, i):
        exp = [self.dlg1, self.dlg2, self.dlg3]
        exp[i].show()

    def get_port(self):
        dlg = Configuration(self)
        dlg.exec_()
        port_opendaq = dlg.return_port()
        if port_opendaq != '':
            self.cfg.setValue('port', port_opendaq)
            self.daq = DAQ(str(port_opendaq))
            self.model = DAQModel.new(*self.daq.get_info())
            self.dlg1 = ConfigExperiment(self.model, self.cfg, 0)
            self.dlg2 = ConfigExperiment(self.model, self.cfg, 1)
            self.dlg3 = ConfigExperiment(self.model, self.cfg, 2)
            for p in [self.cBenable1, self.cBenable2, self.cBenable3, self.cBenable4, self.Bplay]:
                p.setEnabled(True)
            self.statusBar.showMessage("Hardware Version: %s   Firmware Version: %s" % (self.daq.hw_ver[1], self.daq.fw_ver))
        else:
            for p in [self.cBenable1, self.cBenable2, self.cBenable3, self.cBenable4, self.Bplay]:
                p.setEnabled(False)
            self.statusBar.showMessage("")


class ConfigureWave(QtGui.QDialog, configwave.Ui_MainWindow):
    def __init__(self, cfg, parent=None):
        super(ConfigureWave, self).__init__(parent)
        self.setupUi(self)
        self.cBmode.currentIndexChanged.connect(self.change)
        self.Bsubmit.clicked.connect(lambda: self.conf_wave(cfg))

    def conf_wave(self, cfg):
        wave_param = {"wmode_index": self.cBmode.currentIndex(),
                      "period": self.sBperiodms.value(),
                      "offset": self.sBoffset.value(),
                      "amplitude": self.sBamplitude.value(),
                      "time": self.sBtimeon.value(),
                      "rise_time": self.sBriseTime.value()}
        for p in wave_param.keys():
            cfg.setValue(p, wave_param[p])
        self.hide()

    def closeEvent(self, evnt):
            evnt.ignore()
            self.hide()

    def change(self):
        for wid in [self.sWperiod1, self.sWperiod2, self.sWamp1, self.sWamp2]:
            wid.setCurrentIndex(1 if int(self.cBmode.currentIndex()) == 4 else 0)


class ConfigExperiment(QtGui.QDialog, configurechart.Ui_MainWindow):
    def __init__(self, model, cfg, exp, parent=None):
        super(ConfigExperiment, self).__init__(parent)
        self.model = model
        self.names = ['AGND', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'VREF']
        self.setupUi(self)
        self.get_cb_values(cfg, exp)
        self.pBconfirm.clicked.connect(lambda: self.update_conf(cfg, exp))
        self.cBtype.currentIndexChanged.connect(self.status_period)

    def update_conf(self, cfg, exp):
        Range = self.cBrange.currentIndex()
        rate = self.sBrate.value()
        samples = self.sBsamples.value()
        mode_SE = self.cBtype.currentIndex()
        ch_pos = self.names.index(self.cBposchannel.currentText())
        ch_neg = self.names.index(self.cBnegchannel.currentText())
        exp_param = {"type_index": mode_SE, "mode_index": self.cBmode.currentIndex(),
                     "posch": ch_pos, "negch": ch_neg, "range_index": Range,
                     "samples": samples, "rate": rate}
        for p in exp_param.keys():
            cfg.beginWriteArray(p)
            cfg.setArrayIndex(exp)
            cfg.setValue(p, exp_param[p])
            cfg.endArray()
        self.hide()

    def get_cb_values(self, cfg, exp):
        for ninput in self.model.adc.ninputs:
            self.cBnegchannel.addItem(self.names[ninput] if ninput < 9 else self.names[9])
        for pinput in self.model.adc.pinputs:
            self.cBposchannel.addItem(self.names[pinput] if pinput < 9 else self.names[9])
        for gain in self.model.adc.pga_gains:
            self.cBrange.addItem(str(gain))

    def closeEvent(self, evnt):
            evnt.ignore()
            self.hide()

    def status_period(self):
        self.sBrate.setEnabled(False if self.cBtype.currentIndex() else True)


class Configuration(QtGui.QDialog, config.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Configuration, self).__init__(parent)
        self.setupUi(self)
        for portO in list_serial_ports():
            self.cbport.addItem(portO)
        self.connectButton.clicked.connect(self.return_port)

    def return_port(self):
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
