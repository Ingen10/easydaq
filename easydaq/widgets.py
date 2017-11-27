import warnings
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.figure import Figure

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(facecolor='#cccccc')
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.15, bottom=0.15, right=0.9, top=0.9)
        self.ax.grid(True)
        self.ax.autoscale(False)
        FigureCanvas.__init__(self, self.fig)


class MPL_Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = MyMplCanvas()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.canvas)
        self.setLayout(self.vbox)


class NavigationToolbar(NavigationToolbar2QT):
    toolitems = [t for t in NavigationToolbar2QT.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]
