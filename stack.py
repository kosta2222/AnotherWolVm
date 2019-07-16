from variable import Variable
class Stack:

    def __init__(self):
        self.mas:list=[]
    def pushInt(self,i:int):
        self.tmp:Variable=Variable()
        self.tmp.intValue=i
        self.mas.append(self.tmp)

    def popInt(self):
        return self.mas.pop().intValue 

    def pushFloat(self,fl:float):
        self.tmp:Variable=Variable()
        self.tmp.floatValue=fl
        self.mas.append(self.tmp)

    def popFloat(self):
        return self.mas.pop().floatValue 

    def pushStrValue(self,s:list):
        self.tmp:Variable=Variable()
        self.tmp.strValue=s
        self.mas.append(self.tmp)

    def popStrValue(self):
        return self.mas.pop().strValue

    def pushCharValue(self,c:list):
        self.tmp:Variable=Variable()
        self.tmp.charValue=c
        self.mas.append(self.tmp)

    def popCharValue(self):
        return self.mas.pop().charValue

    def pushBytecode(self,b:list):
        self.tmp:Variable=Variable()
        self.tmp.bytecode=b
        self.mas.append(self.tmp)

    def popBytecode(self):
        return self.mas.pop().bytecode 

    def __str__(self):
        str_vals='' 
        if len(self.mas)>0:
          topVar:Variable=self.mas[-1]

          str_vals='int Val:'+str(topVar.intValue)+'\nfloat Val:'+str(topVar.floatValue)+'\nchar Val:'+str(topVar.charValue)+\
          '\nstr Val:'+str(topVar.strValue)+'\nbytecode Val'+str(topVar.bytecode)

        return 'Top of Stack:'+ str_vals