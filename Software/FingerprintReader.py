import time
import serial
import Adafruit_Fingerprint_Custom as adafruit_fingerprint

#============== MEM - USTA =======================
#Libreria para la captura de template de huella y validación
class FingerprintReader:
    def __init__(self):
        self.uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=5)
        self.finger = adafruit_fingerprint.Adafruit_Fingerprint(self.uart)
    def WaitForFinger(self):
        while self.finger.get_image() != adafruit_fingerprint.OK:
            time.sleep(0.1)
    def CaptureTemplate(self):
        self.finger.image_2_tz(1)
        fpTemplate = self.finger.get_fpdata(sensorbuffer="char",slot=1)
        return fpTemplate
    def ValidateTemplate(self, fpTemplate):
        self.finger.send_fpdata(fpTemplate, "char",2)
        result=self.finger.compare_templates()
        return adafruit_fingerprint.OK==result