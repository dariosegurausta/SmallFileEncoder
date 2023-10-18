import os
import time
import Helpers
import FingerprintReader as fpr
import CardReader as cr
import SmallFileCoder as sfc
from Door import Door

class Program:
    def __init__(self) -> None:
        self.defaultKey= [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        self.templetaSize=1536
        self.fpr = fpr.FingerprintReader()
        self.cr = cr.CardReader()
        self.Door = Door()
        self.Door.Test(1)
    def main(self):
        while True:
            try:
                op=self.Menu()
                if op== 1: self.Enroll()
                if op== 2: self.Validate()
            except Exception as exc:
                print('Error: '+str(exc))
                time.sleep(3)
    def Enroll(self):
        self.Clear()
        print('Enroll')
        print('Pon tu huella en el lector....')
        self.fpr.WaitForFinger()
        print('Puedes retirar tu huella.....')
        template = self.fpr.CaptureTemplate()
        print('Codificando......')
        template = sfc.SmallFileCoder.GetNoEndZerosData(template)     
        encoder = sfc.SmallFileCoder(template,1,sfc.Operation.Encode)
        print('Pon la tarjeta en el lector.....')
        id=self.cr.WaitForCardId()
        print('Leyendo tarjeta.....')
        dataEncoded=encoder.CodedData()
        data=self.cr.ReadAllPresentCardNoSectorTrailerNoInfoBlock(self.defaultKey)
        data[0][0]=len(dataEncoded)>>8&0xFF
        data[0][1]=len(dataEncoded)&0xFF
        for i in range(len(dataEncoded)): data[int((i+2)/16)][int((i+2)%16)]=dataEncoded[i]
        print('Escribiendo tarjeta.....')
        self.cr.WriteAllPresentCardNoSectorTrailerNoInfoBlock(id,self.defaultKey,data)
        print('Proceso terminado.')
        input('Digite enter para terminar')
    def Validate(self):
        self.Clear()
        print('Inicia validación')
        print('Presenta la tarjeta....')
        self.cr.WaitForCardId()
        print('Tarjeta detectada....')
        cardData=self.cr.ReadAllPresentCardNoSectorTrailerNoInfoBlock(self.defaultKey)
        cardData = Helpers.ArrayToVector(cardData)
        datalen=cardData[0]*0x100+cardData[1]
        templateCoded=cardData[2:datalen+2]
        decoder = sfc.SmallFileCoder(templateCoded,1,sfc.Operation.Decode)
        template = decoder.Data()
        template=sfc.SmallFileCoder.CompleteEndZerosData(template,self.templetaSize)
        print('Coloque la huella en el sensor....')
        self.fpr.WaitForFinger()
        self.fpr.CaptureTemplate()
        print('Validando.....')
        valid = self.fpr.ValidateTemplate(template)
        if (valid == True): 
            print('Acceso consedido')
            self.Door.Open()
            time.sleep(5)
            self.Door.Close()
        else: print('Acceso denegado')
        input('Presione enter para continuar')
    def Clear(self): os.system('clear')
    def Menu(self):
        while (True):
            self.Clear()
            print('1. Capturar huella y grabar tarjeta')
            print('2. Realizar validación')
            op = input()
            if (op=='1' or op=='2'): return int(op)
Program().main()