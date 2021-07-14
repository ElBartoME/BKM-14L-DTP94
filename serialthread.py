import serial
import os
import threading
import time

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        #print( "base init", file=sys.stderr )
        super(StoppableThread, self).__init__()
        self._stopper = threading.Event()          # ! must not use _stop

    def stopit(self):                              #  (avoid confusion)
        #print( "base stop()", file=sys.stderr )
        self._stopper.set()                        # ! must not use _stop

    def stopped(self):
        return self._stopper.is_set()              # ! must not use _stop

class SerialThread(StoppableThread):

    def __init__(self, *args, **kwargs):
        StoppableThread.__init__(self)
        self.x = 0
        self.y = 0
        self.Y = 0
        self.paused = True  # Start out paused.
        self.state = threading.Condition()

    def setxyY(self, x, y, Y):
        self.x = x
        self.y = y
        self.Y = Y

    def pause(self):
        with self.state:
            self.paused = True  # Block self.

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

    def run(self):
        #print(check_output(['hostname', '-I']))

        with serial.Serial(port='COM3', baudrate=9600, bytesize=7, parity='E', stopbits=2, timeout=1) as ser:
            line = ser.read_until(b'\r')
            line = ser.read_until(b'\r')

            print(line)

            while True:
                with self.state:
                    if self.paused:
                        self.state.wait()  # Block execution until notified.
                # (Y, x, y) = dtp.Yxy()
                Y = self.Y
                x = int(self.x * 1000)
                y = int(self.y * 1000)
                str = 'P1 {x:3d};{y:3d};{Y:3.2f}\r\n'
                str = str.format(x=x, y=y, Y=Y)
                ser.write(str)
                print(str.encode())
                time.sleep(0.75)
