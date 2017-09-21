import warnings
import matplotlib.cbook

from PyQt4.QtGui import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
from matplotlib.figure import Figure


warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(facecolor='#cccccc')
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.15, bottom=0.15, right=0.9, top=0.9)
        self.ax.grid(True)
        self.xtitle = "Time (s)"
        self.ytitle = "Voltage (V)"
        self.format_labels()
        FigureCanvas.__init__(self, self.fig)

    def format_labels(self):
        self.ax.set_xlabel(self.xtitle, fontsize=12)
        self.ax.set_ylabel(self.ytitle, fontsize=12)
        labels_x = self.ax.get_xticklabels()
        labels_y = self.ax.get_yticklabels()
        for xlabel in labels_x:
            xlabel.set_fontsize(10)
        for ylabel in labels_y:
            ylabel.set_fontsize(10)


class MPL_Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = MyMplCanvas()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.canvas)
        self.setLayout(self.vbox)


class NavigationToolbar(NavigationToolbar2QT):
    toolitems = [t for t in NavigationToolbar2QT.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save', 'Subplots')]
