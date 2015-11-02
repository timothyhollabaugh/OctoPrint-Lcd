from __future__ import absolute_import

import octoprint.printer

from ..ui import Data

class OctoprintUpdate(octoprint.printer.PrinterCallback):

    def on_printer_send_current_data(self, cdata):
        print cdata
        Data.setCurrentData(cdata)
