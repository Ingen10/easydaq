# EasyDAQ

EasyDAQ is a test software application intended for demonstrating the Stream Mode operation of openDAQ.
This demo is compatible with Python 3.X.
* * *
**OpenDAQ** is an open source data acquisition instrument, which provides user
several physical interaction capabilities such as analog inputs and outputs,
digital inputs and outputs, timers and counters.

Through a USB connection, openDAQ brings all the information that it captures
to a host computer, where you can decide how to process, display and store it.
Several demos and examples are provided in website's support page.
(http://www.open-daq.com/paginas/support)

Please, go to http://www.open-daq.com for additional info.
For support, e-mail to support@open-daq.com

## Installation


## Installation

It is highly recommended to install this package in a virtual Python environment using
[virtualenv](https://virtualenv.pypa.io/en/stable/) or a similar tool.

```sh
git clone https://github.com/openDAQ/easydaq.git && cd easydaq
pip3 install matplotlib==2.2.5 pyqt5
python setup.py install
```
