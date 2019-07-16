#-*-coding:cp1251-*-
from constants import *
from struct import pack
import re

isa = isinstance
Symbol = str
key_words=['$','set!','arif','defun','return']
def op_prior(str_char_op):
    """
        Приоритет арифметической операции
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
        Это арифметическая операция?
    """

    if c=="-" or c=="+" or c=="*" or c=="/" or c=="%"or c=="^" :return True
    return False

def opn(str_code):
    """
        Перевод в обратную польскую запись
        @param str_code строка инфиксного выражения 
        @return список  постфиксного выражения
    """

    item_i=0
    # Операндовый стек
    OperatStack=[]
    # Выходной список
    resOpn=[]

    while (item_i<len(str_code)):

        # получить следующий член выражения  
        v=str_code[item_i]
        item_i+=1
        # определить тип члена
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
        запаковать число как набор байт
    """

    return pack('h',int_val)

def strToBytes(s):


    return pack('{}s'.format(len(s)),bytes(s,'cp1251'))
    
class Compiller:
    """
          Компилятор
    """

    def __init__(self):

        self.byteCode=[]
        self.startIp=0

        """
           Для формирования индекса переменной
        """
        self.nlocals=0

        """
          карта name => index
      """
        self.localss={}

    def generate(self,int_command):
        """"
             генерация байткода
             @param int_command добавляем число в список
        """

        self.byteCode.append(int_command)

    def varIndexByName(self,_name):
        """
            Находит индекс переменной в глобальной карте
            @param _name имя переменной
            @return кортеж индекс и лейбл карты
        """
        """
        Просматриваем карту
        """
        for pair in self.localss.items():

            if pair[0]==_name:

                return (pair[1],'L') 
            else:

                print("Undefined var:%s"%_name)
                exit(1)


    def compille(self,SExp):
        """
             рекурсивный разбор S-выражения SExp -список с числами и строками
             @param SExp список S-выражения

        """
        """
         S-выражение(Symbolyc expression) выражение вида:
         (<имя функции> <параметр-число> <параметр число> ... <другое S-выражение>:=(<имя функции>  <параметр-число> <параметр число> ...) )
    """
        """
       Всегда узнаем первый член выражения
    """
        """
       Распаковываем список.
       Генерируем соответствующий байт-код.
    """  
        print(SExp)
        if  isa(SExp[0], int):# Это число

            self.generate(iconst)
            self.byteCode.extend(shortToBytes(SExp[0]))

        elif  (SExp[0] not in key_words) :
             self.generate(load_name)
             print('str:',SExp[0])
             
             self.generate(len(SExp[0])) # длина строки 
             self.byteCode.extend(strToBytes(SExp[0]))
 

        elif SExp[0] == '//': # Это комментарии

            pass

        elif SExp[0] == 'set!': # создаем глобальную переменную

            (_, var, exp) = SExp

            self.compille(exp)
            self.generate(istore)

            """
            Локальная переменная не определена, поэтому создаем ее
            """
            if self.localss.get(var)==None:

                index=self.nlocals 
#--------------------------------------------                
                self.generate(index)
#--------------------------------------------
                self.localss[var]=index
                self.nlocals+=1
            
            # Локальная переменная определена, поэтому извлекаем ее (индекс)
            
            else:
            

                self.generate(self.localss.get(var))


        elif SExp[0] == '$': # выполнить выражения слева направо

            for exp in SExp[1:]:

                val = self.compille(exp)

        elif SExp[0] == 'arif': # Это арифметическое выражение

            resOpn=opn(SExp[1:]) # из инфиксной записи в ОПЗ
            """
          Заменяем в списке операции и индификаторы переменных(на индексы)
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
                elif re.match("[a-zA-Z]+",str(i)):# Если это строковый индификатор 

                    indexAndLocation=self.varIndexByName(i)

                    if indexAndLocation[1]=='L':

                        self.generate(iload)

                    # Индекс 
                    self.generate(indexAndLocation[0]) 
                elif isa(i,int):
                     self.generate(iconst)
                     self.byteCode.extend(shortToBytes(i)) 

        elif SExp[0]=='<':# сравнить на меньше

            (_,list_arif1,list_arif2)=SExp

            self.compille(list_arif1)
            self.compille(list_arif2)
            self.generate(ilt)

        elif SExp[0]=='=':# сравнить на равенство

            (_,list_arif1,list_arif2)=SExp

            self.compille(list_arif1)
            self.compille(list_arif2)
            self.generate(ieq)

        elif SExp[0]=='if':# если

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

        elif SExp[0]=='while': # пока

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

        elif SExp[0]=='pass': # ничего не делать

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

        else: # ошибка компиляции

            raise Exception("Unknown function name:%s"%SExp[0])


    def bytecode(self):
        """
             Возвращает результирующий байт код для ВМ
        """

        return self.byteCode
    
#*****************************Вспомогательные функции**********************
def read(s):
        """
            Читает lisp подобное выражение из строки и лексемазирует его
        """
    
        return read_from(tokenize(s))
    
def tokenize(s):
        """
             Ковертирует строку в питон список, токены
        """
    
        return s.replace('(',' ( ').replace(')',' ) ').split()
    
def read_from(tokens):
        """
            Читает выражение,создает 'атомы' - float или строки
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
           Числа становятся числами int , остальное символами,строками
        """
    
        try: return int(token)
        except ValueError:
            try: return int(token)
            except ValueError:
                return Symbol(token)
            
def  writeObjectFile(byteCode):
    """
    Функция записи из списка байт-кода в файл обьектной программы
    writeObjectFile_sLrV
    """ 
    objectProgramName='code.bin'
    with open(objectProgramName,'wb') as fileObj:
        for i in byteCode:
            oneBinData=pack('B',i)
            fileObj.write(oneBinData)            
    
#*****************************Вспомогательные функции**********************
    
   
    
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
                compiller.compille(read(f.read())) # анализируем исходный код программы в компиляторе
                writeObjectFile(compiller.bytecode())
                print(compiller.bytecode())
    
