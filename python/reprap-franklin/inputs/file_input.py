#!/usr/bin/env python
import threading
import time

class FileInput( threading.Thread ):

    def __init__(self, reprap, source, delay=None):
        self.reprap = reprap
        self.source = source
        self.delay = delay

        threading.Thread.__init__(self)
        self.daemon = True


    def run(self):
        with open(self.source) as src:
            for line in src:
                self.reprap.current_firmware.execute_gcode(line)

                if callable(self.delay):
                    self.delay()
                else:
                    time.sleep( float(self.delay) )

        print("Done reading from file.")
