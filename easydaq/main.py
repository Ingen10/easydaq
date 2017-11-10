#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import glob
import csv

import numpy as np
import serial
from serial import SerialException
#from scipy import signal
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from opendaq import DAQ, ExpMode
from opendaq.models import DAQModel
from opendaq.common import LengthError

from .widgets import NavigationToolbar, MyMplCanvas
from . import easy_daq
from . import config
from . import configurechart
from . import configwave
from . import axes_op

BUFFER_SIZE = 400


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
        except SerialException:
            pass
    return result


class MyApp(QtWidgets.QMainWindow, easy_daq.Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.cfg = QtCore.QSettings('opendaq')
        #  Toolbar
        nav = NavigationToolbar(self.plotWidget.canvas, self.plotWidget.canvas)
        nav.setVisible(False)
        for action in nav.actions()[:-1]:
            self.toolBar.addAction(action)
        icons = [":/resources/house.png", ":/resources/pan.png", ":/resources/zoom.png", ":/resources/save.png"]
        for i, action in enumerate(self.toolBar.actions()[6:10]):
            action.setIcon(QIcon(icons[i]))
        #  Graphs
        Y, X = [np.zeros(BUFFER_SIZE)] * 2
        Y[:] = np.nan
        X[:] = np.nan
        self.graphs = []
        colors = ['#ff0000', '#55aa00', '#0000ff']
        buttons = [self.Bconfigure1, self.Bconfigure2, self.Bconfigure3]
        combo_boxes = [self.cBenable1, self.cBenable2, self.cBenable3]
        for i in range(3):
            self.graphs.append(Graph(exp=0, Y=Y, X=X, rate=10, color=colors[i],
                                     button=buttons[i], combo_box=combo_boxes[i]))

        exp_param = {"type_index": 0, "mode_index": 0,
                     "posch": 1, "negch": 0, "range_index": 0,
                     "samples": 200, "rate": 10}
        for p in exp_param.keys():
            self.cfg.beginWriteArray(p)
            for exp in range(3):
                self.cfg.setArrayIndex(exp)
                self.cfg.setValue(p, exp_param[p])
            self.cfg.endArray()

        port_opendaq = str(self.cfg.value('port'))
        try:
            self.daq = DAQ((port_opendaq))
        except (LengthError, SerialException):
            port_opendaq = ''
            self.daq = ''
        if port_opendaq:
            self.statusBar.showMessage("Hardware Version: %s   Firmware Version: %s" % (
                self.daq.hw_ver[1], self.daq.fw_ver))
        for g in self.graphs:
            g.combo_box.setEnabled(bool(port_opendaq))
        for p in [self.actionPlay, self.cBenable4]:
            p.setEnabled(bool(port_opendaq))
        #  Experiments configuration windows
        self.dlg1 = ConfigExperiment(self.daq, self.cfg, 0)
        self.dlg2 = ConfigExperiment(self.daq, self.cfg, 1)
        self.dlg3 = ConfigExperiment(self.daq, self.cfg, 2)
        self.dlg4 = ConfigureWave(self.cfg)

        self.Bconfigure4.clicked.connect(self.configure_wave)
        self.actionPlay.triggered.connect(self.play)
        self.actionStop.triggered.connect(self.stop)
        self.actionCSV.triggered.connect(self.export_csv)
        self.actionConfigure.triggered.connect(self.get_port)
        self.actionAxes.triggered.connect(self.change_axes)
        self.graphs[0].button.clicked.connect(lambda: self.configure_experiment(0))
        self.graphs[1].button.clicked.connect(lambda: self.configure_experiment(1))
        self.graphs[2].button.clicked.connect(lambda: self.configure_experiment(2))

    def stop(self):
        self.daq.stop()
        for g in self.graphs:
            g.combo_box.setEnabled(True)
            g.button.setEnabled(g.combo_box.isChecked())
            self.plotWidget.canvas.ax.plot(g.Y, color=g.color, linewidth=0.7)
        self.daq.flush()
        self.daq.clear_experiments()
        self.actionPlay.toggle()
        self.actionStop.setEnabled(False)
        for wid in [self.actionPlay, self.actionCSV, self.actionConfigure, self.cBenable4]:
            wid.setEnabled(True)
        self.Bconfigure4.setEnabled(self.cBenable4.isChecked())

    def play(self):
        self.actionStop.setEnabled(True)
        for g in self.graphs:
            g.combo_box.setEnabled(False)
            g.button.setEnabled(False)
        for wid in [self.cBenable4, self.Bconfigure4, self.actionCSV, self.actionPlay,
                    self.actionConfigure]:
            wid.setEnabled(False)
        self.daq.clear_experiments()
        self.plotWidget.canvas.ax.cla()
        self.plotWidget.canvas.ax.grid(True)
        Y, X = [np.zeros(BUFFER_SIZE)] * 2
        Y[:] = np.nan
        X[:] = np.nan
        for i, g in enumerate(self.graphs):
            g.Y = Y
            g.X = X
            g.exp = 0
        self.create_experiments()
        self.update()

    def export_csv(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Export as CSV')[0]
        fieldnames = ['Time (ms)', 'Voltage (V)']
        for i, g in enumerate(self.graphs):
            if g.combo_box.isChecked():
                with open('%s_exp%d.csv' % (fname, (i + 1)), 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    j = 0
                    while not(np.isnan(g.Y[j])):
                        writer.writerow(
                            {'Time (ms)': g.X[j] * 1000, 'Voltage (V)': g.Y[j]})
                        j = j + 1

    def create_buffer(self):
        wave_param = ['wmode_index', 'period',
                      'offset', 'amplitude', 'time', 'rise_time']
        param = {}
        for p in wave_param:
            param[p] = int(self.cfg.value(p))
        self.data_size = 300
        self.interval = float(param['period']) / (self.data_size + 1)
        if self.interval > int(self.interval):
            self.interval = int(self.interval) + 1 
        else:
            self.interval = int(self.interval)
        if self.interval < 1:
            self.interval = 1
        self.data_size = int(param['period'] / self.interval)
        self.buffer = np.zeros(self.data_size)
        if param['wmode_index'] == 0:
            self.create_square(param['time'], param['period'],
                               param['amplitude'], param['offset'])
        elif param['wmode_index'] == 1:
            self.create_triangle(param['rise_time'], param['period'],
                                 param['amplitude'], param['offset'])
        elif param['wmode_index'] == 2:
            self.create_sine(param['period'], param[
                             'amplitude'], param['offset'])
        elif param['wmode_index'] == 3:
            self.create_sawtooth(param['period'], param[
                                 'amplitude'], param['offset'])
        elif param['wmode_index'] == 4:
            self.create_fixed_potential(param['period'], param['offset'])
        else:
            path = str(self.cfg.value("file_path"))
            self.import_csv(path)

    def create_sine(self, period, amplitude, offset):
        t = np.arange(0, period, self.interval)
        self.buffer = np.sin(2 * np.pi / period * t) * amplitude + offset

    def create_sawtooth(self, period, amplitude, offset):
        self.buffer = amplitude * \
            (np.linspace(1, 10, self.data_size)) / 10.0 + offset

    def create_square(self, risetime, period, amplitude, offset):
        duty = float(risetime) / period
        t = np.linspace(0, period, self.data_size, endpoint=False)
        for i in range(self.data_size):
            if t[i]/float(period) <= duty:
                self.buffer[i] = offset + amplitude
            else:
                self.buffer[i] = offset
        '''
        duty = float(risetime) / period
        t = np.linspace(0, period, self.data_size, endpoint=False)
        self.buffer = amplitude * \
            (signal.square((2 * np.pi * t / period), duty=duty)) + offset
        '''

    def create_triangle(self, risetime, period, amplitude, offset):
        dutty = float(risetime) / period
        t = np.arange(0, period, self.interval)
        i = 0
        while (float(t[i]) / period) <= dutty:
            i = i + 1
            pass
        self.buffer[:(i+1)] =  amplitude * (np.linspace(1, 10, (i+1))) / 10.0 + offset
        self.buffer[(i+1):] = self.buffer[i] - (amplitude * (np.linspace(1, 10, (self.data_size - i - 1))) / 10.0 + offset)
        '''
        dutty = float(risetime) / period
        t = np.arange(0, period, self.interval)
        self.buffer = amplitude * (signal.sawtooth(2.0 * np.pi / period * t, dutty)) + offset
        '''

    def create_fixed_potential(self, period, offset):
        self.interval = period
        self.buffer[:] = offset

    def import_csv(self, path):
        self.interval = 0.0
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            self.data_size = 400
            self.buffer = np.zeros(self.data_size)
            for i, row in enumerate(reader):
                if i == 0:
                    initial_time = float(row['Time (ms)'])
                self.buffer[i] = float(row['Voltage (V)'])
            self.interval = int(abs(float(row['Time (ms)']) - initial_time) / float(i))
        self.buffer = self.buffer[:i]

    def create_experiments(self):
        exp_param = ['type_index', 'mode_index', 'posch', 'negch', 'range_index',
                     'samples', 'rate']
        for i, g in enumerate(self.graphs):
            if g.combo_box.isChecked():
                #  Parameters
                param = {}
                for j, p in enumerate(exp_param):
                    self.cfg.beginReadArray(p)
                    self.cfg.setArrayIndex(i)
                    param[p] = self.cfg.value(p)
                    self.cfg.endArray()
                self.num_points = 0 if param['mode_index'] else 20
                g.rate = param['rate']
                #  Create experiment
                if int(param['type_index']):
                    g.exp = self.daq.create_external(
                        mode=ExpMode.ANALOG_IN, clock_input=i + 1, edge=0,
                        npoints=self.num_points, continuous=not(param['mode_index']))
                else:
                    g.exp = self.daq.create_stream(
                        mode=ExpMode.ANALOG_IN, period=int(g.rate), npoints=self.num_points,
                        continuous=not(bool(param['mode_index'])))
                g.exp.analog_setup(pinput=int(param['posch']), ninput=int(
                    param['negch']), gain=int(param['range_index']),
                    nsamples=int(param['samples']))
        if self.cBenable4.isChecked():
            self.create_buffer()
            self.waveform = self.daq.create_stream(
                mode=ExpMode.ANALOG_OUT, period=self.interval, npoints=len(self.buffer),
                continuous=True)
            self.waveform.load_signal(self.buffer)

    def update(self):
        play_status = False
        for g in self.graphs:
            play_status = play_status | g.combo_box.isChecked()
        if self.actionPlay.isChecked() and play_status:
            self.daq.start()
            self.plot()
            timer = QtCore.QTimer()
            timer.timeout.connect(self.update)
            timer.start(0.01)
            QtCore.QTimer.singleShot(10, self.update)

    def plot(self):
        i = 0
        for g in self.graphs:
            if g.exp and g.exp.get_mode() == ExpMode.ANALOG_IN:
                if i:
                    self.plotWidget.canvas.ax.hold(True)
                else:
                    self.plotWidget.canvas.ax.hold(not(self.cBosc.isChecked()))
                i = i + 1
                new_data = g.exp.read()
                for j, d in enumerate(new_data):
                    g.Y = np.roll(g.Y, 1)
                    g.Y[0] = float(d)
                    g.X = np.roll(g.X, 1)
                    if np.isnan(g.X[1]):
                        g.X[0] = 0
                    else:
                        g.X[0] = g.X[1] + float(g.rate) / 1000.0
                self.plotWidget.canvas.ax.plot(
                    g.X, g.Y, g.color, linewidth=0.7)
                self.plotWidget.canvas.ax.grid(True)
                self.plotWidget.canvas.draw()

    def configure_wave(self):
        self.dlg4.show()

    def configure_experiment(self, i):
        exp = [self.dlg1, self.dlg2, self.dlg3]
        exp[i].daq = self.daq
        exp[i].show()

    def change_axes(self):
        dlg_axes = AxesConfiguration(self.plotWidget)
        dlg_axes.exec_()
        print(self.graphs[0].X)
        print(self.graphs[0].Y)

    def get_port(self):
        dlg = Configuration(self)
        dlg.exec_()
        port_opendaq = dlg.return_port()
        try:
            self.daq = DAQ(str(port_opendaq))
        except (LengthError, SerialException):
            port_opendaq = ''
        if port_opendaq:
            self.cfg.setValue('port', port_opendaq)
            self.statusBar.showMessage("Hardware Version: %s   Firmware Version: %s" % (
                self.daq.hw_ver[1], self.daq.fw_ver))
            for exp, d in enumerate([self.dlg1, self.dlg2, self.dlg3]):
                d.get_cb_values(self.cfg, exp, self.daq)
        else:
            self.statusBar.showMessage("")
        for g in self.graphs:
            g.combo_box.setEnabled(bool(port_opendaq))
        for p in [self.cBenable4, self.actionPlay]:
            p.setEnabled(bool(port_opendaq))


class ConfigureWave(QtWidgets.QMainWindow, configwave.Ui_mainWindow):
    def __init__(self, cfg, parent=None):
        super(ConfigureWave, self).__init__(parent)
        self.setupUi(self)
        self.path = ''
        self.cBmode.currentIndexChanged.connect(self.change)
        self.Bchoose.clicked.connect(self.select_file)
        self.Bsubmit.clicked.connect(lambda: self.conf_wave(cfg))

    def conf_wave(self, cfg):
        wave_param = {"wmode_index": self.cBmode.currentIndex(),
                      "period": self.sBperiodms.value(),
                      "offset": self.sBoffset.value(),
                      "amplitude": self.sBamplitude.value(),
                      "time": self.sBtimeon.value(),
                      "rise_time": self.sBriseTime.value(),
                      "file_path": str(self.path)}
        for p in wave_param.keys():
            cfg.setValue(p, wave_param[p])
        self.hide()

    def closeEvent(self, evnt):
        evnt.ignore()
        self.hide()

    def change(self):
        index_mode = self.cBmode.currentIndex()
        self.sWDC.setCurrentIndex(1 if index_mode == 5 else 0)
        if index_mode == 4:
            self.sW2.setCurrentIndex(0)
        elif index_mode == 5:
            self.sW2.setCurrentIndex(1)
        else:
            self.sW2.setCurrentIndex(2)

    def select_file(self):
        self.path = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open file', '', "CSV Files (*.csv)")
        path = (str(self.path)).split(',')
        self.path = path[0][2: -1]
        self.lb_namefile.setText(self.path.split('/')[-1])


class ConfigExperiment(QtWidgets.QDialog, configurechart.Ui_MainWindow):
    def __init__(self, daq, cfg, exp, parent=None):
        super(ConfigExperiment, self).__init__(parent)
        self.daq = daq
        self.names = ['AGND', 'A1', 'A2', 'A3',
                      'A4', 'A5', 'A6', 'A7', 'A8', 'VREF']
        self.setupUi(self)
        if daq:
            self.get_cb_values(cfg, exp, daq)
        self.pBconfirm.clicked.connect(lambda: self.update_conf(cfg, exp))
        self.cBtype.currentIndexChanged.connect(self.status_period)

    def update_conf(self, cfg, exp):
        w_range = self.cBrange.currentIndex()
        rate = self.sBrate.value()
        samples = self.sBsamples.value()
        mode_SE = self.cBtype.currentIndex()
        ch_pos = self.names.index(self.cBposchannel.currentText())
        ch_neg = self.names.index(self.cBnegchannel.currentText())
        exp_param = {"type_index": mode_SE, "mode_index": self.cBmode.currentIndex(),
                     "posch": ch_pos, "negch": ch_neg, "range_index": w_range,
                     "samples": samples, "rate": rate}
        for p in exp_param.keys():
            cfg.beginWriteArray(p)
            cfg.setArrayIndex(exp)
            cfg.setValue(p, exp_param[p])
            cfg.endArray()
        self.hide()

    def get_cb_values(self, cfg, exp, daq):
        model = DAQModel.new(*daq.get_info())
        for ninput in model.adc.ninputs:
            self.cBnegchannel.addItem(
                self.names[ninput] if ninput < 9 else self.names[9])
        for pinput in model.adc.pinputs:
            self.cBposchannel.addItem(
                self.names[pinput] if pinput < 9 else self.names[9])
        for gain in model.adc.pga_gains:
            self.cBrange.addItem(str(gain))

    def closeEvent(self, evnt):
        evnt.ignore()
        self.hide()

    def status_period(self):
        self.sBrate.setEnabled(False if self.cBtype.currentIndex() else True)


class Configuration(QtWidgets.QDialog, config.Ui_MainWindow):
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

class AxesConfiguration(QtWidgets.QDialog, axes_op.Ui_MainWindow):
    def __init__(self, plot, parent=None):
        super(AxesConfiguration, self).__init__(parent)
        self.setupUi(self)
        self.plt = plot
        self.configure_widgets()
        self.ax_Bok.clicked.connect(self.config_axes)

    def configure_widgets(self):
        self.ax_title.setText(self.plt.canvas.ax.get_title())
        self.ax_xlb.setText(self.plt.canvas.ax.get_xlabel())
        self.ax_ylb.setText(self.plt.canvas.ax.get_ylabel())
        x_limits = self.plt.canvas.ax.get_xlim()
        self.ax_left.setText(str(x_limits[0] / 100.0))
        self.ax_right.setText(str(x_limits[1] / 100.0))
        y_limits = self.plt.canvas.ax.get_ylim()
        self.ax_bottom.setText(str(y_limits[0]))
        self.ax_top.setText(str(y_limits[1]))

    def config_axes(self):
        self.plt.canvas.ax.set_autoscaley_on(False)
        self.plt.canvas.ax.set_autoscalex_on(False)
        self.plt.canvas.ax.set_xlabel(self.ax_xlb.text(), fontsize=10)
        self.plt.canvas.ax.set_ylabel(self.ax_ylb.text(), fontsize=10)
        self.plt.canvas.ax.set_title(self.ax_title.text())
        self.plt.canvas.ax.set_xlim(float(self.ax_left.text()), float(self.ax_right.text()))
        self.plt.canvas.ax.set_ylim(float(self.ax_bottom.text()), float(self.ax_top.text()))
        scale_options = ['linear', 'log', 'logit']
        self.plt.canvas.draw()
        self.close()
        #return(returns)


class Graph(object):
    def __init__(self, exp, Y, X, rate, color, button, combo_box):
        self.exp = exp
        self.Y = Y
        self.X = X
        self.rate = rate
        self.color = color
        self.button = button
        self.combo_box = combo_box


def main():
    app = QtWidgets.QApplication(sys.argv)
    dlg = MyApp()
    dlg.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
