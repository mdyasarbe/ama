import serial,time 

class ArduinoSetup:
    def __init__(self):
        self.ser=serial.Serial('COM4', 9600, timeout=.1) 

    def connect(self):
        return self.ser
