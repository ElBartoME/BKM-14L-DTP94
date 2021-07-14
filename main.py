import serial
import time
import optix
import serialthread

dtp = optix.Optix()
dtp.set_mode(lcd=0)
dtp.selfcalibrate(prompt=True)
print("Done")

serial_thread = serialthread.SerialThread()
serial_thread.start()
serial_thread.resume()

while True:
    (Y, x, y) = dtp.Yxy()
    serial_thread.setxyY(x,y,Y)



