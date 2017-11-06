# easydaq

EasyDAQ is a test software application intended for demonstrating the Stream Mode operation of openDAQ.
This demo is compatible with Python 2.7 and 3.X.
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
* * *
## Installation

You will need **administrator rights** (root access) to install this package
system-wide.

To install the last stable version:

**Python 3**

```sh
    $ pip3 install easydaq
```
**Python 2.7**
```sh
    $ pip install easydaq
```

To install the development version (it is highly recommended to use a
[virtual environment](https://virtualenv.pypa.io/en/stable/) for this):

```sh
    $ git clone github.com/opendaq/easydaq
    $ cd easydaq
    $ python setup.py install
```

In any case, if for any reason the setup fails, daqcontrol demo will require the following packages:

- opendaq

- setuptools

- numpy

- matplotlib

- serial

- scipy

- PyQt5

All these packages are available on pip. To install them:

**Python 3**

```sh
    $ pip3 install "package"
```
**Python 2.7**
```sh
    $ pip install "package"
```
