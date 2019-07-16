import sys 
from stack import Stack
from localss import Locals
from variable import Variable
from constants import *
from functionObject import FunctionObject
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

class Frame:
   def __init__(self,amountLocals,nargs):
      self.stack=Stack()
      self.locals_=Locals(amountLocals)
      self.returnValue=Variable()
      

class Vm:
  bytecode=[
      load_name,0,"System",
      loads,

      load_name,0,"main",
      iconstNumArgs,0,
      load_bytecode,8,iconst,5,iconst,4,iadd,iload,1,return_,
      make_function,

      load_name,0,"sum_func",
      invoke_function,
      end_file_startMain
      ]  
  def __init__(self,fileName:str):

      #with open(fileName,'rb') as f:

         #bytecode=f.read()
     pass
     self.frame=None 
      

  
  def execute(self,stackFrame:list,b_c:list):
    frame=None 
    if(stackFrame!=None):
        frame=stackFrame[-1]
        print('begin St Fr',stackFrame)
        print('frame',frame)
        print('begi b_c',b_c)
        self.frame=frame

    functions={}       #  functions=map<str,FunctionObject>
    loadStack=Stack()  #  loadStack=vector<Variable>
    stackFrame=[]      #  stackFrame=vector<Frame>
    ip=0
    
    b_c_par=[]
    str_par=''
    
    while(True):
      op=b_c[ip]
      print(op)
#--------------------------------# about load classes/functions    
      if op==load_bytecode:
        ip+=1
        amount_b_c=b_c[ip]

        for i in range(1,amount_b_c+1):
           b_c_par.append(b_c[ip+i])
       
        print(b_c_par)
        loadStack.pushBytecode(b_c_par) 
        ip+=amount_b_c
      if op==load_name:
        ip+=1
        amount=b_c[ip]
        
        ip+=1
        str_par=b_c[ip]
       
        print(str_par)

        loadStack.pushStrValue(str_par)
        
      elif op==iconstNumArgs:
         ip+=1
         arg=b_c[ip]
         loadStack.pushInt(arg)
      
      elif op==make_function:
         func_obj=FunctionObject(loadStack.popBytecode(),loadStack.popInt(),PUBLIC)
         functions[loadStack.popStrValue()]=func_obj
         print('functions:',str(functions))
      elif op==end_file_startMain:
          try:
             funcObject=functions.get('main')
             by_co=funcObject.by_co
             print('bytecode main',by_co)
             currentFrame=Frame(10,funcObject.nargs)
             stackFrame.append(currentFrame)
             print('stack Frame:',str(stackFrame))
             self.execute(stackFrame,by_co)
          except Exception :
             raise VmException("Main method not found")
          break
#--------------------------------------------

#********************************************about inner bytecode
#--------------------------------------------
      elif op==iconst:
         ip+=1
         arg=b_c[ip] 
         frame.stack.pushInt(arg)
#--------------------------------------------
#--------------------------------------------Arifmetic ops
      elif op==iadd:
         frame.stack.pushInt(frame.stack.popInt()+frame.stack.popInt())
#--------------------------------------------
      
         
      elif op==iload:
         ip+=1
         arg=b_c[ip]
      elif op==return_:
         print('ret')
         break
#***************************************************      
      ip+=1 
  def __str__(self):
     return 'FrameStack of fu:'+str(self.frame.stack)       

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
      vm.execute(None,vm.bytecode)
      print(vm)

#================================= 

  
