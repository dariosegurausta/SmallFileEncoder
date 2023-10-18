#============== MEM - USTA =======================
# Funciones de ayuda para el procesamiento generico de informacion y visualización

def printArray_HexFormat(array):
    for i in range(0,len(array)):
        
        if str(type(array[i]))=="<class 'int'>":
            print("%.2X"%array[i],end='');
        else:
            printArray_HexFormat(array[i]);
    print()
def ArrayToVector(array:list):
    vector=[]
    for x in range(len(array)):
        for y in range(len(array[x])):
            vector.append(array[x][y])
    return vector