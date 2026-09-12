# Fibonnace numbers modules 

def fib(n):
    """Write Fib series up to n"""
    a,b=0,1 
    while a < n: 
        print(a, end=' ')
        a,b=b, a+b
    print()

def fibo_array(n):
    result=[]
    a,b=0,1
    while a < n:
        result.append(a)
        a,b=b,a+b
    return result 

# the code in the module will be executed, just as if you imported it, but with the __name__ set to "__main__". That means that by adding this code at the end of your module:

# if __name__ == "__main__":
#     import sys
#     fib(int(sys.argv[1]))
# you can make the file usable as a script as well as an importable module, because the code that parses the command line only runs if the module is executed as the “main” file:
if __name__=="__main__":
    import sys
    fib(int(sys.argv[1]))