from variable import Variable
class Locals:

    def __init__(self,amount):
        self.localss=[Variable()]*amount

    def atInt(self,index,i):
        self.tmp=Variable()
        self.tmp.intValue=i
        self.localss[index]=self.tmp

    def getInt(index):
        return self.localss[index].intValue 

    def atFloat(self,index,fl:float):
        self.tmp=Variable()
        self.tmp.floatValue=fl
        self.localss[index]=self.tmp

    def getFloat(self,index):
        return self.localss[index].floatValue

    def atStr(self,index,s:list):
        self.tmp=Variable()
        self.tmp.strValue=s
        self.locals[index]=self.tmp

    def getStr(self):
         return self.localss[index].strValue

    def atBytecode(self,index,b:list):
        self.tmp=Variable()
        self.tmp.strValue=b
        self.locals[index]=self.tmp

    def getBytecode(self):
         return self.localss[index].bytecode


    def atChar(self,index,c:str):
        self.tmp=Variable()
        self.tmp.charValue=c
        self.localss[index]=self.tmp

    def getChar(self):
         return self.localss[index].charValue    