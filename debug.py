import pdb
pdb.set_trace()

(load_bytecode,load_name,invoke_function,make_function,iconst,iload,_return,_loads,end_file_end)=range(9)
class Variable:

    def __init__(self):
        self.intValue=0
        self.floatValue=0.0
        self.charValue=''
        self.strValue=[] # C as char* for names
        self.bytecode:list=[] # function body C as unsigned char*

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

bytecode=[
      load_name,0,"System",
      _loads,

      load_name,0,"sum_func",
      load_bytecode,5,iconst,0,iload,1,_return,
      iconst,0,
      make_function,

      load_name,0,"sum_func",
      invoke_function,
      end_file_end
      ]
      #self.mainStack=Stack()
def execute(b_c:list):

    functions={}
    mainStack=Stack()
    ip=0
    while(True):
      op=b_c[ip]
    
      if op==load_bytecode:
        ip+=1
        amount_b_c=b_c[ip]

        b_c_par=[]
        for i in range(ip,amount_b_c):
           b_c_par.append(b_c[ip+i])
       
        print(b_c_par)
        mainStack.pushBytecode(b_c_par)
        ip+=amount_b_c
      if op==load_name:
        ip+=1
        amount=b_c[ip]
        
        ip+=1
        str_par=b_c[ip]
       # for i in range(ip,amount+1):
        #   str_par.append(i)
       
        print(str_par)

        mainStack.pushStrValue(str_par)
        
      elif op==iconst:
         ip+=1
         arg=b_c[ip]
         
      elif op==end_file_end:
        break
      ip+=1
            
        
execute(bytecode)        
