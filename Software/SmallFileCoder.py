from multipledispatch import dispatch
from enum import Enum
import copy

class Operation(Enum):
    Encode=0
    Decode=1
class DataFormat(Enum):
    Encoded=True
    Clear=False
class SmallFileCoder:
    def Data(self): return self._clearData;
    def CodedData(self): return self._codedData;
    def __init__(self,Data:list, lengthCode: int, operation: Operation):
        self._tableLength = 2**lengthCode
        self._codeLength = lengthCode
        if operation == Operation.Encode:
            self._clearData = Data
            self._codingTable = self.SelectCodingTable()
            self._codedData = self.EncodingData()
        else:
            self._codedData = Data
            (self._codingTable,self._clearData)=self.DecodingData()
    def SelectCodingTable(self):
        histogram = [ {'Index':i,'Value':0} for i in range(256)]
        for i in range(len(self._clearData)):
                item = list(
                    filter(lambda x:x['Index']==self._clearData[i],
                           histogram)
                    )[0]
                item['Value']+=1
        result=copy.deepcopy(histogram)
        result.sort(key=lambda x: x['Value'],reverse=True)
        result =result[0:self._tableLength]
        result = list(map(lambda x:x['Index'],result))
        return result
    def EncodingData(self):
        encodedData = []
        iEncodedData = 0
        for pattern in self._codingTable:
            iEncodedData = SmallFileCoder.CopyBits(encodedData, pattern, iEncodedData, 8)
        for n in range(len(self._clearData)):
            dato = self._clearData[n];
            if (any(map(lambda x:x==dato, self._codingTable))):
                proyected = list(map(lambda x: {'value':x,'index':self._codingTable.index(x)},self._codingTable))
                proyected = list(filter(lambda x:x['value']==dato,proyected))
                indexCode = proyected[0]['index']                    
                iEncodedData = SmallFileCoder.SetBit(encodedData, DataFormat.Encoded.value, iEncodedData);
                iEncodedData = SmallFileCoder.CopyBits(encodedData, indexCode, iEncodedData, self._codeLength)
            else:
                iEncodedData = SmallFileCoder.SetBit(encodedData, DataFormat.Clear.value, iEncodedData)
                iEncodedData = SmallFileCoder.CopyBits(encodedData, dato, iEncodedData, 8)
        return encodedData
    def DecodingData(self):
        codedTable = [0 for i in range(self._tableLength)]
        data = []
        codedTable=self._codedData[0:len(codedTable)]
        iEncodedBit = 8 * self._tableLength;
        iClearBits = 0
        while (True):
            curBit=SmallFileCoder.GetBit(self._codedData, iEncodedBit, self._codeLength);
            if (curBit is None): break
            iEncodedBit+=1
            if (curBit==DataFormat.Encoded.value):
                indexPattern = 0;
                (iEncodedBit,indexPattern) = SmallFileCoder.CopyBits(indexPattern, self._codedData, iEncodedBit, self._codeLength,self._codeLength);
                Pattern = codedTable[indexPattern];
                iClearBits = SmallFileCoder.CopyBits(data,Pattern,iClearBits,8);
            else:
                value = 0
                (iEncodedBit,value) = SmallFileCoder.CopyBits(value, self._codedData, iEncodedBit, 8, self._codeLength)
                iClearBits = SmallFileCoder.CopyBits(data, value, iClearBits, 8);
        return (codedTable,data)

    @staticmethod
    def SetBit(Destino: list,Value:bool, Position:int):
            if(Position%8==0):Destino.append(0)
            if (Value):
                Destino[len(Destino) - 1] |= (0x80>>(Position%8))
            return Position+1
    @staticmethod
    def GetBit(Data:list, Position:int,CodeLen:int=0):
        bitsLeft = (len(Data) * 8) - Position;
        if ((len(Data)) <= int(Position / 8)):
            return None
        CurrentBit = (Data[int(Position / 8)] & (0x80 >> (Position % 8))) != 0
        if (CodeLen > 0):
            if (CurrentBit == DataFormat.Encoded.value and bitsLeft < CodeLen): return None
            if (CurrentBit == DataFormat.Clear.value and bitsLeft < 8): return None
        return CurrentBit;
    @staticmethod
    @dispatch(int,list,int,int,int)
    def CopyBits(Destino:int, Origen:list, Position:int, bitsCount:int, CodeLen:int):
        for bit in range(0,bitsCount):
            curBit = SmallFileCoder.GetBit(Origen, Position)
            if (curBit is None): raise Exception("No se puedo leer el bit "+Position)
            if ( curBit==True):
                Destino |= (0x80 >> (8 - bitsCount) + bit)
            else:
                Destino &= (~(0x80 >> (8 - bitsCount) + bit));
            Position+=1
        return (Position,Destino)
    @staticmethod
    @dispatch(list,int,int,int)
    def CopyBits(Destino:list, Value:int,Position:int, bitsCount:int):
        c = (0x1 << (bitsCount - 1))
        while (c > 0):
            Position=SmallFileCoder.SetBit(Destino,(c & Value) != 0, Position)
            c >>= 1
        return Position
    @staticmethod
    def GetNoEndZerosData(datos):
        dataLength=len(datos)
        newDataLength=dataLength
        for i in range(0,dataLength):
            if datos[dataLength-i-1]!=0:
                newDataLength=dataLength-i
                break
        return datos[0:newDataLength]
    @staticmethod
    def CompleteEndZerosData(datos:list, dataSize:int=1536):
        newDatos = [0 for i in range(dataSize)]
        for i in  range(len(datos)):newDatos[i]=datos[i]
        return newDatos