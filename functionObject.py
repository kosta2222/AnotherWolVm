from constants import *
class FunctionObject:

    by_co:list=[]
    security:int=PRIVATE # для классов открытый по умолчанию

    nargs:int=0

    def __init__(self,by_co_body,nargs,sec=PRIVATE):

        self.security=sec
        self.by_co=by_co_body
        self.nargs=nargs
