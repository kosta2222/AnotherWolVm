#-*-coding:cp1251-*-
from constants import *
from struct import pack
import re

isa = isinstance
Symbol = str
key_words=['$','set!','arif','defun','return']
def op_prior(str_char_op):
    """
        ��������� �������������� ��������
    """

    if str_char_op=="^":

        return 6
    elif str_char_op=="*":

        return 5
    elif str_char_op=="/":

        return 5
    elif str_char_op=="%":

        return 3
    elif str_char_op=="+":

        return 2
    elif str_char_op=="-":

        return 2

def isOp(c):
    """
        ��� �������������� ��������?
    """

    if c=="-" or c=="+" or c=="*" or c=="/" or c=="%"or c=="^" :return True
    return False

def opn(str_code):
    """
        ������� � �������� �������� ������
        @param str_code ������ ���������� ��������� 
        @return ������  ������������ ���������
    """

    item_i=0
    # ����������� ����
    OperatStack=[]
    # �������� ������
    resOpn=[]

    while (item_i<len(str_code)):

        # �������� ��������� ���� ���������  
        v=str_code[item_i]
        item_i+=1
        # ���������� ��� �����
        if isa(v,int):

            resOpn.append(v)
        elif re.match("[A-Za-z]+",str(v)):

            resOpn.append(v)
        elif isOp(v):

                while(len(OperatStack)>0 and
                OperatStack[-1]!="[" and
                op_prior(v)<=op_prior(OperatStack[-1]) ):
                    resOpn.append(OperatStack.pop())

                OperatStack.append(v)
        elif v==']':

            while len(OperatStack)>0:

                x=OperatStack.pop()
                if x=='[':

                    break
                resOpn.append(x)
        elif v=="[":
            OperatStack.append(v)
    while len(OperatStack)>0 :

           resOpn.append(OperatStack.pop())

    return resOpn

def shortToBytes(int_val):
    """
        ���������� ����� ��� ����� ����
    """

    return pack('h',int_val)

def strToBytes(s):


    return pack('{}s'.format(len(s)),bytes(s,'cp1251'))
    
class Compiller:
    """
          ����������
    """

    def __init__(self):

        self.byteCode=[]
        self.startIp=0

        """
           ��� ������������ ������� ����������
        """
        self.nlocals=0

        """
          ����� name => index
      """
        self.localss={}

    def generate(self,int_command):
        """"
             ��������� ��������
             @param int_command ��������� ����� � ������
        """

        self.byteCode.append(int_command)

    def varIndexByName(self,_name):
        """
            ������� ������ ���������� � ���������� �����
            @param _name ��� ����������
            @return ������ ������ � ����� �����
        """
        """
        ������������� �����
        """
        for pair in self.localss.items():

            if pair[0]==_name:

                return (pair[1],'L') 
            else:

                print("Undefined var:%s"%_name)
                exit(1)


    def compille(self,SExp):
        """
             ����������� ������ S-��������� SExp -������ � ������� � ��������
             @param SExp ������ S-���������

        """
        """
         S-���������(Symbolyc expression) ��������� ����:
         (<��� �������> <��������-�����> <�������� �����> ... <������ S-���������>:=(<��� �������>  <��������-�����> <�������� �����> ...) )
    """
        """
       ������ ������ ������ ���� ���������
    """
        """
       ������������� ������.
       ���������� ��������������� ����-���.
    """  
        print(SExp)
        if  isa(SExp[0], int):# ��� �����

            self.generate(iconst)
            self.byteCode.extend(shortToBytes(SExp[0]))

        elif  (SExp[0] not in key_words) :
             self.generate(load_name)
             print('str:',SExp[0])
             
             self.generate(len(SExp[0])) # ����� ������ 
             self.byteCode.extend(strToBytes(SExp[0]))
 

        elif SExp[0] == '//': # ��� �����������

            pass

        elif SExp[0] == 'set!': # ������� ���������� ����������

            (_, var, exp) = SExp

            self.compille(exp)
            self.generate(istore)

            """
            ��������� ���������� �� ����������, ������� ������� ��
            """
            if self.localss.get(var)==None:

                index=self.nlocals 
#--------------------------------------------                
                self.generate(index)
#--------------------------------------------
                self.localss[var]=index
                self.nlocals+=1
            
            # ��������� ���������� ����������, ������� ��������� �� (������)
            
            else:
            

                self.generate(self.localss.get(var))


        elif SExp[0] == '$': # ��������� ��������� ����� �������

            for exp in SExp[1:]:

                val = self.compille(exp)

        elif SExp[0] == 'arif': # ��� �������������� ���������

            resOpn=opn(SExp[1:]) # �� ��������� ������ � ���
            """
          �������� � ������ �������� � ������������ ����������(�� �������)
        """
            for i in resOpn:

                if isOp(i):

                    if i=="+":

                        self.generate(iadd)
                    if i=="-":

                        self.generate(isub)
                    if i=="*":

                        self.generate(imul)
                    if i=="/":

                        self.generate(idiv)
                    if i=="%":

                        self.generate(irem)
                    if i=="^":

                        self.generate(ipow)
                elif re.match("[a-zA-Z]+",str(i)):# ���� ��� ��������� ����������� 

                    indexAndLocation=self.varIndexByName(i)

                    if indexAndLocation[1]=='L':

                        self.generate(iload)

                    # ������ 
                    self.generate(indexAndLocation[0]) 
                elif isa(i,int):
                     self.generate(iconst)
                     self.byteCode.extend(shortToBytes(i)) 

        elif SExp[0]=='<':# �������� �� ������

            (_,list_arif1,list_arif2)=SExp

            self.compille(list_arif1)
            self.compille(list_arif2)
            self.generate(ilt)

        elif SExp[0]=='=':# �������� �� ���������

            (_,list_arif1,list_arif2)=SExp

            self.compille(list_arif1)
            self.compille(list_arif2)
            self.generate(ieq)

        elif SExp[0]=='if':# ����

            (_,list_test,list_trueEpr,list_falseExpr)=SExp

            self.compille(list_test)
            self.generate(brf)
            self.generate(0)
            self.generate(0)
            nAddr0_1=len(self.byteCode)
            self.compille(list_trueEpr)
            self.generate(br)
            self.generate(0)
            self.generate(0)
            nAddr1_2=len(self.byteCode)
            delta1=nAddr1_2-nAddr0_1
            self.byteCode[nAddr0_1-2]=shortToBytes(delta1)[0]
            self.byteCode[nAddr0_1-1]=shortToBytes(delta1)[1]
            self.compille(list_falseExpr)
            nAddr3_4=len(self.byteCode)
            delta2=(nAddr3_4-nAddr1_2)+2
            self.byteCode[nAddr1_2-2]=shortToBytes(delta2)[0]
            self.byteCode[nAddr1_2-1]=shortToBytes(delta2)[1]

        elif SExp[0]=='while': # ����

            (_,list_test,list_whileBody)=SExp

            nAddr1_2=len(self.byteCode)
            self.compille(list_test)
            self.generate(brf)
            self.generate(0)
            self.generate(0)
            nAddr0_1=len(self.byteCode)
            self.compille(list_whileBody)
            self.generate(br)
            self.generate(0)
            self.generate(0)
            nAddr2_3=len(self.byteCode)
            delta1=nAddr2_3-nAddr0_1
            delta2=(nAddr2_3-nAddr1_2)-2
            self.byteCode[nAddr0_1-2]=shortToBytes(delta1)[0]
            self.byteCode[nAddr0_1-1]=shortToBytes(delta1)[1]
            self.byteCode[nAddr2_3-2]=shortToBytes(-delta2)[0]
            self.byteCode[nAddr2_3-1]=shortToBytes(-delta2)[1]

        elif SExp[0]=='pass': # ������ �� ������

            self.generate(noop)
        elif SExp[0]=='defun':
           (_,nameFunc,arg,body)=SExp
           self.compille(nameFunc) 
           #self.compille([0])
           self.generate(load_bytecode)
           self.generate(0)
           n1by_co=len(self.byteCode)
           self.compille(body)
           n2by_co=len(self.byteCode)
           deltaBy_co=n2by_co-n1by_co
           self.byteCode[len(self.byteCode)-deltaBy_co-1]=deltaBy_co
           
        elif SExp[0]=='return':
            self.generate(return_)

        else: # ������ ����������

            raise Exception("Unknown function name:%s"%SExp[0])


    def bytecode(self):
        """
             ���������� �������������� ���� ��� ��� ��
        """

        return self.byteCode
    
#*****************************��������������� �������**********************
def read(s):
        """
            ������ lisp �������� ��������� �� ������ � ������������� ���
        """
    
        return read_from(tokenize(s))
    
def tokenize(s):
        """
             ����������� ������ � ����� ������, ������
        """
    
        return s.replace('(',' ( ').replace(')',' ) ').split()
    
def read_from(tokens):
        """
            ������ ���������,������� '�����' - float ��� ������
        """
    
        if len(tokens) == 0:
    
            raise SyntaxError('unexpected EOF while reading')
    
        token = tokens.pop(0)
        if '(' == token:
    
            L = []
            while tokens[0] != ')':
                L.append(read_from(tokens))
            tokens.pop(0) # pop off ')'
            return L
    
        elif ')' == token:
    
            raise SyntaxError('unexpected )')
    
        else:
    
            return atom(token)
    
def atom(token):
        """
           ����� ���������� ������� int , ��������� ���������,��������
        """
    
        try: return int(token)
        except ValueError:
            try: return int(token)
            except ValueError:
                return Symbol(token)
            
def  writeObjectFile(byteCode):
    """
    ������� ������ �� ������ ����-���� � ���� ��������� ���������
    writeObjectFile_sLrV
    """ 
    objectProgramName='code.bin'
    with open(objectProgramName,'wb') as fileObj:
        for i in byteCode:
            oneBinData=pack('B',i)
            fileObj.write(oneBinData)            
    
#*****************************��������������� �������**********************
    
   
    
import sys
version ="1.0.0"
info="Compiller\nVersion:"+version+"\nAuthor:Muhamedjanov Konstantin K. ."
if __name__=='__main__':
    
        if len(sys.argv)==1:
            print(info)
        else:
            if(sys.argv[1]=='-info'):
                print(info)
            else:
              with open(sys.argv[1],'r') as f:  
                compiller=Compiller()
                compiller.compille(read(f.read())) # ����������� �������� ��� ��������� � �����������
                writeObjectFile(compiller.bytecode())
                print(compiller.bytecode())
    
