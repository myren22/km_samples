'''
Created on Apr 9, 2019

@author: kmyren
'''

class MyClass():
    '''
    classdocs
    '''


    def __init__(self, param1, param2):
        '''
        Constructor
        '''
        self.someValue=None
        pass
    def aMethod(self):
        '''
        aMethod notes
        '''
    def printHello(self, extraStr=''):
        '''
        printHello prints hello!, and maybe some extra info if provided
        '''
        print('hello!',extraStr)
        
if __name__ == '__main__':
    aClassObj = MyClass(1, 'aStr')
    aClassObj.printHello()
    