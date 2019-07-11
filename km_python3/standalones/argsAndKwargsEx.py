'''
Created on Apr 9, 2019

Notes gathered from the documenations at this link:
http://book.pythontips.com/en/latest/args_and_kwargs.html 

@author: kmyren
'''
def test_var_args(f_arg, *argv):
    '''Will print out first arg and all following arguments.'''
    print("first normal arg:", f_arg)
    for arg in argv:
        print("another arg through *argv:", arg)

def greet_me_kwargs(**kwargs):
    '''Will print out the key and value pair of all inputs.'''
    for key, value in kwargs.items():
        print("{0} = {1}".format(key, value))
        
def test_args_kwargs_as_inputs(arg1, arg2, arg3):
    '''Will be used to test out reformatting list or dicts as inputs, in a normal method call'''
    print("arg1:", arg1)
    print("arg2:", arg2)
    print("arg3:", arg3)
        
def argsAndKwargsEx():
    print('-argsAndKwargsEx-\n')
    
    print('\n1. [test_var_args] Example:')
    test_var_args('yasoob', 'python', 'eggs', 'test')
    
    print('\n2. [greet_me_kwargs] Example:')
    greet_me_kwargs(name="yasoob", race='caucasian', height='6 ft 8 in', nationality='Costa Rican')
    
    
    print('\n3.1 [test_args_kwargs] Example:')
    argsList = ("two", 3, 5)  
    test_args_kwargs_as_inputs(*argsList)
    
    print('\n3.2 [test_args_kwargs] Example:')
    kwargsDict = {"arg3": 3, "arg2": "two", "arg1": 5}
    test_args_kwargs_as_inputs(**kwargsDict)
    

if __name__ == '__main__':
    argsAndKwargsEx()
    pass