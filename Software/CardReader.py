from mfrc522 import MFRC522
#============== MEM - USTA =======================
#Libreria para la escritura y lectura de Mifare 1K
#   enfocada en el proceso de la informacion de toda la tarjeta a la vez
class CardReader:
    def __init__(self):
        self.mfrcReader = MFRC522()
        self.sectorTrailers=[3,7,11,15,19,23,27,31,35,39,43,47,51,55,59,63]
    def WaitForCardId(self):
        while True:
            uid=self.GetCardId()
            if(uid!=None):break
        return uid
    def GetCardId(self):
        intento=5
        while intento>0:
            (status,TagType) = self.mfrcReader.MFRC522_Request(self.mfrcReader.PICC_REQIDL)
            if(status==self.mfrcReader.MI_OK):
                    (status,uid) = self.mfrcReader.MFRC522_Anticoll()
                    if(len(uid)>0):
                        return uid
                    else:
                        raise ValueError('Presenta solo una tarjeta')
            intento=intento-1
        return None
    def ReadBlock(self,uid,key,bloque):       
        self.mfrcReader.MFRC522_SelectTag(uid)
        state = self.mfrcReader.MFRC522_Auth(self.mfrcReader.PICC_AUTHENT1A,bloque,key,uid)
        if state !=self.mfrcReader.MI_OK:raise ValueError("Falló autenticacion")
        data = self.mfrcReader.MFRC522_Read(bloque)
        self.mfrcReader.MFRC522_StopCrypto1()
        return data
    def ReadAllPresentCardNoSectorTrailerNoInfoBlock(self,key):
        datos =[]
        for bloque in range(1,64):
            if ((bloque+1)%4)==0:continue
            for intento in range(0,5):
                uid=self.GetCardId()
                if uid!=None:
                    print("Leyendo bloque: %d"%bloque)
                    dat = self.ReadBlock(uid,key,bloque)
                    datos.append(dat)
                    break
            if intento>=4: return None
        return datos
    def WriteSector(self,uid,key,bloque,data):        
        if bloque in self.sectorTrailers: raise ValueError('Este es un Sector Trailer, no se puede escribir con esta función')        
        if len(data)!=16: raise ValueError('Se deben escribir solo los 8 bytes del sector')
        self.mfrcReader.MFRC522_SelectTag(uid)
        state = self.mfrcReader.MFRC522_Auth(self.mfrcReader.PICC_AUTHENT1A,bloque,key,uid)
        if state !=self.mfrcReader.MI_OK:raise ValueError("Falló autenticacion")
        data = self.mfrcReader.MFRC522_Write(bloque,data)
        self.mfrcReader.MFRC522_StopCrypto1()
    def WriteAllPresentCardNoSectorTrailerNoInfoBlock(self,uid,key,data):
        expectedDataLend=64-len(self.sectorTrailers)-1
        if(len(data)!=expectedDataLend): raise ValueError('Los datos deben la informacionpara '+str(expectedDataLend)+' bloques de 16 bytes cada uno')
        for bloque in range(1,64):
            if ((bloque+1)%4)==0:continue
            newId=self.GetCardId()
            if(newId!=uid): raise ValueError('La tarjeta se ha cambiado!!!!')
            print("Escibiendo bloque: %d"%bloque)
            self.WriteSector(uid,key,bloque,data[(bloque-1)-int(bloque/4)])
