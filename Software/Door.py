#============== MEM - USTA =======================
# Encapsula las funciones de puertos para apertura y cierre de la puerta
from gpiozero import LED
import time
class Door:
    def __init__(self):
        self.DoorPortA="GPIO26"
        self.DoorPortB="GPIO16"
        self.DoorA = LED(self.DoorPortA)
        self.DoorB = LED(self.DoorPortB)
    def Open(self):
        self.DoorA.on()
        self.DoorB.off()
    def Close(self):
        self.DoorA.off()
        self.DoorB.off()
    def Test(self, seconds:int):
        self.Open()
        time.sleep(seconds)
        self.Close()
        time.sleep(seconds)