class Variable:

    def __init__(self):
        self.intValue=0
        self.floatValue=0.0
        self.charValue=''
        self.strValue=[] # C as char* for bytecode and names
        self.bytecode:list=[] # function body C as unsigned char*