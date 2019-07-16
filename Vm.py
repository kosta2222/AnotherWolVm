import sys 
from stack import Stack
from constants import *
from vmException import VmException


class langClass:
 
   def __init__(self):
       self.methods={}
       self.constructors={}
       
       self.fields={}
       self.constants={}

       self.parents={}

       self.security:int=PRIVATE 

       self.classType:int=DEFAULT

class FunctionObject:
  
  by_co:list=[]
  security:int=PRIVATE # для классов открытый по умолчанию

  nargs:int=0

  def __init__(self,by_co_body,nargs,sec=PRIVATE):

     self.security=sec
     self.by_co=by_co_body
     self.nargs=nargs
     

class Vm:
  bytecode=[
      load_name,0,"System",
      loads,

      load_name,0,"main",
      iconstNumArgs,0,
      load_bytecode,5,iconst,0,iload,1,returnVoid,
      make_function,

      load_name,0,"sum_func",
      invoke_function,
      end_file_startMain
      ]  
  def __init__(self,fileName:str):

      #with open(fileName,'rb') as f:

         #bytecode=f.read()
     pass

      
  def __str__(self):
     return 'Top of Vm loadStack:'+str(self.loadStack) 
  
  def execute(self,b_c:list):

    self.functions={}
    self.loadStack=Stack()
    ip=0
    
    b_c_par=[]
    str_par=''
    
    while(True):
      op=b_c[ip]
#--------------------------------# about load classes/functions    
      if op==load_bytecode:
        ip+=1
        amount_b_c=b_c[ip]

        for i in range(1,amount_b_c+1):
           b_c_par.append(b_c[ip+i])
       
        print(b_c_par)
        self.loadStack.pushBytecode(b_c_par)
        ip+=amount_b_c
      if op==load_name:
        ip+=1
        amount=b_c[ip]
        
        ip+=1
        str_par=b_c[ip]
       
        print(str_par)

        self.loadStack.pushStrValue(str_par)
        
      elif op==iconstNumArgs:
         ip+=1
         arg=b_c[ip]
         self.loadStack.pushInt(arg)
      
      elif op==make_function:
         func_obj=FunctionObject(self.loadStack.popBytecode(),self.loadStack.popInt(),PUBLIC)
         self.functions[self.loadStack.popStrValue()]=func_obj
         print('functions:',str(self.functions))
      elif op==end_file_startMain:
          try:
             funcObject=self.functions.get('main')
             by_co=funcObject.by_co
             print('bytecode main',by_co)
          except Exception :
             raise VmException("Main method not found")
          break
#--------------------------------------------

#--------------------------------------------about inner bytecode
      elif op==iconst:
         ip+=1
         arg=b_c[ip] 
      ip+=1                      

#===========================
version ="1.0.0"
info="Virtual Machine\nVersion:"+version+"\nAuthor: ."
if __name__=='__main__':

  if len(sys.argv)==1:
   print(info)
  else:
    if(sys.argv[1]=='-info'):
        print(info)
    else: 
      #programFileName=sys.argv[1]

      vm=Vm(sys.argv[1])
      vm.execute(vm.bytecode)
      print(vm)

#================================= 

  
