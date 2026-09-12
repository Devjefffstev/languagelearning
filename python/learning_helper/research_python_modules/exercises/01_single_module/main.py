# main.py — starter for Exercise 01.
# Goal: bind the greeter module three different ways and call each binding.

import greeter

from greeter import greet
from greeter import greet as g 


def main():
    # TODO 1: bind the module with `import greeter`
    # TODO 2: bind the function with `from greeter import greet`
    # TODO 3: bind the module under an alias with `import greeter as g`
    # Then print a greeting from each binding.

    a = greeter.greet("Jeff")
    print(a)

    print("Hello " + greet("Lulu"))
    


if __name__ == "__main__":
    main()