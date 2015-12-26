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
 - Adjusts displayed information to match printer profile:
  - Number of extruders
  - Heated Bed temperatures

Experimental Features
===
**Theses features may or may not work depending on state of completion, your system, and other factors**

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
