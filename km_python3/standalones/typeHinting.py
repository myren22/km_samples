##############################################################
#
# TypeHinting is a feature added in python 3.5 and later.
# The hints are treated only as syntax, unless used with "mypy", which will
# throw an exception if a type input or return is violated.
#
# to run with mypy, simply install with "pip install mypy"
# then call mypy from terminal, "mypy typeHinting.py"
#
##############################################################

def hello_name(name: str) -> str:
    return(f"Hello {name}")
    
def add_two_nums(val1: int, val2: int) -> int:
    return val1 + val2
    
if __name__ == "__main__":
    """
    This is only called if the file is called directly by user when running python.
    if imported by other classes it does not run.
    """
    a1 =hello_name("kyle")
    #===========================================================================
    # a2= add_two_nums(1, 5)
    #===========================================================================
    print(hello_name("john"))
    print(str( add_two_nums(3, 9)))
    
    #Now to have an invalid type.
    #Have 2 strings as input and add them together. this is valid normally. 
    #Only when running mypy will it fail.
    print(str( add_two_nums("first.","second")))
    