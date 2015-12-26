Octoprint-Lcd
===

Octoprint-Lcd is a touchscreen interface plugin for [Octoprint](https://github.com/foosel/OctoPrint), designed for the official [Raspberry Pi Touchscreen](https://www.raspberrypi.org/products/raspberry-pi-touch-display/). It is currently undergoing development, and is nowhere near complete, but is very usable on a day to day biases.

Octoprint-Lcd uses [Kivy](http://kivy.org/#home) to draw to the screen and handle input in a separate thread.

Features
===
**Stable, fully functioning features**

 - View status of the printer, including:
  - Current state
  - Current file loaded
  - Temperatures
  - Filament usage for the current file loaded
  - Time into print
  - Time remaining in print
  - Total time of print
  - Start, stop, or cancel prints
 - Control of the printer, including:
  - Temperatures with a nice on screen keypad
  - Tool selection
  - Filament extrude/retract of different amounts
  - Motors on/off
  - Jog with different step sizes
  - Home XY, Z, or XYZ
 - Connection and other miscellaneous controls, including:
  - Serial port, baud rate, and profile selection for connecting
  - Printer and AUX power
  - Shutdown of the Pi
 - File Selector for files uploaded to Octoprint:
  - Shows files in date order, newest at the top
  - Shows date uploaded, estimated time, and filament usage
  - Allows printing, selecting, or deleting a file
 - Status information always present in top right of screen:
  - Current state
  - Loaded file
 - Adjusts displayed information to match printer profile:
  - Number of extruders
  - Heated Bed temperatures

Experimental Features
===
**These features may or may not work depending on state of completion, your system, and other factors**

 - USB drive hotplug file transfer
  - Allows files on a USB drive to be transfered to Octoprint for printing
  - Uses udisks2 through dbus to detect USB drive insertion and moutning
  - Seems to have permission problems on Raspbian, however it works fine on Ubuntu.

Upcoming Features
===
**Features to maybe get into a future commit**

 - Settings in Octoprint settings manager
 - Custom buttons
 - Terminal tab
 - Gcode viewer
 - Slicer tab

Installation
===

First, make sure that [Octoprint](https://github.com/foosel/OctoPrint) is installed

Install [Kivy](http://kivy.org/#home):
---
**Rasbian Jessie:**

From http://kivy.org/docs/installation/installation-rpi.html:

Install the dependencies:
```
sudo apt-get update
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
      python-setuptools libgstreamer1.0-dev git-core \
         gstreamer1.0-plugins-{bad,base,good,ugly} \
            gstreamer1.0-{omx,alsa} python-dev cython
```
Install Kivy globally on your system:
```
sudo pip install git+https://github.com/kivy/kivy.git@master
```
Or build and use kivy inplace (best for development):
```
git clone https://github.com/kivy/kivy
cd kivy

make
echo "export PYTHONPATH=$(pwd):\$PYTHONPATH" >> ~/.profile
source ~/.profile
```

**Rasbian Wheezy:**

From http://kivy.org/docs/installation/installation-rpi.html:

Add APT sources for Gstreamer 1.0 in /etc/apt/sources.list:
```
deb http://vontaene.de/raspbian-updates/ . main
```
Add APT key for vontaene.de:
```
gpg --recv-keys 0C667A3E
gpg -a --export 0C667A3E | sudo apt-key add -
```
Install the dependencies:
```
sudo apt-get update
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev
```
Install pip from source:
```
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
sudo python get-pip.py
```
Install Cython from sources (debian package are outdated):
```
sudo pip install cython
```
Install Kivy globally on your system:
```
sudo pip install git+https://github.com/kivy/kivy.git@master
```
Or build and use kivy inplace (best for development):
```
git clone https://github.com/kivy/kivy
cd kivy

make
echo "export PYTHONPATH=$(pwd):\$PYTHONPATH" >> ~/.profile
source ~/.profile
```
Install Octoprint-Lcd:
===

Make sure that the correct `python` is being run if Octoprint is in a virtual environment (ie OctoPi)
```
git clone https://github.com/chickenchuck040/OctoPrint-Lcd.git
cd OctoPrint-Lcd
python setup.py install
```
